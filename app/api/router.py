# app/api/router.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlmodel import Session
from app.services.ocr import run_ocr
from app.services.nlp import extract_entities
from app.models import Report
from app.core.db import get_session
from app.core.auth import get_active_user

router = APIRouter(prefix="/api")

@router.get("/health", tags=["infra"])
async def health_check():
    return {"status": "ok"}

@router.post("/reports/upload", response_model=Report, tags=["reports"])
async def upload_report(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user=Depends(get_active_user),
    nlp_method: str = Query("transformer", enum=["transformer", "spacy"])
):
    ct = file.content_type
    if ct not in ("application/pdf", "image/png", "image/jpeg"):
        raise HTTPException(status_code=415, detail="Unsupported file type")
    contents = await file.read()

    # OCR extraction
    text = run_ocr(contents, ct)
    # NER extraction using chosen method
    entities = extract_entities(text, method=nlp_method)

    # create & persist the report
    report = Report(
        filename=file.filename,
        content_type=ct,
        text=text,
        entities=entities,
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
