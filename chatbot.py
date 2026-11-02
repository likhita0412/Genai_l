import ollama
from datetime import datetime

SYSTEM_PROMPT = "You are a pirate. Explain everything like one for computer science students. Keep answers concise."
options = {"temperature": 0.7, "num_predict": 300}

history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("Commands: /reset  /save  quit")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in {"quit", "exit"}:
        break

    if user_input == "/reset":
        history = [{"role": "system", "content": SYSTEM_PROMPT}]
        print("Conversation cleared.\n")
        continue

    if user_input == "/save":
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            for msg in history:
                if msg["role"] != "system":
                    f.write(f"{msg['role'].capitalize()}: {msg['content']}\n\n")
        print(f"Saved to {filename}\n")
        continue

    if not user_input:
        continue

    history.append({"role": "user", "content": user_input})

    reply = ""
    print("Bot: ", end="", flush=True)
    for chunk in ollama.chat(model="llama3.2:3b", messages=history, options=options, stream=True):
        text = chunk["message"]["content"]
        print(text, end="", flush=True)
        reply += text
    print("\n")

    history.append({"role": "assistant", "content": reply})