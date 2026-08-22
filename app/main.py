from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Assistant",
    description="An enterprise AI knowledge assistant",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Assistant is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
