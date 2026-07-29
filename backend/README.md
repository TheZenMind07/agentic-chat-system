# Backend

FastAPI + LangChain + ChromaDB + OpenAI.

## Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET  /health` — health check
- `POST /ingest` — multipart upload of `.pdf` or `.txt`; chunks & indexes
- `POST /chat` — JSON `{"question": "..."}` → `{answer, sources[]}`

## Notes

- ChromaDB persists to `../data/chroma/`
- Uploads stored under `../data/uploads/`
- Defaults: `text-embedding-3-small` (embeddings), `gpt-4o-mini` (chat), top_k=4