import re # pattern match
import glob # find files
import os 
import ollama
import chromadb

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:3b"
ENTRY = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]\s*(.+)$", re.S)

# 1. Load every file, keep the date and source with each entry
docs, metas = [], []
for path in sorted(glob.glob("case_files/*.txt")): #return
    source = os.path.basename(path)
    with open(path) as f:
        for entry in f.read().split("\n\n"):
            m = ENTRY.match(entry.strip())
            if not m:
                continue
            docs.append(m.group(2).strip())
            metas.append({"source": source, "date": m.group(1)})

print(f"Loaded {len(docs)} entries from {len(set(m['source'] for m in metas))} files")

# 2. Embed and store
embeddings = ollama.embed(model=EMBED_MODEL, input=docs)["embeddings"]
collection = chromadb.Client().create_collection("case")
collection.add(
    ids=[str(i) for i in range(len(docs))],
    documents=docs,
    embeddings=embeddings,
    metadatas=metas,
)

# 3. Ask questions
while True:
    question = input("\nInvestigator question (or quit): ").strip()
    if question.lower() in {"quit", "exit"}:
        break
    if not question:
        continue

    if question == "/timeline":
        for m, d in sorted(zip(metas, docs), key=lambda p: p[0]["date"]): #label pairing
            print(f"[{m['date']} | {m['source']}] {d}")
        continue

    q = ollama.embed(model=EMBED_MODEL, input=question)["embeddings"][0]
    results = collection.query(query_embeddings=[q], n_results=min(6, len(docs)))

    # Sort the evidence by time in Python, not by the model
    evidence = sorted(
        zip(results["metadatas"][0], results["documents"][0]),
        key=lambda pair: pair[0]["date"],
    )
    context = "\n".join(f"[{m['date']} | {m['source']}] {d}" for m, d in evidence)

    prompt = (
        "You are assisting a fictional case review. Use ONLY the evidence below, "
        "which is in chronological order.\n"
        "1. Answer the question, citing each fact as [date | source].\n"
        "2. List any contradictions between statements and records, quoting both sides.\n"
        "3. If the evidence is not enough, say \"Not enough evidence.\"\n\n"
        f"Evidence:\n{context}\n\nQuestion: {question}"
    )

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0, "num_ctx": 4096, "num_predict": 400},
    )
    print("\n--- EVIDENCE USED ---\n" + context)
    print("\n--- ANSWER ---\n" + response["message"]["content"])