import json
from pathlib import Path

from ltb.strategy.strategies.volume_breakout import VolumeBreakoutStrategy


class StrategyLoader:

    def __init__(self):

        self.config_path = Path("config/strategies.json")

    def load(self):

        with open(self.config_path) as f:
            config = json.load(f)

        strategies = []

        if config.get("volume_breakout", {}).get("enabled"):

            params = config["volume_breakout"]

            strategies.append(
                VolumeBreakoutStrategy(params)
            )

        return strategies
