from pathlib import Path

LOG_DIR = Path("logs")


class LogManager:

    def list_logs(self):
        return [f.name for f in LOG_DIR.glob("*.log")]

    def tail(self, log_name, lines=200):

        path = LOG_DIR / log_name

        if not path.exists():
            return []

        with open(path, "r") as f:
            return f.readlines()[-lines:]
