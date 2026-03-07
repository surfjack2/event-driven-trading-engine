class PositionSizeManager:

    def __init__(self, engine):

        self.engine = engine

        self.capital = 10000000
        self.risk_per_trade = 0.01

    def calculate_qty(self, price):

        risk_amount = self.capital * self.risk_per_trade

        qty = int(risk_amount / price)

        if qty < 1:
            qty = 1

        return qty
