import random

class OrderExecutor:
    def __init__(self, settings):
        self.settings = settings

        mock_config = settings.get("mock", {})

        self.mock_enabled = mock_config.get("enabled", True)
        self.mock_mode = mock_config.get("mode", "normal")
        self.price = mock_config.get("price", 50000)

        self.counter = 0  # 상태 변수 (POC용)

    # ==========================
    # REAL PRICE (실전 모드)
    # ==========================
    def get_real_price(self):
        raise NotImplementedError("Real API not implemented yet")

    # ==========================
    # PRICE ENTRY POINT
    # ==========================
    def get_price(self):

        # 🔒 1st 실전 모드
        if not self.mock_enabled:
            return self.get_real_price()

        # 🔬 2nd MOCK 모드
        mode = self.mock_mode

        # ====== FORCE BREAK (POC 재현용) ======
        if mode == "force_break":
            self.counter += 1

            if self.counter == 15:
                self.price *= 0.90  # -10% 강제 붕괴
            else:
                self.price *= 1.001

        # ====== DROP MODE ======
        elif mode == "drop":
            if random.random() < 0.1:
                self.price *= 0.95
            else:
                self.price *= random.uniform(0.999, 1.001)

        # ====== TREND MODE ======
        elif mode == "trend":
            self.price *= random.uniform(0.998, 1.002)

        # ====== NORMAL MODE ======
        else:
            change = random.uniform(-0.01, 0.01)
            self.price *= (1 + change)

        return round(self.price, 2)

    # ==========================
    # ORDER FUNCTIONS
    # ==========================
    def market_buy(self, symbol, qty):
        self.counter = 0  # 포지션 시작 시 카운터 리셋
        return {"symbol": symbol, "qty": qty, "price": self.get_price()}

    def market_sell(self, symbol, qty):
        return {"symbol": symbol, "qty": qty, "price": self.get_price()}
