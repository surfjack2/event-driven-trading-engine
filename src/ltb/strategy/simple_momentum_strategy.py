import random


class SimpleMomentumStrategy:

    def check_entry(self, symbol):

        # 확률 기반 시뮬레이션
        return random.random() > 0.7

    def calculate_stop(self, price):

        # ATR 대신 간단한 8% stop
        return price * 0.92
