from ltb.system.logger import logger


class VWAPReclaimBandStrategy:

    def __init__(self, config=None):

        self.config = config or {}

    def evaluate(self, event):

        symbol = event["symbol"]

        if not vwap or not prev or not price:
            return []

        if atr:

                return []
