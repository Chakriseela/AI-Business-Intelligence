import asyncio
import json
import re
import ollama


from google import genai
from google.genai import types
from backend.Prompts.generate_sql import get_sql_prompt

from backend.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OLLAMA_MODEL
)

from backend.mcp_server.client import MCPClient
from backend.observability.phoenix_setup import tracer


# =========================================================
# Gemini Client
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# Gemini config
# =========================================================

GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)


# =========================================================
# SQL Validation
# =========================================================

def validate_sql(query: str) -> tuple[bool, str]:

    if not query:
        return False, "Generated SQL is empty."

    query = query.replace("```sql", "")
    query = query.replace("```", "")
    query = query.strip()

    query_lower = query.lower()

    # Only SELECT
    if not query_lower.startswith("select"):
        return False, "Only SELECT statements are allowed."

    # Prevent multiple statements
    if ";" in query.rstrip(";"):
        return False, "Multiple SQL statements are not allowed."

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "attach",
        "detach",
        "pragma",
    ]

    for keyword in blocked_keywords:

        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, query_lower):
            return False, (
                f"Blocked SQL operation: {keyword}"
            )

    return True, query


# =========================================================
# Find SQL MCP Tool
# =========================================================

def find_sql_tool(
    tools: list[dict]
) -> dict:

    for tool in tools:

        schema = tool.get(
            "input_schema",
            {}
        )

        properties = schema.get(
            "properties",
            {}
        )

        if "query" in properties:
            return tool

    raise RuntimeError(
        "No SQL MCP tool was found."
    )


# =========================================================
# Generate SQL
# =========================================================

def generate_sql(
    question: str,
    tool_description: str,
    input_schema: dict,
    model_provider: str,
    model_name: str,
) -> str:

    prompt = get_sql_prompt(tool_description, input_schema, question)

    # try:

    #     response = client.models.generate_content(
    #         model=GEMINI_MODEL,
    #         contents=prompt,
    #         # config=GENERATION_CONFIG,
    #     )
    #     sql = response.text.strip()

    # except Exception:

    #     response = ollama.chat(
    #         model=OLLAMA_MODEL,
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": prompt,
    #             }
    #         ],
    #     )
    #     sql = response["message"]["content"]

    if model_provider == "ollama":
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        sql = (
            response
            .get("message", {})
            .get("content", "")
        )
    else:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=GENERATION_CONFIG,
        )

        if isinstance(response, str):
            sql = response
        else:
            sql = response.text or ""


    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    # Make sure we actually got SQL
    if not sql:
        raise RuntimeError(
            f"{model_provider} returned an empty SQL response."
        )

    return sql


# =========================================================
# SQL Agent
# =========================================================

async def sql_agent(
    question: str,
    model_provider: str = "gemini",
    model_name: str = GEMINI_MODEL,
) -> dict:

    with tracer.start_as_current_span("sql_agent") as span:
        """
        SQL Agent responsibilities:

        1. Discover SQL MCP tool
        2. Generate SQL using Gemini
        3. Validate SQL
        4. Call MCP
        5. Return database evidence

        It does NOT generate the final natural-language answer.
        """
        span.set_attribute("agent.name", "sql_agent")
        span.set_attribute("input.question", question)
        span.set_attribute("llm.provider", model_provider)
        span.set_attribute("llm.model", model_name)

        async with MCPClient() as mcp_client:
            with tracer.start_as_current_span("mcp.list_tools") as mcp_span:

                # -------------------------------------------------
                # Discover MCP tools
                # -------------------------------------------------

                tools = await mcp_client.list_tools()

                mcp_span.set_attribute("mcp.tool.count", len(tools))

            sql_tool = find_sql_tool(tools)

            span.set_attribute("mcp.sql_tool.name", sql_tool["name"])

            # -------------------------------------------------
            # Generate SQL
            # -------------------------------------------------
            with tracer.start_as_current_span("gemini.sql_generation") as llm_span:
                generated_sql = generate_sql(
                    question=question,
                    tool_description=sql_tool["description"],
                    input_schema=sql_tool["input_schema"],
                    model_provider=model_provider,
                    model_name=model_name,
                )

                llm_span.set_attribute("llm.model", model_name)
                llm_span.set_attribute("sql.generated", generated_sql)
            

            # -------------------------------------------------
            # Validate SQL
            # -------------------------------------------------

            with tracer.start_as_current_span("sql.validation") as validation_span:
                is_valid, validated_sql = validate_sql(
                    generated_sql
                )

                validation_span.set_attribute("sql.valid", is_valid)
                validation_span.set_attribute("sql.validated", validated_sql)

                if not is_valid:

                    return {
                        "success": False,
                        "sql": generated_sql,
                        "data": [],
                        "row_count": 0,
                        "mcp_tool": sql_tool["name"],
                        "error": validated_sql,
                    }

            # -------------------------------------------------
            # Call MCP Tool
            # -------------------------------------------------

            with tracer.start_as_current_span("mcp.call_tool") as mcp_span:

                mcp_span.set_attribute("mcp.tool.name", sql_tool["name"])
                mcp_span.set_attribute("db.sql", validated_sql)


                tool_result = await mcp_client.call_tool(
                    tool_name=sql_tool["name"],
                    arguments={
                        "query": validated_sql
                    },
                )

                mcp_span.set_attribute("mcp.error", tool_result.get("is_error", False))
    # -----------------------------------------------------
    # Extract structured result
    # -----------------------------------------------------

    database_result = tool_result.get(
        "structured_content"
    )

    # Fallback to text content
    if not database_result:

        for content in tool_result.get(
            "content",
            []
        ):
            try:
                parsed = json.loads(content)

                if isinstance(parsed, dict):
                    database_result = parsed
                    break

            except (json.JSONDecodeError, TypeError):
                continue

    if not database_result:
        database_result = {}

    # -----------------------------------------------------
    # MCP error
    # -----------------------------------------------------

    if tool_result.get("is_error"):

        return {
            "success": False,
            "sql": validated_sql,
            "data": [],
            "row_count": 0,
            "mcp_tool": sql_tool["name"],
            "error": tool_result,
        }

    span.set_attribute("db.row_count", database_result.get("row_count", 0))

    # -----------------------------------------------------
    # Return evidence only
    # -----------------------------------------------------

    return {
        "success": database_result.get(
            "success",
            True
        ),

        "sql": validated_sql,

        "data": database_result.get(
            "data",
            []
        ),

        "row_count": database_result.get(
            "row_count",
            0
        ),

        "mcp_tool": sql_tool["name"],
    }


# =========================================================
# Sync Wrapper
# =========================================================

def run_sql_agent(
    question: str
) -> dict:

    return asyncio.run(
        sql_agent(question)
    )


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    question = input(
        "Ask a business question: "
    )

    result = run_sql_agent(
        question
    )

    print("\n" + "=" * 60)
    print("SQL AGENT")
    print("=" * 60)

    print("\nGenerated SQL:")
    print(
        result.get(
            "sql"
        )
    )

    print("\nMCP Tool:")
    print(
        result.get(
            "mcp_tool"
        )
    )

    print("\nDatabase Data:")
    print(
        result.get(
            "data"
        )
    )

    print(
        f"\nRows: "
        f"{result.get('row_count', 0)}"
    )