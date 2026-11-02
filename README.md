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