from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import get_settings
from .ingest import load_and_split
from .qa import answer
from .vectorstore import add_documents

app = FastAPI(title="Agentic Chat System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)) -> dict:
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / file.filename
    dest.write_bytes(await file.read())
    try:
        chunks = load_and_split(dest)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse {file.filename}: {e}")
    if not chunks:
        raise HTTPException(status_code=400, detail="No extractable content")
    ids = add_documents(chunks, source=file.filename)
    return {"filename": file.filename, "chunks": len(chunks), "ids": ids[:5]}


@app.post("/chat", response_model=ChatResponse)
def chat(q: Question) -> ChatResponse:
    result = answer(q.question)
    return ChatResponse(**result)