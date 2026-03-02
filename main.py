import time
import traceback
from app.engine import TradingEngine

def run_engine():
    engine = TradingEngine()
    print("=== KIS TRADER ENGINE STARTED ===")

    while True:
        engine.tick()
        time.sleep(1)


if __name__ == "__main__":
    while True:
        try:
            run_engine()
        except KeyboardInterrupt:
            print("Manual shutdown.")
            break
        except Exception as e:
            print("FATAL ERROR:", e)
            traceback.print_exc()
            time.sleep(3)
