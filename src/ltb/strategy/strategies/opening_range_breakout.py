from ltb.system.logger import logger
import time


class OpeningRangeBreakoutStrategy:

    def __init__(self, config=None):

        self.config = config or {}

        self.range_high = {}
        self.range_low = {}

        self.range_complete = {}

    def evaluate(self, event):

        symbol = event.get("symbol")

        now = time.localtime()
