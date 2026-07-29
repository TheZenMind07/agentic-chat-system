# agentic-chat-system

Customer-support chat with an agent orchestrator that routes to five specialized sub-agents (image retrieval, customer / driver / booking details, SOP RAG over ChromaDB).

See [`docs/plan.md`](docs/plan.md) for the full architecture and [`docs/images/architecture.png`](docs/images/architecture.png) for the diagram.

## Stack

- **Backend**: FastAPI (SSE streaming), LangChain, LangGraph (supervisor), ChromaDB, OpenAI (`gpt-4o-mini`)
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

| Method | Path | Purpose | Caller |
|---|---|---|---|
| GET | `/health` | health check | — |
| POST | `/chat` (SSE) | streamed customer chat | Chat UI |
| POST | `/ingest` (multipart) | admin uploads SOP / chat-context docs | Admin |

## Layout

```
agentic-chat-system/
├── backend/                     FastAPI + LangChain + LangGraph
│   ├── app/
│   │   ├── main.py              routes: /health, /chat (SSE), /ingest
│   │   ├── config.py            env settings
│   │   ├── ingest.py            SOP load + split
│   │   ├── vectorstore.py       Chroma wrapper
│   │   ├── vision.py            gpt-4o-mini vision extraction
│   │   ├── data/                mock JSON loaders
│   │   └── agents/              orchestrator + 5 sub-agents
│   └── requirements.txt
├── frontend/                    React + Vite
│   └── src/
│       ├── App.jsx
│       └── main.jsx
├── data/                        JSON fixtures + Chroma persistence (gitignored)
└── docs/                        plan.md, images/
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) — direct pushes to `main` are blocked; all changes go via PR.