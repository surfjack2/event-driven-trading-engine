import logging


class ExecutionEngine:

    def __init__(self, engine):

        self.engine = engine

    def enter(self, symbol, qty, price, stop):

        logging.info(f"ENTER {symbol} qty={qty} price={price} stop={stop}")

        self.engine.positions[symbol] = {
            "qty": qty,
            "entry": price,
            "stop": stop
        }

    def exit(self, symbol):

        if symbol in self.engine.positions:

            del self.engine.positions[symbol]

        logging.info(f"EXIT {symbol}")
