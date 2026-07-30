from io import BytesIO

from fastapi.testclient import TestClient

from university_knowledge_assistant.main import app
from university_knowledge_assistant.routers import documents as documents_router


client = TestClient(app)


def test_upload_document_returns_201(monkeypatch):
    # Arrange
    async def fake_process_pdf(file):
        return ["Page 1"]

    monkeypatch.setattr(
        documents_router,
        "process_pdf",
        fake_process_pdf,
    )

    files = {
        "file": (
            "test.pdf",
            BytesIO(b"fake pdf"),
            "application/pdf",
        )
    }

    # Act
    response = client.post("/documents", files=files)

    # Assert
    assert response.status_code == 201
    assert response.json() == {
        "message": "PDF uploaded and processed successfully."
    }