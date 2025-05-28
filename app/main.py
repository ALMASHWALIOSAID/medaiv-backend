from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.db import engine
from app.api.router import router as api_router  # ✅ important
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

def on_startup():
    SQLModel.metadata.create_all(engine)

# ✅ Include the router with /api prefix
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
