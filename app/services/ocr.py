import io
from typing import List
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

# point to tesseract.exe if needed:
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Poppler bin folder for pdf2image
POPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"

def run_ocr_on_image_bytes(img_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(img)

def run_ocr(file_bytes: bytes, content_type: str) -> str:
    if content_type == "application/pdf":
        # convert PDF to images using your Poppler installation
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
