# import ollama

# response = ollama.chat(
#     model="qwen3.5:0.8b",
#     messages=[
#         {
#             "role": "user",
#             "content": "what is your name",
#         }
#     ],
# )

# answer = response["message"]["content"]
# print(answer)

import os
from dotenv import load_dotenv
load_dotenv()  

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create( model="gpt-5-mini", input="Write a short bedtime story about a unicorn.")

print(response.output_text)