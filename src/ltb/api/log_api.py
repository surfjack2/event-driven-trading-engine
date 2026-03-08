from fastapi import APIRouter
from ltb.system.log_manager import LogManager

router = APIRouter()

manager = LogManager()


@router.get("/logs")
def list_logs():
    return manager.list_logs()


@router.get("/logs/{log_name}")
def read_log(log_name: str):
    return manager.tail(log_name)
