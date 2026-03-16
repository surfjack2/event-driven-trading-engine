class ExitManager:

    def __init__(self):

        self.closing_symbols = set()

    def request_exit(self, symbol):

        if symbol in self.closing_symbols:
            return False

        self.closing_symbols.add(symbol)

        return True

    def clear(self, symbol):

        if symbol in self.closing_symbols:
            self.closing_symbols.remove(symbol)
