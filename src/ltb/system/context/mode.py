from enum import Enum


class SystemMode(str, Enum):

    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"
