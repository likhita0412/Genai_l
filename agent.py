import ollama
from datetime import datetime

MODEL = "llama3.2:3b"
MAX_STEPS = 5  # safety limit so it can never loop forever

def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: The first number
        b: The second number
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers together.

    Args:
        a: The first number
        b: The second number
    """
    return a * b

def get_time() -> str:
    """Get the current time of day."""
    return datetime.now().strftime("%H:%M")

def read_file(filename: str) -> str:
    """Read a text file from the current folder and return its contents.

    Args:
        filename: The name of the file, for example notes.txt
    """
    with open(filename) as f:
        return f.read()[:3000]  # cap the size so it fits in the context window

tools = [add, multiply, get_time, read_file]
available = {t.__name__: t for t in tools}

messages = [{
    "role": "system",
    "content": "You are a helpful assistant. Use the tools when needed, "
               "and give a short final answer when you have what you need.",
}]

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in {"quit", "exit"}:
        break
    if not user_input:
        continue
    messages.append({"role": "user", "content": user_input})

    for step in range(MAX_STEPS):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=tools,
            options={"num_ctx": 4096, "temperature": 0},
        )
        messages.append(response.message)

        if not response.message.tool_calls:
            print("Agent:", response.message.content)
            break

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            print(f"  [step {step + 1}: calling {name} with {args}]")
            try:
                result = available[name](**args)
            except Exception as e:
                result = f"Error: {e}"
            messages.append({"role": "tool", "tool_name": name, "content": str(result)})
    else:
        print("Agent: stopped after reaching the step limit.")