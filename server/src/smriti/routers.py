from fastapi import APIRouter
from .upload.router import create_router as create_upload_router


def create_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")
    router.include_router(create_upload_router())
    return router
