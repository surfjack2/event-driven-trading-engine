import time
from ltb.core.trading_engine import TradingEngine
from ltb.runtime.queue_bus import queue_signal


def run_engine():

    engine = TradingEngine()

    print("=== LTB ENGINE PROCESS STARTED ===")

    while True:

        try:

            # 기존 엔진 루프
            engine.tick()

            # Strategy Worker 신호 처리
            while not queue_signal.empty():

                signal = queue_signal.get()

                symbol = signal["symbol"]
                price = signal["price"]

                print(f"[ENGINE] executing signal {signal}")

                engine.execution.enter(symbol, 1, price, price * 0.92)

        except Exception as e:

            print("ENGINE ERROR:", e)

        time.sleep(1)
