import time
import datetime

from ltb.system.logger import logger


class MarketSessionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.market_open = False
        self.session = "CLOSED"

        self.bus.subscribe(
            "market.calendar",
            self.on_calendar
        )

    def run(self):

        logger.info("[MARKET SESSION WORKER STARTED]")

        while True:

            self.update_session()

            time.sleep(10)

    def on_calendar(self, data):

        self.market_open = data.get("open", False)

    def update_session(self):

        if not self.market_open:

            if self.session != "CLOSED":

                self.session = "CLOSED"

                self.publish()

            return

        now = datetime.datetime.utcnow().time()

        if now < datetime.time(13, 30):
            new_session = "PREMARKET"

        elif now < datetime.time(14, 30):
            new_session = "OPEN"

        elif now < datetime.time(19, 0):
            new_session = "MIDDAY"

        else:
            new_session = "POWERHOUR"

        if new_session != self.session:

            self.session = new_session

            self.publish()

    def publish(self):

        logger.info(
            "[MARKET SESSION] %s",
            self.session
        )

        self.bus.publish(
            "market.session",
            {
                "session": self.session
            }
        )
