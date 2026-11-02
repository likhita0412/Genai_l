import json
import ollama

response = ollama.chat(
    model="llama3.2:3b",
    format="json",
    messages=[{
        "role": "user",
        "content": 'Extract from this text: "Alice, 21, studies CS at MIT." '
                   "Return JSON with keys name, age, major, university.",
    }],
)

data = json.loads(response["message"]["content"])
print(data)
print(data["name"])