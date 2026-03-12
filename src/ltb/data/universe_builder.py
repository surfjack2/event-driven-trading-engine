class UniverseBuilder:

    def __init__(self, size=50):

        self.size = size

    def build(self):

        symbols = []

        for i in range(self.size):

            symbol = f"TEST{i:03d}"

            symbols.append(symbol)

        return symbols
