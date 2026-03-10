import logging
import os


def setup_logging():

    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # engine
    engine_handler = logging.FileHandler("logs/engine.log")
    engine_handler.setFormatter(formatter)
    root.addHandler(engine_handler)

    # market
    market_handler = logging.FileHandler("logs/market.log")
    market_handler.setFormatter(formatter)
    logging.getLogger("MARKET").addHandler(market_handler)

    # strategy
    strategy_handler = logging.FileHandler("logs/strategy.log")
    strategy_handler.setFormatter(formatter)
    logging.getLogger("STRATEGY").addHandler(strategy_handler)

    # trade
    trade_handler = logging.FileHandler("logs/trade.log")
    trade_handler.setFormatter(formatter)
    logging.getLogger("ORDER").addHandler(trade_handler)

    # portfolio
    portfolio_handler = logging.FileHandler("logs/portfolio.log")
    portfolio_handler.setFormatter(formatter)
    logging.getLogger("PORTFOLIO").addHandler(portfolio_handler)

    # risk
    risk_handler = logging.FileHandler("logs/risk.log")
    risk_handler.setFormatter(formatter)
    logging.getLogger("RISK").addHandler(risk_handler)

    # trail
    trail_handler = logging.FileHandler("logs/trail.log")
    trail_handler.setFormatter(formatter)
    logging.getLogger("TRAIL").addHandler(trail_handler)
