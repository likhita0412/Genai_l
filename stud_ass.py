import sys
import ollama

MODEL = "llama3.2:3b"

def ask(prompt, system="You are a helpful CS tutor. Use only the notes provided. Be concise."):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0.3, "num_predict": 500, "num_ctx": 4096},
    )
    return response["message"]["content"]

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "notes.txt"
    try:
        with open(filename) as f:
            notes = f.read()
    except FileNotFoundError:
        print(f"Could not find {filename}")
        return

    print("=== SUMMARY ===")
    print(ask(f"Summarize these notes in 5 bullet points.\n\nNotes:\n{notes}"))

    print("\n=== KEY TERMS ===")
    print(ask(
        "List the 5 most important terms from the notes, each with a one-sentence definition. "
        "Format: Term: definition\n\n"
        f"Notes:\n{notes}"
    ))

    print("\n=== QUIZ ===")
    print(ask(
        "Write 3 multiple-choice questions based only on the notes. "
        "Give options A-D and state the correct answer after each question.\n\n"
        f"Notes:\n{notes}"
    ))

main()