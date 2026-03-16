def pct(value):

    if value is None:
        return "-"

    try:
        return f"{value * 100:.2f}%"
    except Exception:
        return "-"


def num(value):

    if value is None:
        return "-"

    try:
        return f"{value:.2f}"
    except Exception:
        return "-"
