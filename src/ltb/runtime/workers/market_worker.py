import time
import random

from ltb.system.logger import logger


class MarketWorker:

    def __init__(self, bus):

        self.bus = bus

        self.price = 55000

        self.state = "sideways"

        self.tick = 0


    def next_state(self):

        states = [
            "trend_up",
            "trend_down",
            "pullback",
            "sideways"
        ]

        self.state = random.choice(states)

        logger.info("[MARKET STATE] %s", self.state)


    def simulate_price(self):

        if self.state == "trend_up":

            self.price += random.uniform(50, 250)

        elif self.state == "trend_down":

            self.price -= random.uniform(50, 250)

        elif self.state == "pullback":

            self.price -= random.uniform(20, 120)

        elif self.state == "sideways":

            self.price += random.uniform(-80, 80)

        if self.price < 1000:
            self.price = 1000


    def run(self):

        logger.info("[MARKET WORKER STARTED]")

        while True:

            self.tick += 1

            # 30틱마다 시장 상태 변경
            if self.tick % 30 == 0:
                self.next_state()

            self.simulate_price()

            event = {
                "symbol": "TEST",
                "price": self.price,
                "market_state": self.state
            }

            logger.info(
                "[MARKET] price=%s state=%s",
                self.price,
                self.state
            )

            self.bus.publish(
                "market.price",
                event
            )

            time.sleep(0.2)


def run_market_worker(bus):

    worker = MarketWorker(bus)

    worker.run()
