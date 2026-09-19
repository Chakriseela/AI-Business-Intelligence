import ollama

response = ollama.chat(
    model="qwen3.5:0.8b",
    messages=[
        {
            "role": "user",
            "content": "what is your name",
        }
    ],
)

answer = response["message"]["content"]
print(answer)