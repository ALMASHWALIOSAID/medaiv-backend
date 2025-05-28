# app/core/config.py

import os
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    # your required settings
    DATABASE_URL: str = "sqlite:///./test.db"
    SQLALCHEMY_ECHO: bool = False
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# convenient module‐level singleton
settings = get_settings()