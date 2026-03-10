import random


class SimpleMomentumStrategy:

    def __init__(self, config=None):

        self.config = config or {}

    def evaluate(self, event):

        symbol = event.get("symbol")
        price = event.get("price")

        # 확률 기반 시뮬레이션
        if random.random() > 0.7:

            signal = {
                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "qty": 1,
                "strategy": "simple_momentum"
            }

            return [signal]

        return []
