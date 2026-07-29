from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from .config import get_settings


def get_vectorstore() -> Chroma:
    settings = get_settings()
    embeddings = OpenAIEmbeddings(model=settings.embed_model, api_key=settings.openai_api_key)
    return Chroma(
        collection_name="agentic_chat",
        embedding_function=embeddings,
        persist_directory=settings.chroma_dir,
    )


def add_documents(chunks: list[Document], source: str) -> list[str]:
    vs = get_vectorstore()
    ids = vs.add_documents(chunks, metadatas=[{"source": source}] * len(chunks))
    return ids


def similarity_search(query: str, k: int | None = None) -> list[Document]:
    vs = get_vectorstore()
    return vs.similarity_search(query, k=k or get_settings().top_k)