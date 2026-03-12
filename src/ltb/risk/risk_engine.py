from ltb.system.logger import logger


class RiskEngine:

    def __init__(self):

        self.max_open_positions = 5
        self.max_symbol_position = 100
        self.max_capital_usage = 0.3
        self.daily_loss_limit = -200000

        self.open_positions = {}
        self.capital = 10000000
        self.used_capital = 0
        self.realized_pnl = 0

        logger.info("[RISK ENGINE INITIALIZED]")


    def update_position(self, symbol, position, price):

        # 포지션 종료 시 제거
        if position <= 0:

            if symbol in self.open_positions:
                del self.open_positions[symbol]

        else:

            self.open_positions[symbol] = {
                "qty": position,
                "price": price
            }

        # capital 재계산
        total = 0

        for pos in self.open_positions.values():

            total += pos["qty"] * pos["price"]

        self.used_capital = total


    def record_trade(self, pnl):

        self.realized_pnl += pnl


    def check(self, symbol, qty, price):

        # 신규 포지션 제한
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

        new_capital = self.used_capital + qty * price

        if new_capital / self.capital > self.max_capital_usage:

            logger.warning("[RISK BLOCK] capital usage limit")
            return False

        if self.realized_pnl <= self.daily_loss_limit:

            logger.warning("[RISK BLOCK] daily loss limit hit")
            return False

        return True
