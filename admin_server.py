import sys
import os

# src 디렉토리를 Python path에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI
from ltb.api.log_api import router as log_router


app = FastAPI(
    title="LTB Admin Console",
    description="LTB Management API",
    version="1.0"
)

app.include_router(log_router)


@app.get("/")
def root():
    return {
        "service": "LTB Admin Console",
        "status": "running"
    }
