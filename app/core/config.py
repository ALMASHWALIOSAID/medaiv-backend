import os
from functools import lru_cache
from sqlmodel import create_engine

class Settings:
    OCR_LANG: str = os.getenv("OCR_LANG", "eng")
    MODEL_NAME: str = os.getenv("SPACY_MODEL", "en_core_web_sm")

    # ← Add this line:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./medaiv.db")

    # (if you’ve also added auth:)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme-supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Now this works because Settings has DATABASE_URL
settings = get_settings()
engine = create_engine(settings.DATABASE_URL, echo=True)
