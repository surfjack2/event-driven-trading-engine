import time

from ltb.system.logger import logger


class AccountStatsWorker:

    def __init__(self, bus):

        self.bus = bus

        self.daily_pnl = 0
        self.weekly_pnl = 0
        self.monthly_pnl = 0

        self.capital = 0

        self.bus.subscribe(
            "risk.daily_pnl",
            self.on_daily_pnl
        )

        self.bus.subscribe(
            "portfolio.capital",
            self.on_capital
        )

    def on_daily_pnl(self, data):

        pnl = data.get("pnl", 0)

        self.daily_pnl = pnl
        self.weekly_pnl += pnl
        self.monthly_pnl += pnl

    def on_capital(self, data):

        self.capital = data.get("capital", 0)

    def run(self):

        logger.info("[ACCOUNT STATS WORKER STARTED]")

        while True:

            logger.info(
                "[ACCOUNT] capital=%s daily=%s weekly=%s monthly=%s",
                round(self.capital, 2),
                round(self.daily_pnl, 2),
                round(self.weekly_pnl, 2),
                round(self.monthly_pnl, 2)
            )

            time.sleep(5)
