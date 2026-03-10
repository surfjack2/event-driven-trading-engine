from ltb.trade.trade_store import TradeStore


class TradeRecorder:

    def __init__(self):

        self.store = TradeStore()

    def record_fill(self, order):

        trade = {
            "symbol": order.get("symbol"),
            "side": order.get("side"),
            "price": order.get("price"),
            "qty": order.get("qty")
        }

        self.store.record_trade(trade)
