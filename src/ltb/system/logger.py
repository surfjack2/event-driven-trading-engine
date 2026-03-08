import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "engine.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("ltb_engine")

logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

# 파일 로그
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

# 콘솔 로그 (docker logs용)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False
