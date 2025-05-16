# app/main.py
from fastapi import FastAPI
from sqlalchemy import Engine
from app.api.router import router as api_router
from sqlmodel import SQLModel
from app.api.auth import router as auth_router
from app.core.config import engine  

SQLModel.metadata.create_all(engine)

app = FastAPI(title="MedAIV Backend")
app.include_router(api_router)
app.include_router(auth_router)  