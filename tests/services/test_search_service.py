import pytest

from university_knowledge_assistant.services import search as search_service


def test_normalize_text_removes_extra_whitespace_and_ignores_case():
    # Arrange
    text = "  Hello   WORLD\nPython  "

    # Act
    result = search_service.normalize_text(text)

    # Assert
    assert result == "hello world python"


def test_find_occurrence_positions_returns_all_positions():
    # Arrange
    text = "test text test"
    query = "test"

    # Act
    result = search_service.find_occurrence_positions(text, query)

    # Assert
    assert result == [0, 10]


def test_find_occurrence_positions_returns_empty_list_when_query_is_missing():
    # Arrange
    text = "test text"

    # Act
    result = search_service.find_occurrence_positions(text, "")

    # Assert
    assert result == []


def test_find_occurrence_positions_returns_empty_list_when_query_is_not_found():
    # Arrange
    text = "university notes"
    query = "python"

    # Act
    result = search_service.find_occurrence_positions(text, query)

    # Assert
    assert result == []


def test_find_occurrence_positions_finds_overlapping_occurrences():
    # Arrange
    text = "aaaa"
    query = "aa"

    # Act
    result = search_service.find_occurrence_positions(text, query)

    # Assert
    assert result == [0, 1, 2]


def test_build_passage_returns_context_around_query():
    # Arrange
    text = "a" * 40 + "query" + "b" * 40
    position = 40
    query_length = len("query")

    # Act
    result = search_service.build_passage(
        text,
        query_length,
        position,
    )

    # Assert
    assert result == "a" * 30 + "query" + "b" * 30


def test_build_passage_does_not_exceed_start_of_text():
    # Arrange
    text = "query followed by some text"
    position = 0
    query_length = len("query")

    # Act
    result = search_service.build_passage(
        text,
        query_length,
        position,
    )

    # Assert
    assert result == text


def test_build_passage_does_not_exceed_end_of_text():
    # Arrange
    text = "some text before query"
    position = text.find("query")
    query_length = len("query")

    # Act
    result = search_service.build_passage(
        text,
        query_length,
        position,
    )

    # Assert
    assert result == text


@pytest.mark.asyncio
async def test_search_document_service_returns_results_by_page(monkeypatch):
    # Arrange
    async def fake_process_pdf(file):
        return [
            "Python is useful. Python is popular.",
            "This page does not contain the query.",
            "Learning PYTHON is useful.",
        ]

    monkeypatch.setattr(
        search_service,
        "process_pdf",
        fake_process_pdf,
    )

    fake_file = object()

    # Act
    result = await search_service.search_document_service(
        fake_file,
        "python",
    )

    # Assert
    assert result == [
        {
            "page": 1,
            "occurrence_count": 2,
            "occurrences": [
                {
                    "position": 0,
                    "passage": "python is useful. python is popular.",
                },
                {
                    "position": 18,
                    "passage": "python is useful. python is popular.",
                },
            ],
        },
        {
            "page": 3,
            "occurrence_count": 1,
            "occurrences": [
                {
                    "position": 9,
                    "passage": "learning python is useful.",
                }
            ],
        },
    ]


@pytest.mark.asyncio
async def test_search_document_service_ignores_case_and_extra_whitespace(
    monkeypatch,
):
    # Arrange
    async def fake_process_pdf(file):
        return ["University   Knowledge\nAssistant"]

    monkeypatch.setattr(
        search_service,
        "process_pdf",
        fake_process_pdf,
    )

    fake_file = object()

    # Act
    result = await search_service.search_document_service(
        fake_file,
        "KNOWLEDGE assistant",
    )

    # Assert
    assert result == [
        {
            "page": 1,
            "occurrence_count": 1,
            "occurrences": [
                {
                    "position": 11,
                    "passage": "university knowledge assistant",
                }
            ],
        }
    ]


@pytest.mark.asyncio
async def test_search_document_service_returns_empty_list_when_query_is_not_found(
    monkeypatch,
):
    # Arrange
    async def fake_process_pdf(file):
        return [
            "First page",
            "Second page",
        ]

    monkeypatch.setattr(
        search_service,
        "process_pdf",
        fake_process_pdf,
    )

    fake_file = object()

    # Act
    result = await search_service.search_document_service(
        fake_file,
        "python",
    )

    # Assert
    assert result == []


@pytest.mark.asyncio
async def test_search_document_service_returns_empty_list_for_empty_query(
    monkeypatch,
):
    # Arrange
    async def fake_process_pdf(file):
        return ["Some text"]

    monkeypatch.setattr(
        search_service,
        "process_pdf",
        fake_process_pdf,
    )

    fake_file = object()

    # Act
    result = await search_service.search_document_service(
        fake_file,
        "",
    )

    # Assert
    assert result == []
