import time
import random


def run_market_worker():

    print("[MARKET WORKER STARTED]")

    while True:

        # 실제 구현 시 KIS price API 호출

        price = random.uniform(45000, 65000)

        print(f"[MARKET] price update {price}")

        time.sleep(1)
