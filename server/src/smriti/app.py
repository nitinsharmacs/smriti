from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import create_api_router


def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://localhost:8081",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(create_api_router())

    @app.get("/health")
    async def health():
        return {"health": "ok"}

    return app
