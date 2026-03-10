class PositionManager:

    def __init__(self):

        self.positions = {}

    def has_position(self, symbol):

        return symbol in self.positions

    def open_position(self, symbol, price):

        self.positions[symbol] = {
            "entry_price": price,
            "highest_price": price
        }

    def update_price(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]

        if price > pos["highest_price"]:
            pos["highest_price"] = price

    def close_position(self, symbol):

        if symbol in self.positions:
            del self.positions[symbol]

    def get_position(self, symbol):

        return self.positions.get(symbol)
