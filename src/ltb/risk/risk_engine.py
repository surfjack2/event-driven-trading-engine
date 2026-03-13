from ltb.system.logger import logger


class RiskEngine:

    def __init__(self):

        # 동시에 열 수 있는 종목 수
        self.max_open_positions = 5

        # 종목별 최대 보유 수량
        self.max_symbol_position = 2000

        # 일일 손실 제한
        self.daily_loss_limit = -200000

        self.open_positions = {}

        self.capital = 10000000

        self.realized_pnl = 0

        logger.info("[RISK ENGINE INITIALIZED]")


    def update_position(self, symbol, position, price):

        if position <= 0:

            if symbol in self.open_positions:
                del self.open_positions[symbol]

        else:

            self.open_positions[symbol] = {
                "qty": position,
                "price": price
            }


    def record_trade(self, pnl):

        self.realized_pnl += pnl


    def check(self, symbol, qty, price):

        # 신규 포지션 수 제한
        if symbol not in self.open_positions:

            if len(self.open_positions) >= self.max_open_positions:

                logger.warning("[RISK BLOCK] max open positions reached")
                return False

        current_position = 0

        if symbol in self.open_positions:
            current_position = self.open_positions[symbol]["qty"]

        if current_position + qty > self.max_symbol_position:

            logger.warning("[RISK BLOCK] max symbol position reached")
            return False

        if self.realized_pnl <= self.daily_loss_limit:

            logger.warning("[RISK BLOCK] daily loss limit hit")
            return False

        return True
