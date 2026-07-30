# University Knowledge Assistant

University Knowledge Assistant is a backend application for uploading, searching and exploring university notes and documents.

The project is currently under active development as a personal portfolio project aimed at progressively applying modern backend development and software engineering practices.

---

## Project Goal

The long-term goal is to build a platform that allows students to:

* upload PDF documents;
* search text within PDF documents;
* retrieve relevant passages and page numbers;
* perform semantic searches;
* generate summaries, quizzes and flashcards;
* simulate oral examinations;
* track study progress;
* view citations and source references.

---

## Minimum Viable Product (MVP)

The first version of the application will provide:

* PDF upload;
* text search;
* passage retrieval;
* page number retrieval.

More advanced features will be introduced incrementally after the core backend functionality has been completed.

---

## Project Status

### Completed

* Initial FastAPI application
* Health-check endpoint
* PDF upload
* PDF validation
* Text extraction
* Text search
* Passage retrieval with page numbers
* Automated testing

### Next

* Static analysis

---

## Technology Stack

### Currently Used

* Python 3.12+
* FastAPI
* Uvicorn
* Pydantic
* pypdf
* python-multipart
* uv
* Git
* GitHub
* pytest
* httpx
* pytest-asyncio

### Planned

* Ruff (static analysis)
* GitHub Actions (Continuous Integration)
* PostgreSQL
* Docker
* Continuous Deployment

---

## Project Structure

```text
src/
└── university_knowledge_assistant/
    ├── __init__.py
    ├── main.py
    ├── routers/
    │   ├── __init__.py
    │   ├── documents.py
    │   ├── health.py
    │   └── search.py
    └── services/
        ├── __init__.py
        ├── documents.py
        └── search.py

tests/
├── api/
│   ├── test_documents_api.py
│   ├── test_health_api.py
│   └── test_search_api.py
└── services/
    ├── test_documents_service.py
    └── test_search_service.py

LICENSE
README.md
pyproject.toml
uv.lock
```

---

## Getting Started

### Requirements

* Python 3.12+
* uv

### Clone the repository

```bash
git clone git@github.com:dagatacla-cyber/university-knowledge-assistant.git
cd university-knowledge-assistant
```

### Install dependencies

```bash
uv sync
```
This command creates (or updates) the virtual environment, installs all project dependencies, and installs the application as an editable Python package.

### Run the application

```bash
uv run uvicorn university_knowledge_assistant.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

Run the complete test suite:

```bash
uv run pytest
```
Run the test suite with detailed output:
```bash
uv run pytest -v
```

---

## Available Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /health | Check the application status |
| POST | /documents | Upload, validate and process a PDF document |
| POST | /search | Search text within an uploaded PDF document |

---

## Development Workflow

The project follows a Git Flow-inspired branching strategy.

### Branches

* `main`
* `develop`
* `feature/*`

Features are developed in dedicated branches and merged into `develop` through Pull Requests.

---

## Roadmap

* [x] Initial FastAPI application
* [x] Health-check endpoint
* [x] PDF upload
* [x] PDF validation
* [x] Text extraction
* [x] Text search
* [x] Passage retrieval with page numbers
* [x] Automated testing
* [ ] Static analysis
* [ ] Continuous Integration with GitHub Actions
* [ ] Database integration
* [ ] Docker
* [ ] Continuous Deployment
---

## License

This project is released under the MIT License.
