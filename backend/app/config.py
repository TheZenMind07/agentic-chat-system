from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str
    embed_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    chroma_dir: str = "../data/chroma"
    upload_dir: str = "../data/uploads"
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()