# Mani — Omega financial assistant

A financial-advisor chatbot built with [LlamaIndex](https://www.llamaindex.ai/). The **Omega**
Streamlit app answers questions about stocks, funds and budgeting using a ReAct agent that can
pull live data via the Yahoo Finance tools.

> General information only — not personalised financial advice.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
streamlit run src/app.py
```

## Files

- `src/app.py` — the Omega chat app.
- `loading.py` — helper to load a folder of documents into a vector index (`.granignore` lists
  files to skip).
- `rnd.ipynb` — exploratory notebook (reading a mutual-fund PDF into an index).
