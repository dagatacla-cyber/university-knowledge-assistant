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

### Next

* Text search

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


### Planned

* PostgreSQL
* Docker
* Automated testing
* CI/CD

---

## Project Structure

```text
app/
├── routers/
│   ├── documents.py
│   └── health.py
└── main.py

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
git clone <repository-url>
cd university-knowledge-assistant
```

### Install dependencies

```bash
uv sync
```

### Run the application

```bash
uv run uvicorn app.main:app --reload
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

## Available Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /health | Check the application status |
| POST | /documents | Upload, validate and process a PDF document |

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
* [ ] Text search
* [ ] Passage retrieval with page numbers
* [ ] Database integration
* [ ] Automated testing
* [ ] Docker
* [ ] CI/CD

---

## License

This project is released under the MIT License.
