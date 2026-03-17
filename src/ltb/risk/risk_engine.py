from ltb.system.logger import logger


class RiskEngine:

    def __init__(self, context):

        self.open_positions = {}

        logger.info("[RISK ENGINE INITIALIZED]")

    def get_capital(self):

        return self.context.get_capital()

    def update_position(self, symbol, position, price):

        if position <= 0:

            if symbol in self.open_positions:
                del self.open_positions[symbol]

        else:

            }

