import ollama

MODEL = "llama3.2:3b"

def ask(prompt, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        options={"temperature": 0, "num_predict": 300},
    )
    return response["message"]["content"]

text = """Recursion is when a function calls itself to solve a smaller version
of the same problem. Every recursive function needs a base case that stops
the recursion, and a recursive case that moves toward the base case.
Without a base case, the function calls itself forever and causes a stack overflow."""

# 1. Vague prompt
print("=== 1. VAGUE ===")
print(ask(f"Make questions about this: {text}"))

# 2. Clear instructions
print("\n=== 2. CLEAR ===")
print(ask(f"Write exactly 3 multiple-choice questions based only on the text below. "
          f"Give 4 options (A-D) for each and mark the correct answer.\n\nText:\n{text}"))

# 3. Few-shot (give an example of the format)
print("\n=== 3. FEW-SHOT ===")
print(ask(
    "Write 3 quiz questions based only on the text below. Follow this format exactly:\n\n"
    "Q: What does a stack hold?\n"
    "A: Function calls waiting to finish.\n\n"
    f"Text:\n{text}"
))

# 4. Role + step by step
print("\n=== 4. ROLE + STEPS ===")
print(ask(
    f"First list the 3 most important ideas in the text. Then write one question for each idea.\n\nText:\n{text}",
    system="You are a university CS teacher writing exam questions. Be precise and concise.",
))