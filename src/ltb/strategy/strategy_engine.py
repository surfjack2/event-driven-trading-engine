from ltb.system.logger import logger


class StrategyEngine:

    def __init__(self):

        self.strategies = []

    def register(self, strategy):

        self.strategies.append(strategy)

        logger.info(
            "[STRATEGY ENGINE] registered %s",
            strategy.__class__.__name__
        )

    def evaluate(self, event):

        signals = []

        for strategy in self.strategies:

            try:

                result = strategy.evaluate(event)

                if not result:
                    continue

                for signal in result:
                    signals.append(signal)

            except Exception as e:

                logger.error(
                    "[STRATEGY ENGINE ERROR] %s",
                    str(e)
                )

        return signals
