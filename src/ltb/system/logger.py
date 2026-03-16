import logging
import os
import sys
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = "engine.log"

MAX_LOG_SIZE = 10 * 1024 * 1024
BACKUP_COUNT = 5


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


log_path = os.path.join(LOG_DIR, LOG_FILE)


logger = logging.getLogger("LTB")
logger.setLevel(logging.INFO)

logger.propagate = False


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)


# -----------------------------
# FILE LOG
# -----------------------------

file_handler = RotatingFileHandler(
    log_path,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# -----------------------------
# CONSOLE LOG SWITCH
# -----------------------------

def enable_console_logging():

    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
