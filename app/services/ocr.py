# app/services/ocr.py

import io
from typing import Union

from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import csv

def run_ocr(contents: bytes, content_type: str) -> str:
    if content_type == "text/plain":
        return contents.decode("utf-8", errors="ignore")

    if content_type == "text/csv":
        decoded = contents.decode("utf-8", errors="ignore").splitlines()
        reader = csv.reader(decoded)
        return "\n".join([", ".join(row) for row in reader])

    if content_type == "application/pdf":
        reader = PdfReader(io.BytesIO(contents))
        text_pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(text_pages)

    if content_type in ("image/png", "image/jpeg"):
        img = Image.open(io.BytesIO(contents))
        return pytesseract.image_to_string(img)

    raise RuntimeError(f"Unhandled content type: {content_type}")
