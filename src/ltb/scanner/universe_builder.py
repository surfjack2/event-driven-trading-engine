import random
from ltb.system.logger import logger


class UniverseBuilder:

    def __init__(self):

        self.watchlist = []

    def build(self):

        symbols = []

        # Mock 시장 종목 생성
        for i in range(100000, 101000):
            symbols.append(str(i))

        random.shuffle(symbols)

        # Watchlist 크기 제한
        self.watchlist = symbols[:10]

        logger.info(f"Universe built: {len(self.watchlist)} symbols")

        return self.watchlist
