from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/ops")
def ops_page():

    return FileResponse(
        "web/ui/ops/ops_guide.html"
    )
