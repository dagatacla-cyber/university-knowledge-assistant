from fastapi import HTTPException, UploadFile, status
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from io import BytesIO

async def process_pdf(file: UploadFile) -> list[str]:
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

    # Extract text page by page
    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)
        else:
            pages.append("")

    # Check if any text was extracted
    if not any(page_text.strip() for page_text in pages):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="The PDF does not contain extractable text.",
        )

    return pages