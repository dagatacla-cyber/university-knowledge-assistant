from typing import TypedDict

from fastapi import UploadFile

from university_knowledge_assistant.services.documents import process_pdf


class OccurrenceResult(TypedDict):
    position: int
    passage: str


class PageSearchResult(TypedDict):
    page: int
    occurrence_count: int
    occurrences: list[OccurrenceResult]


def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and ignoring letter case."""
    return " ".join(text.casefold().split())


def find_occurrence_positions(text: str, query: str) -> list[int]:
    """Return the starting positions of all query occurrences in the text."""
    if not query:
        return []

    positions: list[int] = []
    position = text.find(query)

    while position != -1:
        positions.append(position)
        position = text.find(query, position + 1)

    return positions


def build_passage(
    text: str,
    query_length: int,
    position: int,
) -> str:
    """Return the text passage containing the query."""
    start = max(0, position - 30)
    end = min(len(text), position + query_length + 30)
    return text[start:end]


async def search_document_service(
    file: UploadFile,
    query: str,
) -> list[PageSearchResult]:
    """Search for a query across all pages of an uploaded PDF document."""
    pages = await process_pdf(file)
    results: list[PageSearchResult] = []
    normalized_query = normalize_text(query)
    query_length = len(normalized_query)

    for page_number, page_text in enumerate(pages, start=1):
        normalized_page_text = normalize_text(page_text)
        positions = find_occurrence_positions(normalized_page_text, normalized_query)

        if positions:
            occurrences: list[OccurrenceResult] = []
            for position in positions:
                passage = build_passage(normalized_page_text, query_length, position)
                occurrence_result: OccurrenceResult = {
                    "position": position,
                    "passage": passage,
                }
                occurrences.append(occurrence_result)
                

            results.append(
                {
                    "page": page_number,
                    "occurrence_count": len(occurrences),
                    "occurrences": occurrences,
                }
            )

    return results

