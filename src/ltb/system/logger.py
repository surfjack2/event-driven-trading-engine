import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "engine.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("ltb_engine")

logger.setLevel(logging.INFO)

# ===== 기존 handler 제거 (중복 방지 핵심) =====
if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.propagate = False
