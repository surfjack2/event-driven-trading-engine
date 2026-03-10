import yaml


class StrategyConfigLoader:

    def __init__(self, config_path="config/strategies.yaml"):
        self.config_path = config_path

    def load(self):

        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f)

        return data.get("strategies", {})
