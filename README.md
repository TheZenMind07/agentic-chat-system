# agentic-chat-system

RAG chat over your documents: upload PDFs/text, ask questions, get cited answers.

## Stack

- **Backend**: FastAPI, LangChain, ChromaDB (local), OpenAI embeddings + chat
- **Frontend**: React + Vite

## Quick start

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

Vite proxies `/api/*` → `http://localhost:8000`.

## API

| Method | Path     | Purpose                                |
|--------|----------|----------------------------------------|
| GET    | /health  | health check                           |
| POST   | /ingest  | multipart upload (`.pdf` / `.txt`)     |
| POST   | /chat    | JSON `{question}` → `{answer, sources}`|

## Layout

```
agentic-chat-system/
├── backend/           FastAPI + LangChain
│   ├── app/
│   │   ├── main.py        FastAPI routes
│   │   ├── config.py      env-driven settings
│   │   ├── ingest.py      load + split
│   │   ├── vectorstore.py Chroma wrapper
│   │   └── qa.py          retrieval + LLM
│   └── requirements.txt
├── frontend/          React + Vite
│   └── src/
│       ├── App.jsx
│       └── main.jsx
└── data/              Chroma persistence + uploads (gitignored)
```