from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlmodel import Session

from app.core.db import get_session
from app.core.auth import get_active_user
from app.models.schemas import ReportRead
from app.models.report import Report
from app.services.ocr import run_ocr
from app.services.nlp import extract_entities

router = APIRouter(prefix="/api", tags=["reports"])

@router.get("/health", tags=["infra"])
async def health_check():
    return {"status": "ok"}

@router.post("/reports/upload", response_model=ReportRead)
async def upload_report(
    file: UploadFile = File(...),
    nlp_method: Literal["transformer", "spacy"] = Query("transformer"),
    current_user=Depends(get_active_user),
    session: Session = Depends(get_session),
):
    ct = file.content_type
    if ct not in ("application/pdf", "image/png", "image/jpeg"):
        raise HTTPException(status_code=415, detail="Unsupported file type")
    contents = await file.read()

    text = run_ocr(contents, ct)
    entities = extract_entities(text, method=nlp_method)

    rpt = Report(
        filename=file.filename,
        content_type=ct,
        text=text,
        entities=entities,
        owner_id=current_user.id,
    )
    session.add(rpt)
    session.commit()
    session.refresh(rpt)
    return rpt