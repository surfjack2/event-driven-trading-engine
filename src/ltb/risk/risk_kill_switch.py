from ltb.system.logger import logger


class RiskKillSwitch:

    def __init__(self):

        # 최대 보유 포지션
        self.max_position = 5

        # 최대 주문 횟수
        self.max_trades = 20

        # 현재 상태
        self.current_position = 0
        self.trade_count = 0

        self.enabled = True

        logger.info("[RISK KILL SWITCH INITIALIZED]")


    def update_position(self, position):

        self.current_position = position


    def record_trade(self):

        self.trade_count += 1


    def check(self):

        if not self.enabled:
            return True

        if self.current_position >= self.max_position:

            logger.warning("[RISK BLOCK] max position reached")

            return False

        if self.trade_count >= self.max_trades:

            logger.warning("[RISK BLOCK] max trades reached")

            return False

        return True
