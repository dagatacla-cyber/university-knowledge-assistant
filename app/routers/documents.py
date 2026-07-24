from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pypdf import PdfReader
from pypdf.errors import PdfReadError


documents_router = APIRouter()


@documents_router.post(
        "/documents",
        status_code=status.HTTP_201_CREATED,
        )
async def upload_document(file: UploadFile = File(...)):
    # Validate MIME type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are allowed.",
        )

    # Read uploaded file
    content = await file.read()

    # Create an in-memory binary stream
    pdf_stream = BytesIO(content)

    # Validate PDF structure
    try:
        reader = PdfReader(pdf_stream)
    except PdfReadError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid PDF.",
        )

    # Extract text
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # Check if any text was extracted
    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The PDF does not contain extractable text.",
        )

    # Return response
    return {
    "message": "PDF uploaded and processed successfully."
    }
