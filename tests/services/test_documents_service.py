import asyncio
from io import BytesIO
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, UploadFile
from pypdf.errors import PdfReadError
from starlette.datastructures import Headers

from university_knowledge_assistant.services import documents as documents_service


def create_upload_file(
    content: bytes = b"test content",
    content_type: str = "application/pdf",
) -> UploadFile:
    return UploadFile(
        file=BytesIO(content),
        filename="test.pdf",
        headers=Headers({"content-type": content_type}),
    )


def test_process_pdf_returns_extracted_text(monkeypatch):
    # Arrange
    file = create_upload_file()

    fake_pages = [
        SimpleNamespace(extract_text=lambda: "First page"),
        SimpleNamespace(extract_text=lambda: "Second page"),
    ]

    fake_reader = SimpleNamespace(pages=fake_pages)

    monkeypatch.setattr(
        documents_service,
        "PdfReader",
        lambda pdf_stream: fake_reader,
    )

    # Act
    result = asyncio.run(documents_service.process_pdf(file))

    # Assert
    assert result == ["First page", "Second page"]


def test_process_pdf_preserves_pages_without_text(monkeypatch):
    # Arrange
    file = create_upload_file()

    fake_pages = [
        SimpleNamespace(extract_text=lambda: "First page"),
        SimpleNamespace(extract_text=lambda: None),
        SimpleNamespace(extract_text=lambda: "Third page"),
    ]

    fake_reader = SimpleNamespace(pages=fake_pages)

    monkeypatch.setattr(
        documents_service,
        "PdfReader",
        lambda pdf_stream: fake_reader,
    )

    # Act
    result = asyncio.run(documents_service.process_pdf(file))

    # Assert
    assert result == ["First page", "", "Third page"]


def test_process_pdf_rejects_non_pdf_file():
    # Arrange
    file = create_upload_file(
        content=b"plain text",
        content_type="text/plain",
    )

    # Act
    with pytest.raises(HTTPException) as exception:
        asyncio.run(documents_service.process_pdf(file))

    # Assert
    assert exception.value.status_code == 415
    assert exception.value.detail == "Only PDF files are allowed."


def test_process_pdf_rejects_invalid_pdf(monkeypatch):
    # Arrange
    file = create_upload_file(content=b"invalid PDF content")

    def raise_pdf_read_error(pdf_stream):
        raise PdfReadError("Invalid PDF")

    monkeypatch.setattr(
        documents_service,
        "PdfReader",
        raise_pdf_read_error,
    )

    # Act
    with pytest.raises(HTTPException) as exception:
        asyncio.run(documents_service.process_pdf(file))

    # Assert
    assert exception.value.status_code == 400
    assert exception.value.detail == "The uploaded file is not a valid PDF."


def test_process_pdf_rejects_pdf_without_extractable_text(monkeypatch):
    # Arrange
    file = create_upload_file()

    fake_pages = [
        SimpleNamespace(extract_text=lambda: None),
        SimpleNamespace(extract_text=lambda: ""),
        SimpleNamespace(extract_text=lambda: "   "),
    ]

    fake_reader = SimpleNamespace(pages=fake_pages)

    monkeypatch.setattr(
        documents_service,
        "PdfReader",
        lambda pdf_stream: fake_reader,
    )

    # Act
    with pytest.raises(HTTPException) as exception:
        asyncio.run(documents_service.process_pdf(file))

    # Assert
    assert exception.value.status_code == 422
    assert (
        exception.value.detail
        == "The PDF does not contain extractable text."
    )