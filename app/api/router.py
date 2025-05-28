# app/api/router.py
from fastapi import APIRouter
from app.api import auth, reports

router = APIRouter(prefix="/api")

@router.get("/health", tags=["infra"])
async def health_check():
    return {"status": "ok"}

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(reports.router, prefix="/reports")
