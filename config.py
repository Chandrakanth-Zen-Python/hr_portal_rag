import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    load_dotenv = None


if load_dotenv:
    load_dotenv()


@dataclass(frozen=True)
class Settings:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_access_key_id: str | None = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")

    embeddings_model: str = os.getenv(
        "BEDROCK_EMBEDDINGS_MODEL", "amazon.titan-embed-text-v1"
    )
    llm_model: str = os.getenv(
        "BEDROCK_LLM_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0"
    )

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "hr_portal")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    similarity_top_k: int = int(os.getenv("SIMILARITY_TOP_K", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1024"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))


settings = Settings()
