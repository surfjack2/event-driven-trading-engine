import sys
import os

# src 디렉토리를 Python path에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI

# 기존 로그 API
from ltb.api.log_api import router as log_router

# 내부 문서 API
from ltb.api.docs_api import router as docs_router

# 운영 상태 API (OPS)
from ltb.api.routes.ops import router as ops_router


app = FastAPI(
    title="LTB Admin Console",
    description="LTB Management API",
    version="1.0"
)


# =========================
# Router 등록
# =========================

# 로그 조회 API
app.include_router(log_router)

# 내부 문서 조회 API
app.include_router(docs_router)

# 운영 상태 API
app.include_router(ops_router)


# =========================
# Root Endpoint
# =========================

@app.get("/")
def root():

    return {
        "service": "LTB Admin Console",
        "status": "running"
    }
