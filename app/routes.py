from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
import os
import shutil
from app.rag_pipeline import process_document, run_query

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = process_document(file_path)
        return {"message": "Document processed", "chunks": result["chunks"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

@router.get("/search")
async def search_query(q: str = Query(..., min_length=3)):
    try:
        answer = run_query(q)
        return {"query": q, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {e}")
