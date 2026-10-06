import ollama
from backend.config.settings import GEMINI_API_KEY
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_with_selected_model(
    prompt: str,
    provider: str,
    model_name: str,
) -> str:
 
    if provider == "ollama":
 
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return (
            response
            .get("message", {})
            .get("content", "")
            .strip()
        )
 
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
 
    if isinstance(response, str):
        return response.strip()
    
    return (response.text or "").strip()
 