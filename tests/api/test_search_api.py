from io import BytesIO

from fastapi.testclient import TestClient

from university_knowledge_assistant.main import app
from university_knowledge_assistant.routers import search as search_router


client = TestClient(app)


def test_search_document_returns_results(monkeypatch):
    # Arrange
    async def fake_search_document_service(file, query):
        return [
            {
                "page": 1,
                "occurrence_count": 1,
                "occurrences": [
                    {
                        "position": 0,
                        "passage": "python is useful",
                    }
                ],
            }
        ]

    monkeypatch.setattr(
        search_router,
        "search_document_service",
        fake_search_document_service,
    )

    files = {
        "file": (
            "test.pdf",
            BytesIO(b"fake pdf"),
            "application/pdf",
        )
    }

    data = {
        "query": "python",
    }

    # Act
    response = client.post(
        "/search",
        files=files,
        data=data,
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "query": "python",
        "results": [
            {
                "page": 1,
                "occurrence_count": 1,
                "occurrences": [
                    {
                        "position": 0,
                        "passage": "python is useful",
                    }
                ],
            }
        ],
    }


def test_search_document_returns_empty_results(monkeypatch):
    # Arrange
    async def fake_search_document_service(file, query):
        return []

    monkeypatch.setattr(
        search_router,
        "search_document_service",
        fake_search_document_service,
    )

    files = {
        "file": (
            "test.pdf",
            BytesIO(b"fake pdf"),
            "application/pdf",
        )
    }

    data = {
        "query": "missing",
    }

    # Act
    response = client.post(
        "/search",
        files=files,
        data=data,
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "query": "missing",
        "results": [],
    }


def test_search_document_requires_file():
    # Arrange
    data = {
        "query": "python",
    }

    # Act
    response = client.post(
        "/search",
        data=data,
    )

    # Assert
    assert response.status_code == 422


def test_search_document_requires_query():
    # Arrange
    files = {
        "file": (
            "test.pdf",
            BytesIO(b"fake pdf"),
            "application/pdf",
        )
    }

    # Act
    response = client.post(
        "/search",
        files=files,
    )

    # Assert
    assert response.status_code == 422