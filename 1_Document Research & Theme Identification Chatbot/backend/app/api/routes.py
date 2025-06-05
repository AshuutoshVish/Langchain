from fastapi import APIRouter, UploadFile, File
from app.services.document_processor import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    text = await process_document(file)
    return {"filename": file.filename, "extracted_text": text[:500]}  # return a preview
