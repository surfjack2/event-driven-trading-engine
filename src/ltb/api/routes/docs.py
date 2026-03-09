from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import markdown
import pathlib

router = APIRouter()

DOC_PATH = pathlib.Path("docs/operations")


@router.get("/docs/operations/logs", response_class=HTMLResponse)
def log_inspection():

    file = DOC_PATH / "log_inspection.md"

    if not file.exists():
        return "<h1>Document not found</h1>"

    text = file.read_text()

    html = markdown.markdown(text)

    return f"""
    <html>
    <body style="font-family: monospace; padding:40px;">
    {html}
    </body>
    </html>
    """
