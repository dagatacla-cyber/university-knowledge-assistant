from fastapi import APIRouter, File, UploadFile, status
from university_knowledge_assistant.services.documents import process_pdf


documents_router = APIRouter()


@documents_router.post(
        "/documents",
        status_code=status.HTTP_201_CREATED,
        )
async def upload_document(file: UploadFile = File(...)):
    pages = await process_pdf(file)

    return {
    "message": "PDF uploaded and processed successfully."
    }
