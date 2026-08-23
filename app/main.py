from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="An enterprise AI knowledge assistant",
    version=settings.app_version,
)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.app_version,
    }