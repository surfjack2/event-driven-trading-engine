import json
import os
from datetime import datetime


TRADE_FILE = "logs/trades.json"


class TradeStore:

    def __init__(self):

        if not os.path.exists(TRADE_FILE):
            with open(TRADE_FILE, "w") as f:
                json.dump([], f)

    def _load(self):

        with open(TRADE_FILE, "r") as f:
            return json.load(f)

    def _save(self, trades):

        with open(TRADE_FILE, "w") as f:
            json.dump(trades, f, indent=2)

    def record_trade(self, trade):

        trades = self._load()

        trade["timestamp"] = datetime.utcnow().isoformat()

        trades.append(trade)

        self._save(trades)

    def list_trades(self):

        return self._load()

    def last_trades(self, n=20):

        trades = self._load()

        return trades[-n:]
