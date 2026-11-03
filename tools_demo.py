import ollama
from datetime import datetime

MODEL = "llama3.2:3b"

def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: The first number
        b: The second number
    """
    return a + b

def get_time() -> str:
    """Get the current time of day."""
    return datetime.now().strftime("%H:%M")

available = {"add": add, "get_time": get_time}

messages = [{"role": "user", "content": input("Ask me something: ")}]

response = ollama.chat(model=MODEL, messages=messages, tools=[add, get_time])
messages.append(response.message)

if response.message.tool_calls:
    for call in response.message.tool_calls:
        name = call.function.name
        args = call.function.arguments
        print(f"[Model wants to call {name} with {args}]")
        result = available[name](**args)
        messages.append({"role": "tool", "tool_name": name, "content": str(result)})

    final = ollama.chat(model=MODEL, messages=messages)
    print("Answer:", final.message.content)
else:
    print("Answer:", response.message.content)