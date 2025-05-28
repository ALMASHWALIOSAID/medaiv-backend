from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session, select
from fastapi import Request
from pydantic import BaseModel

from app.core.db import get_session
from app.core.auth import get_active_user
from app.models.schemas import ReportRead
from app.models.report import Report
from app.models.user import User
from app.services.ocr import run_ocr
from app.services.nlp import extract_entities

router = APIRouter(tags=["reports"])


class RequestEntity(BaseModel):
    text: str
    method: str = "spacy"  # or "transformer"


@router.post("/extract")
def extract_from_text(payload: RequestEntity):
    text = payload.text
    method = payload.method
    entities = extract_entities(text, method=method)
    return {"entities": entities}


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    current_user: User = Depends(get_active_user),
    session: Session = Depends(get_session),
):
    content_type = file.content_type
    if content_type not in ("application/pdf", "image/png", "image/jpeg", "text/plain"):
        raise HTTPException(status_code=415, detail="Unsupported file type")

    contents = await file.read()
    text = run_ocr(contents, content_type)
    entities = extract_entities(text)
    if not isinstance(entities, dict):
        entities = {}

    print("DEBUG ENTITIES TYPE:", type(entities), entities)
    report = Report(
        filename=file.filename,
        content_type=content_type,
        text=text,
        entities=entities,  # ✅ already a dict
        owner_id=current_user.id,
    )

    session.add(report)
    session.commit()
    session.refresh(report)
    return report


@router.get("/", response_model=List[ReportRead])
def list_reports(
    current_user: User = Depends(get_active_user),
    session: Session = Depends(get_session),
):
    reports = session.exec(
        select(Report).where(Report.owner_id == current_user.id)
    ).all()

    for rpt in reports:
        if not isinstance(rpt.entities, dict):
            rpt.entities = {}

    return reports


@router.get("/{report_id}", response_model=ReportRead)
def get_report(
    report_id: int,
    current_user: User = Depends(get_active_user),
    session: Session = Depends(get_session),
):
    rpt = session.get(Report, report_id)
    if not rpt or rpt.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Report not found")
    return rpt
