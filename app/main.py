from fastapi import FastAPI
from app.routers.health import health_router
from app.routers.documents import documents_router

app = FastAPI(
    title="University Knowledge Assistant",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(documents_router)