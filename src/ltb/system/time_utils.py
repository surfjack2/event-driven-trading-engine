"""
LTB Time Utilities

엔진 전역에서 사용하는 시간 관련 유틸리티.
- timezone 통일
- 시장 세션 판단
- 시간 포맷
- 백테스트 확장 대비
"""

import time
from datetime import datetime, timezone, timedelta


# --------------------------------------------------
# TIMEZONE
# --------------------------------------------------

KST = timezone(timedelta(hours=9))


# --------------------------------------------------
# BASIC TIME
# --------------------------------------------------

def now_ts():
    """
    현재 timestamp 반환
    """
    return time.time()


def now_dt():
    """
    timezone-aware datetime
    """
    return datetime.now(KST)


def now_str():
    """
    사람이 읽기 쉬운 시간 문자열
    """
    return now_dt().strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------
# TIMESTAMP CONVERSION
# --------------------------------------------------

def ts_to_dt(ts):
    """
    timestamp → datetime
    """
    try:
        return datetime.fromtimestamp(ts, KST)
    except Exception:
        return None


def ts_to_str(ts):
    """
    timestamp → 문자열
    """
    dt = ts_to_dt(ts)

    if not dt:
        return "-"

    return dt.strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------
# MARKET SESSION
# --------------------------------------------------

def market_session():

    """
    한국 시장 기준 세션
    """

    now = now_dt()

    h = now.hour
    m = now.minute

    t = h * 60 + m

    open_time = 9 * 60
    close_time = 15 * 60 + 30

    if t < open_time:
        return "PRE_MARKET"

    if open_time <= t <= close_time:
        return "OPEN"

    return "POST_MARKET"


def is_market_open():

    """
    장중 여부
    """

    return market_session() == "OPEN"


# --------------------------------------------------
# SLEEP UTILITIES
# --------------------------------------------------

def sleep_until_next_second():

    """
    다음 초까지 sleep
    """

    now = time.time()

    sleep_time = 1 - (now - int(now))

    if sleep_time > 0:
        time.sleep(sleep_time)


def sleep_until(ts):

    """
    특정 timestamp까지 sleep
    """

    now = time.time()

    if ts > now:
        time.sleep(ts - now)


# --------------------------------------------------
# DURATION FORMAT
# --------------------------------------------------

def format_duration(seconds):

    """
    seconds → HH:MM:SS
    """

    seconds = int(seconds)

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02d}:{m:02d}:{s:02d}"
