import csv
import time
from datetime import datetime

from ltb.system.logger import logger


class ReplayMarketWorker:

    def __init__(self, bus, data_file, replay_speed=0.01):

        self.bus = bus
        self.data_file = data_file
        self.replay_speed = replay_speed

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

                time.sleep(self.replay_speed)

        logger.info("[REPLAY FINISHED]")
