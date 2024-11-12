from pydantic_settings import BaseSettings
from typing import Dict
from pathlib import Path

class TextPaths(BaseSettings):
    raw_path: Path
    processed_path: Path | None = None
    query_path: Path | None = None

class PreprocessingSettings(BaseSettings):
    strategy: str = "sentence"
    chunk_size: int = 4
    chunk_overlap: int = 1
    include_context_header: bool = True

class EmbeddingSettings(BaseSettings):
    api_model: str = "text-embedding-3-small"
    dimension: int = 1536

    class Config:
        protected_namespaces = ('settings_',)

class LLMSettings(BaseSettings):
    model: str = "gpt-4o-mini"
    temperature: float = 0
    max_tokens: int = 2000

    class Config:
        protected_namespaces = ('settings_',)

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str

    # LLM settings
    llm: LLMSettings = LLMSettings()
    
    # Preprocessing settings
    preprocessing: PreprocessingSettings = PreprocessingSettings()
    
    # Embedding settings
    embeddings: EmbeddingSettings = EmbeddingSettings()
    
    # Text paths
    texts: Dict[str, TextPaths] = {
        "dalloway": TextPaths(
            raw_path="data/raw/mrs_dalloway.txt",
            query_path="data/processed/mrs_dalloway_queries.jsonl"
        ),
        "odyssey": TextPaths(
            raw_path="data/raw/odyssey_butcher.txt",
            processed_path="data/processed/odyssey_processed.jsonl"
        )
    }

    # Storage settings
    storage: Dict[str, Path] = {
        "persist_dir": Path("data/persisted"),
        "embeddings_dir": Path("data/persisted/embeddings")
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

# Create a global settings instance
settings = Settings()
