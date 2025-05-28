# tests/test_ocr.py

import os
import sys
from fpdf import FPDF

# ensure project root is on sys.path so "app" can be imported
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

import io
import pytest
from app.services.ocr import run_ocr

def test_run_ocr_plain_text():
    data = b"Just some text"
    out = run_ocr(data, "text/plain")
    assert out == "Just some text"

def test_run_ocr_unsupported():
    with pytest.raises(RuntimeError, match="Unhandled content type"):
        run_ocr(b"", "application/zip")
def test_run_ocr_pdf(tmp_path):
    from fpdf import FPDF
    pdf_path = tmp_path / "text.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello OCR!", ln=True)
    pdf.output(str(pdf_path))

    contents = pdf_path.read_bytes()
    result = run_ocr(contents, "application/pdf")
    assert "Hello OCR" in result

def test_run_ocr_image(tmp_path, monkeypatch):
    # mock PIL and pytesseract pipeline
    from PIL import Image
    import pytesseract

    fake_img = Image.new("RGB", (10, 10), color="white")
    monkeypatch.setattr(pytesseract, "image_to_string", lambda im: "OCRd")
    data = io.BytesIO()
    fake_img.save(data, format="PNG")
    data = data.getvalue()

    assert run_ocr(data, "image/png") == "OCRd"

