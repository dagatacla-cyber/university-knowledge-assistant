from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile, status

from university_knowledge_assistant.services.search import search_document_service

search_router = APIRouter()


@search_router.post(
    "/search",
    status_code=status.HTTP_200_OK,
)
async def upload_document(
    file: Annotated[UploadFile, File()],
    query: Annotated[str, Form()],
):
    results = await search_document_service(file, query)
    return {
        "query": query,
        "results": results,
    }
