from ltb.system.logger import logger
import time


class VWAPBandBounceStrategy:

    def __init__(self, config=None):

        self.config = config or {}

        self.last_touch = {}

    def evaluate(self, event):

        symbol = event["symbol"]
