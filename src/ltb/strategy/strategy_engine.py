from ltb.system.logger import logger


class StrategyEngine:

    def __init__(self):

        self.strategies = []

    # ---------------------------
    # 전략 등록
    # ---------------------------
    def register(self, strategy):

        logger.info(
            "[STRATEGY ENGINE] register %s",
            strategy.name
        )

        self.strategies.append(strategy)

    # ---------------------------
    # 전략 평가
    # ---------------------------
    def evaluate(self, event):

        signals = []

        for strategy in self.strategies:

            try:

                signal = strategy.evaluate(event)

                if signal:

                    signals.append(signal)

            except Exception as e:

                logger.error(
                    "[STRATEGY ERROR] %s %s",
                    strategy.name,
                    str(e)
                )

        return signals
