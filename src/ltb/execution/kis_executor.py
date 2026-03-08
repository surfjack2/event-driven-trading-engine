from ltb.system.logger import logger


class KISExecutor:

    def __init__(self):

        logger.info("[KIS EXECUTOR INITIALIZED]")


    def place_order(self, symbol, side, qty, price):

        logger.info(
            "[KIS] placing order %s %s qty=%s price=%s",
            symbol,
            side,
            qty,
            price
        )

        # 현재는 mock fill
        fill = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price
        }

        logger.info("[KIS] order filled")

        return fill
