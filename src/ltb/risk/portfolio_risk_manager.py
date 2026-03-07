class PortfolioRiskManager:

    def __init__(self, engine):

        self.engine = engine
        self.max_portfolio_risk = 100000

    def can_open_position(self, new_risk):

        current_risk = 0

        for p in self.engine.positions.values():

            entry = p["entry"]
            stop = p["stop"]
            qty = p["qty"]

            current_risk += abs(entry - stop) * qty

        if current_risk + new_risk > self.max_portfolio_risk:
            return False

        return True
