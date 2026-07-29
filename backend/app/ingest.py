from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import get_settings


def load_and_split(file_path: str | Path) -> list:
    path = Path(file_path)
    suffix = path.suffix.lower()
    loader = PyPDFLoader(str(path)) if suffix == ".pdf" else TextLoader(str(path), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=get_settings().chunk_size,
        chunk_overlap=get_settings().chunk_overlap,
    )
    return splitter.split_documents(docs)