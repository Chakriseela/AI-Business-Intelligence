from google import genai
import ollama
from backend.config.settings import GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_MODEL
from backend.Prompts.responce_prompt import get_response_prompt
from backend.observability.phoenix_setup import tracer


client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# Response Agent
# =========================================================

def response_agent(
    question: str,
    sql_result: dict | None = None,
    rag_result: dict | None = None,
    model_provider: str = "gemini",
    model_name: str = GEMINI_MODEL,
) -> str:

    with tracer.start_as_current_span("response_agent") as span:

        span.set_attribute("agent.name", "response_agent")
        span.set_attribute("input.question", question)
        span.set_attribute("llm.provider", model_provider)
        span.set_attribute("llm.model", model_name)
    
        """
        Final Response Agent.

        Combines evidence from:
        - SQL Agent
        - RAG Agent
        - or both
        """

        sql_result = sql_result or {}
        rag_result = rag_result or {}

        sql_data = sql_result.get("data",[])

        executed_sql = sql_result.get("sql","")

        rag_context = rag_result.get("context","")

        rag_sources = rag_result.get("sources",[])

        # -----------------------------------------------------
        # Build evidence
        # -----------------------------------------------------

        evidence = ""

        if sql_result:

            evidence += f"""
===== SQL EVIDENCE =====

SQL Query:
{executed_sql}

Database Result:
{sql_data}

Rows:
{sql_result.get('row_count', 0)}
"""

        if rag_result:

            evidence += f"""
    ===== RAG EVIDENCE =====

    Retrieved Documents:
    {rag_sources}

    Knowledge Base Context:
    {rag_context}
    """

        # -----------------------------------------------------
        # Prompt
        # -----------------------------------------------------

        prompt = get_response_prompt(question, evidence)

        # -----------------------------------------------------
        # Generate final answer
        # -----------------------------------------------------
        with tracer.start_as_current_span("llm.response_generation") as llm_span:

            llm_span.set_attribute("llm.model", model_name)

            try:

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
            
                    answer = (
                        response
                        .get("message", {})
                        .get("content", "")
                        .strip()
                    )
                else:
                    
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    if isinstance(response, str):
                        answer = response.strip()
                    else:
                        answer = (
                            response.text or ""
                        ).strip()
            
            except Exception as exc:

                raise RuntimeError(
                    f"Response generation failed "
                    f"using {model_provider}/{model_name}: {exc}"
                ) from exc
            
            if not answer:
                raise RuntimeError(
                    f"{model_provider}/{model_name} returned "
                    "an empty response."
                )
            return answer
 



    # try:

    #     response = client.models.generate_content(
    #         model=GEMINI_MODEL,
    #         contents=prompt,
    #         # config=GENERATION_CONFIG,
    #     )
    #     return response.text.strip()


    # except Exception:
    #     ollama_response  = ollama.chat(
    #         model=OLLAMA_MODEL,
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": prompt,
    #             }
    #         ],
    #     )
    #     return ollama_response["message"]["content"]
      