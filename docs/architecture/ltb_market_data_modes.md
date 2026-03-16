============================================================
LTB MARKET DATA MODES
============================================================

BACKTEST
--------------------------------

Worker

ReplayMarketWorker

Source

CSV dataset replay


PAPER
--------------------------------

Worker

MarketWorker

Source

Mock random market generator


LIVE
--------------------------------

Worker

MarketWorker

Source

Not implemented

Placeholder only


Notes

LIVE market integration will require

KIS websocket
Upbit websocket


Pipeline

market.price
↓
IndicatorWorker
↓
StrategyWorker


============================================================
END
============================================================
