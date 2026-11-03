import ollama
import chromadb

EMBED_MODEL = "nomic-embed-text"

# 1. Load notes and split into chunks (one per paragraph)
with open("notes.txt") as f:
    text = f.read()
chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
print(f"Created {len(chunks)} chunks")

# 2. Turn every chunk into an embedding
embeddings = ollama.embed(model=EMBED_MODEL, input=chunks)["embeddings"]

# 3. Store them in a vector database (in memory)
client = chromadb.Client()
collection = client.create_collection("notes")
collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"source": "notes.txt", "chunk": i} for i in range(len(chunks))],
)

# 4. Ask questions and see which chunks match
while True:
    question = input("\nQuestion (or quit): ").strip()
    if question.lower() in {"quit", "exit"}:
        break
    q_embedding = ollama.embed(model=EMBED_MODEL, input=question)["embeddings"][0]
    results = collection.query(query_embeddings=[q_embedding], n_results=2)
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"\n[{meta['source']}, chunk {meta['chunk']}]")
        print(doc)