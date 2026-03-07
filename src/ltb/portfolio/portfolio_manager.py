from ltb.portfolio.position import Position


class PortfolioManager:

    def __init__(self):
        self.positions = {}

    # ==========================
    # 포지션 조회
    # ==========================
    def get_positions(self):
        return self.positions

    # ==========================
    # 포지션 열기
    # ==========================
    def open_position(self, symbol, qty, entry_price, stop_price):

        pos = Position(symbol, qty, entry_price, stop_price)

        self.positions[symbol] = pos

        return pos

    # ==========================
    # 포지션 종료
    # ==========================
    def close_position(self, symbol):

        if symbol in self.positions:
            del self.positions[symbol]

    # ==========================
    # 포지션 존재 여부
    # ==========================
    def has_position(self, symbol):

        return symbol in self.positions
