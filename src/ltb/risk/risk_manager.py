from ltb.system.logger import logger
from ltb.risk.atr_stop import ATRStop


class RiskManager:

    def __init__(self, engine):

        self.engine = engine

    def update_price(self, price):

        self.last_price = price

