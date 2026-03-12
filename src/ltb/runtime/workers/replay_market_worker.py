import csv
import time
from datetime import datetime

from ltb.system.logger import logger


class ReplayMarketWorker:

    def __init__(self, bus, data_file):

        self.bus = bus
        self.data_file = data_file

        self.prev_price = {}

    def run(self):

        logger.info("[REPLAY MARKET WORKER STARTED]")

        with open(self.data_file, "r") as f:

            reader = csv.DictReader(f)

            for row in reader:

                symbol = row["symbol"]
                price = float(row["price"])
                volume = float(row["volume"])

                prev_price = self.prev_price.get(symbol)

                event = {
                    "symbol": symbol,
                    "price": price,
                    "volume": volume,
                    "prev_price": prev_price,
                }

                self.bus.publish(
                    "market.price",
                    event
                )

                self.bus.publish(
                    "MARKET_TICK",
                    event
                )

                self.prev_price[symbol] = price

                # replay 속도
                time.sleep(0.01)

        logger.info("[REPLAY FINISHED]")
