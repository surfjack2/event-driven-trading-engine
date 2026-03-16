import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = "engine.log"

# 로그 파일 최대 크기 (10MB)
MAX_LOG_SIZE = 10 * 1024 * 1024

# 로그 파일 최대 보관 개수
BACKUP_COUNT = 5


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


log_path = os.path.join(LOG_DIR, LOG_FILE)


logger = logging.getLogger("LTB")

logger.setLevel(logging.INFO)

# 다른 logger로 전파 방지
logger.propagate = False


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)


# 파일 로그 (로테이션 적용)
file_handler = RotatingFileHandler(
    log_path,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT
)

file_handler.setFormatter(formatter)


# 🔴 콘솔 핸들러 제거
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)


logger.addHandler(file_handler)
