import asyncio
import json
import re
import ollama


from google import genai
from google.genai import types

from backend.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OLLAMA_MODEL
)

from backend.mcp_server.client import MCPClient


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
) -> str:

    prompt = f"""
You are the SQL reasoning agent for BizInsight AI.

Convert the user's business question into ONE valid
SQLite SELECT query.

MCP SQL Tool Description:
{tool_description}

MCP Tool Input Schema:
{input_schema}

Database guidance:

- customers = customer information
- products = product information
- orders = order-level sales information
- order_items = products inside each order

Important rules:

- Use only the tables and columns described above.
- Generate only SELECT.
- Never generate INSERT, UPDATE, DELETE, DROP,
  ALTER, CREATE, PRAGMA, ATTACH, or DETACH.
- Use SQLite syntax.
- When calculating sales or revenue, normally use
  completed orders only unless the user explicitly
  asks for cancelled/all orders.
- Return ONLY SQL.
- Do not use markdown.

User Question:
{question}
"""

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            # config=GENERATION_CONFIG,
        )
        sql = response.text.strip()

    except Exception:

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        sql = response["message"]["content"]
    


    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    # Make sure we actually got SQL
    if not sql:
        raise RuntimeError(
            "Both Gemini and Ollama returned an empty SQL response."
        )

    return sql


# =========================================================
# SQL Agent
# =========================================================

async def sql_agent(
    question: str
) -> dict:
    """
    SQL Agent responsibilities:

    1. Discover SQL MCP tool
    2. Generate SQL using Gemini
    3. Validate SQL
    4. Call MCP
    5. Return database evidence

    It does NOT generate the final natural-language answer.
    """

    async with MCPClient() as mcp_client:

        # -------------------------------------------------
        # Discover MCP tools
        # -------------------------------------------------

        tools = await mcp_client.list_tools()

        sql_tool = find_sql_tool(tools)

        # -------------------------------------------------
        # Generate SQL
        # -------------------------------------------------

        generated_sql = generate_sql(
            question=question,
            tool_description=sql_tool["description"],
            input_schema=sql_tool["input_schema"],
        )

        # -------------------------------------------------
        # Validate SQL
        # -------------------------------------------------

        is_valid, validated_sql = validate_sql(
            generated_sql
        )

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

        tool_result = await mcp_client.call_tool(
            tool_name=sql_tool["name"],
            arguments={
                "query": validated_sql
            },
        )

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