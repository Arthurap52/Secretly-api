import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./secretly.db"
    )
    enable_docs: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()