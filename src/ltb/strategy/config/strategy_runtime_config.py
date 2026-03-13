import json
import os
import time

from ltb.system.logger import logger


class StrategyRuntimeConfig:

    CONFIG_PATH = "config/strategy_config.json"

    RELOAD_INTERVAL = 10

    def __init__(self):

        self.last_load = 0
        self.config = {}

        self._load()

    def _load(self):

        if not os.path.exists(self.CONFIG_PATH):

            logger.warning(
                "[STRATEGY CONFIG] file not found %s",
                self.CONFIG_PATH
            )

            return

        try:

            with open(self.CONFIG_PATH, "r") as f:
                self.config = json.load(f)

            self.last_load = time.time()

            logger.info(
                "[STRATEGY CONFIG] loaded strategies=%s",
                list(self.config.keys())
            )

        except Exception as e:

            logger.error(
                "[STRATEGY CONFIG] load failed %s",
                e
            )

    def get(self, strategy):

        now = time.time()

        if now - self.last_load > self.RELOAD_INTERVAL:
            self._load()

        return self.config.get(strategy, {})
