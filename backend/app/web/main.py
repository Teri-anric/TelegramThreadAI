"""
Main module for the backend.
"""

from fastapi import FastAPI

from .api import api_router

app = FastAPI(
    title="TelegramThreadAI",
    description="AI-enhanced Telegram threads platform",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    """
    Healthcheck endpoint to check if the server is running
    """
    return {"status": "ok"}
