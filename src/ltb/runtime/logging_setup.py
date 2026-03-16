import logging
import os


def setup_logging():

    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    root = logging.getLogger()

    # 기존 콘솔 핸들러 제거
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    root.setLevel(logging.INFO)

    # engine (root)
    engine_handler = logging.FileHandler("logs/engine.log")
    engine_handler.setFormatter(formatter)
    root.addHandler(engine_handler)

    # market
    market_logger = logging.getLogger("MARKET")
    market_logger.propagate = False
    market_handler = logging.FileHandler("logs/market.log")
    market_handler.setFormatter(formatter)
    market_logger.addHandler(market_handler)

    # strategy
    strategy_logger = logging.getLogger("STRATEGY")
    strategy_logger.propagate = False
    strategy_handler = logging.FileHandler("logs/strategy.log")
    strategy_handler.setFormatter(formatter)
    strategy_logger.addHandler(strategy_handler)

    # trade
    trade_logger = logging.getLogger("ORDER")
    trade_logger.propagate = False
    trade_handler = logging.FileHandler("logs/trade.log")
    trade_handler.setFormatter(formatter)
    trade_logger.addHandler(trade_handler)

    # portfolio
    portfolio_logger = logging.getLogger("PORTFOLIO")
    portfolio_logger.propagate = False
    portfolio_handler = logging.FileHandler("logs/portfolio.log")
    portfolio_handler.setFormatter(formatter)
    portfolio_logger.addHandler(portfolio_handler)

    # risk
    risk_logger = logging.getLogger("RISK")
    risk_logger.propagate = False
    risk_handler = logging.FileHandler("logs/risk.log")
    risk_handler.setFormatter(formatter)
    risk_logger.addHandler(risk_handler)

    # trail
    trail_logger = logging.getLogger("TRAIL")
    trail_logger.propagate = False
    trail_handler = logging.FileHandler("logs/trail.log")
    trail_handler.setFormatter(formatter)
    trail_logger.addHandler(trail_handler)
