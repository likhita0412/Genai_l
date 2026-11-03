import ollama
import chromadb

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:3b"

# Load and chunk notes
with open("notes.txt") as f:
    text = f.read()

chunks = []
for para in text.split("\n\n"):
    para = para.strip()
    if not para:
        continue
    current = ""
    for line in para.split("\n"):
        if len(current) + len(line) > 500 and current:
            chunks.append(current.strip())
            current = ""
        current += line + "\n"
    if current.strip():
        chunks.append(current.strip())
print(f"Created {len(chunks)} chunks")

# Embed and store
embeddings = ollama.embed(model=EMBED_MODEL, input=chunks)["embeddings"]
client = chromadb.Client()
collection = client.create_collection("notes")
collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"source": "notes.txt", "chunk": i} for i in range(len(chunks))],
)

while True:
    question = input("\nQuestion (or quit): ").strip()
    if question.lower() in {"quit", "exit"}:
        break
    if not question:
        continue

    # Retrieve
    q_embedding = ollama.embed(model=EMBED_MODEL, input=question)["embeddings"][0]
    results = collection.query(query_embeddings=[q_embedding], n_results=min(2, len(chunks)))
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    # Build the prompt with the retrieved chunks
    context = "\n\n".join(f"[chunk {m['chunk']}] {d}" for d, m in zip(docs, metas))
    prompt = (
        "Answer the question using only the notes below. "
        "If the notes don't contain the answer, say \"That's not in my notes.\"\n\n"
        f"Notes:\n{context}\n\nQuestion: {question}"
    )

    # Generate
    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2, "num_predict": 300, "num_ctx": 4096},
    )
    print("\nAnswer:", response["message"]["content"])
    print("Sources:", ", ".join(f"chunk {m['chunk']}" for m in metas))