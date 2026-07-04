from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "PCBMind AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pcbmind"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"

    SECRET_KEY: str = "pcbmind-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""

    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GEMINI_MODEL: str = "gemini-2.0-flash"

    OCTOPART_API_KEY: str = ""
    MOUSER_API_KEY: str = ""
    DIGIKEY_CLIENT_ID: str = ""
    DIGIKEY_CLIENT_SECRET: str = ""

    STORAGE_PATH: str = "./storage"
    GENERATED_PATH: str = "./storage/generated"
    UPLOAD_PATH: str = "./storage/uploads"

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
