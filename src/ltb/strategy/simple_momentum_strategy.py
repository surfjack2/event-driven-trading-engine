from ltb.system.logger import logger


class SimpleMomentumStrategy:

    def __init__(self, config=None):

        self.config = config or {}

    def evaluate(self, event):

        symbol = event.get("symbol")
