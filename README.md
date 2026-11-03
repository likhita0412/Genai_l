<<<<<<< HEAD
# GenAI Learning - Week 1

Beginner projects using local LLMs with Ollama and Python.
 
## Projects
- `call_one.py`: first call to a local model and token counts
- `chatbot.py`: streaming chatbot with memory, `/reset` and `/save` commands
- `json_test.py`: structured JSON output

## Setup
1. Install Ollama and run `ollama pull llama3.2:3b`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install ollama`
4. `python chatbot.py`

## What I learned
- LLM APIs are stateless; memory is just resending the history
- Temperature and token limits change output behavior
- JSON mode helps, but outputs still need validation
=======
# Genai_l
>>>>>>> d55c618d5383cce28fc04e2ff0078fc80882c01c

#Week 2 notes
## Week 2 notes

I compared four prompting techniques on the same quiz-generation task using llama3.2:3b.
[Technique that worked best] gave the best results because [what you observed, e.g. it
followed the format exactly]. The vague prompt [what went wrong, e.g. returned a random
number of questions with no answers marked]. I also found that [one surprise, e.g. the
model added a fact that wasn't in the text, so "based only on the text" matters].

## Week 3 notes

Built a RAG Q&A tool over my notes with Ollama embeddings and Chroma. My first version put the
whole file into one chunk, and the model failed to answer. Splitting the notes into smaller
chunks fixed it, so chunking matters as much as the model. The "answer only from the notes"
rule works most of the time, but small models don't always follow it.