import time
from ltb.system.logger import logger
from ltb.data.universe_builder import UniverseBuilder


class UniverseScannerWorker:

    def __init__(self, bus):

        self.bus = bus

        self.builder = UniverseBuilder()

        self.current_universe = set()

        # symbol → timestamp
        self.scanner_candidates = {}

        # 후보 유지 시간
        self.candidate_ttl = 300

        # 최대 universe
        self.max_universe = 200

        self.bus.subscribe(
            "market.scanner",
            self.on_scanner
        )

    def run(self):

        logger.info("[UNIVERSE SCANNER WORKER STARTED]")

        while True:

            self.cleanup_candidates()

            base = set(self.builder.build())

            dynamic = set(self.scanner_candidates.keys())

            universe = base | dynamic

            # universe size 제한
            if len(universe) > self.max_universe:

                universe = set(list(universe)[:self.max_universe])

            if universe != self.current_universe:

                self.current_universe = universe

                logger.info(
                    f"[UNIVERSE] updated symbols={len(universe)}"
                )

                self.bus.publish(
                    "market.universe",
                    {
                        "symbols": list(universe)
                    }
                )

            time.sleep(30)

    def on_scanner(self, data):

        symbol = data["symbol"]

        self.scanner_candidates[symbol] = time.time()

    def cleanup_candidates(self):

        now = time.time()

        expired = []

        for symbol, ts in self.scanner_candidates.items():

            if now - ts > self.candidate_ttl:
                expired.append(symbol)

        for symbol in expired:

            del self.scanner_candidates[symbol]

        if expired:

            logger.info(
                f"[UNIVERSE] expired candidates removed={len(expired)}"
            )
