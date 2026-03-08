import time
from ltb.core.trading_engine import TradingEngine


def run_engine():

    engine = TradingEngine()

    print("=== LTB ENGINE PROCESS STARTED ===")

    while True:

        try:

            engine.tick()

        except Exception as e:

            print("ENGINE ERROR:", e)

        time.sleep(1)
