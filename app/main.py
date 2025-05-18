from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.router import router as reports_router


def create_app() -> FastAPI:
    app = FastAPI(title="MedAIV Backend", version="0.1.0")
    app.include_router(auth_router)
    app.include_router(reports_router)
    return app


app = create_app()