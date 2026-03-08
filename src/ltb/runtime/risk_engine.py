from ltb.system.logger import logger


class RiskEngine:

    def __init__(self):

        self.max_position = 1

        logger.info("[RISK ENGINE INITIALIZED]")


    def check(self, symbol, qty, price):

        # 지금은 단순 통과

        return True
