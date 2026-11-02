import ollama

response = ollama.chat(
    model="llama3.2:3b",   # must match a name from `ollama list`
    messages=[
        {"role": "user", "content": "you are a concise tutor answer in 50 words"},
        {"role": "user", "content": "Explain recursion to a first-year CS student."}],
    options={"num_predict": 100}
)

print(response["message"]["content"])
print("Input tokens:", response["prompt_eval_count"])
print("Output tokens:", response["eval_count"])