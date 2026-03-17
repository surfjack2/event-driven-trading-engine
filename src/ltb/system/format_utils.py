"""
LTB Formatting Utilities

CLI / Logging / Monitoring 에서 사용하는 공통 숫자 포맷 유틸.
"""


def num(value, digits=2):
    """
    일반 숫자 포맷

    example
    123.4567 → 123.46
    """

    if value is None:
        return "-"

    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "-"


def pct(value, digits=2):
    """
    퍼센트 포맷

    example
    0.1234 → 12.34%
    """

    if value is None:
        return "-"

    try:
        return f"{float(value) * 100:.{digits}f}%"
    except Exception:
        return "-"


def currency(value, digits=2):
    """
    통화 포맷

    example
    12345.6 → 12,345.60
    """

    if value is None:
        return "-"

    try:
        return f"{float(value):,.{digits}f}"
    except Exception:
        return "-"


def compact(value):
    """
    큰 숫자 축약

    example
    1200 → 1.2K
    2000000 → 2.0M
    """

    if value is None:
        return "-"

    try:

        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        if abs(value) >= 1_000:
            return f"{value/1_000:.2f}K"

        return f"{value:.2f}"

    except Exception:
        return "-"


def ratio(value, digits=2):
    """
    비율 포맷

    example
    1.2345 → 1.23
    """

    if value is None:
        return "-"

    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "-"


def integer(value):
    """
    정수 포맷
    """

    if value is None:
        return "-"

    try:
        return f"{int(value)}"
    except Exception:
        return "-"


def safe(value):
    """
    문자열 안전 출력
    """

    if value is None:
        return "-"

    return str(value)
