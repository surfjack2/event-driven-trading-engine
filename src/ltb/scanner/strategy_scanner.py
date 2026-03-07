from ltb.system.logger import logger


class StrategyScanner:

    def __init__(self, strategy):

        self.strategy = strategy

    def scan(self, watchlist):

        candidates = []

        for symbol in watchlist:

            try:

                if self.strategy.check_entry(symbol):
                    candidates.append(symbol)

            except Exception as e:

                logger.error(f"Scanner error {symbol}: {e}")

        return candidates
