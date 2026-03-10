from ltb.system.logger import logger


class StrategyEngine:

    def __init__(self):

        self.strategies = []

        logger.info("[STRATEGY ENGINE INITIALIZED]")


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

                if result:
                    signals.extend(result)

            except Exception as e:

                logger.error(
                    "[STRATEGY ENGINE ERROR] strategy=%s error=%s",
                    strategy.__class__.__name__,
                    e
                )

        return signals
