class PortfolioRiskManager:

    def __init__(self, engine):

        self.engine = engine

    def can_open_position(self, new_risk):

        for p in self.engine.positions.values():

            return False

        return True
