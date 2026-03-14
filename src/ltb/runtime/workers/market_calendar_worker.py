import time
import datetime
import pandas_market_calendars as mcal

from ltb.system.logger import logger


class MarketCalendarWorker:

    def __init__(self, bus, market="US"):

        self.bus = bus

        self.market = market

        if market == "US":
            self.calendar = mcal.get_calendar("NYSE")

        elif market == "KR":
            self.calendar = mcal.get_calendar("XKRX")

        else:
            raise ValueError("Unsupported market")

        self.last_state = None

    def run(self):

        logger.info("[MARKET CALENDAR WORKER STARTED]")

        while True:

            now = datetime.datetime.utcnow()

            today = now.date()

            schedule = self.calendar.schedule(
                start_date=today,
                end_date=today
            )

            open_flag = not schedule.empty

            if open_flag != self.last_state:

                logger.info(
                    "[MARKET CALENDAR] market=%s open=%s",
                    self.market,
                    open_flag
                )

                self.bus.publish(
                    "market.calendar",
                    {
                        "market": self.market,
                        "open": open_flag
                    }
                )

                self.last_state = open_flag

            time.sleep(60)
