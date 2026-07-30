from fastapi import FastAPI
from university_knowledge_assistant.routers.health import health_router
from university_knowledge_assistant.routers.documents import documents_router
from university_knowledge_assistant.routers.search import search_router
app = FastAPI(
    title="University Knowledge Assistant",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(documents_router)
app.include_router(search_router)