# app/services/ocr.py

import io
import os
from typing import List
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

# Allow configuration via ENV for portability
TESSERACT_CMD = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows default
)
POPLER_PATH = os.getenv(
    "POPPLER_PATH",
    r"C:\Program Files\poppler-24.08.0\Library\bin"  # Windows default
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def run_ocr_on_image_bytes(img_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(img)

def run_ocr(file_bytes: bytes, content_type: str) -> str:
    """
    If PDF: convert each page to an image via pdf2image + Poppler,
    otherwise run OCR directly on the image bytes.
    """
    if content_type == "application/pdf":
        pages = convert_from_bytes(
            file_bytes,
            poppler_path=POPLER_PATH
        )
        texts: List[str] = []
        for page in pages:
            buf = io.BytesIO()
            page.save(buf, format="PNG")
            texts.append(pytesseract.image_to_string(Image.open(buf)))
        return "\n\n---PAGE BREAK---\n\n".join(texts)
    else:
        return run_ocr_on_image_bytes(file_bytes)
