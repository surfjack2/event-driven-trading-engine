import sys
import os

# src 디렉토리를 Python path에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI

from ltb.api.log_api import router as log_router
from ltb.api.docs_api import router as docs_router


app = FastAPI(
    title="LTB Admin Console",
    description="LTB Management API",
    version="1.0"
)

# 기존 로그 API
app.include_router(log_router)

# 내부 운영 문서 API
app.include_router(docs_router)


@app.get("/")
def root():
    return {
        "service": "LTB Admin Console",
        "status": "running"
    }
