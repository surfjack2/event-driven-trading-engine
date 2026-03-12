import yaml

from ltb.strategy.simple_momentum_strategy import SimpleMomentumStrategy
from ltb.strategy.strategies.vwap_reclaim_band import VWAPReclaimBandStrategy


class StrategyLoader:

    def __init__(self, config_path="config/strategies.yaml"):
        self.config_path = config_path

    def load(self):

        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f)

        strategies = []

        configs = data.get("strategies", {})

        for name, config in configs.items():

            if not config.get("enabled", False):
                continue

            # --------------------------
            # Simple Momentum Strategy
            # --------------------------

            if name == "simple_momentum":

                strategy = SimpleMomentumStrategy(config)

                strategies.append(strategy)

            # --------------------------
            # VWAP Reclaim Band Strategy
            # --------------------------

            elif name == "vwap_reclaim_band":

                strategy = VWAPReclaimBandStrategy(config)

                strategies.append(strategy)

        return strategies
