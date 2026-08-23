from fastapi import FastAPI
from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="An enterprise AI knowledge assistant",
    version=settings.app_version,
)

app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running!"
    }
app.include_router(documents_router)