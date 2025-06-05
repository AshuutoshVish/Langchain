# OCR + PDF Text Extraction

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

async def process_document(file):
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(await file.read())
    elif file.content_type.startswith("image/"):
        return extract_text_from_image(await file.read())
    else:
        return "Unsupported file type"

def extract_text_from_pdf(file_bytes):
    text = ""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image)
