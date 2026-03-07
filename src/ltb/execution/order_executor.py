import random


class OrderExecutor:

    def __init__(self, settings):

        self.settings = settings

    # ==========================
    # PRICE
    # ==========================

    def get_price(self, symbol):

        # POC용 랜덤 가격 시뮬레이션
        base = 50000

        price = base + random.uniform(-5000, 5000)

        return round(price, 2)

    # ==========================
    # BUY
    # ==========================

    def market_buy(self, symbol, qty):

        price = self.get_price(symbol)

        return {
            "symbol": symbol,
            "qty": qty,
            "price": price
        }

    # ==========================
    # SELL
    # ==========================

    def market_sell(self, symbol, qty):

        price = self.get_price(symbol)

        return {
            "symbol": symbol,
            "qty": qty,
            "price": price
        }
