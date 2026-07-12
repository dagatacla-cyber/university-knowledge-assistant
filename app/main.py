from fastapi import FastAPI
from app.routers.health import router

app = FastAPI(
    title="University Knowledge Assistant",
    version="0.1.0",
)


app.include_router(router)