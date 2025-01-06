from fastapi import FastAPI
from .api import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    """
    Healthcheck endpoint to check if the server is running
    """
    return {"status": "ok"}
