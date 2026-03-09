from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import markdown
import pathlib

router = APIRouter(
    prefix="/docs",
    tags=["internal-docs"]
)

DOC_ROOT = pathlib.Path("docs")


@router.get("/operations/logs", response_class=HTMLResponse)
def view_log_inspection():

    file = DOC_ROOT / "operations" / "log_inspection.md"

    if not file.exists():
        return "<h1>Document not found</h1>"

    text = file.read_text(encoding="utf-8")

    html = markdown.markdown(text)

    return f"""
    <html>
        <head>
            <title>LTB Operations Docs</title>
        </head>
        <body style="font-family: monospace; padding:40px;">
            {html}
        </body>
    </html>
    """
