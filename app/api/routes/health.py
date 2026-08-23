from fastapi import APIRouter

from app.core.config import settings


router = APIRouter(
    prefix="",
    tags=["Health"],
)


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.app_version,
    }