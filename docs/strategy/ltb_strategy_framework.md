# LTB Strategy Framework

The strategy framework allows multiple trading strategies to run simultaneously.

Strategies generate signals which are later evaluated by the ranking engine.

--------------------------------------------------

Strategy Lifecycle

Market Event
↓
Strategy Evaluation
↓
Signal Generation
↓
Signal Ranking
↓
Portfolio Selection
↓
Execution

--------------------------------------------------

Strategy Examples

VWAP Reclaim

Price reclaims VWAP after temporary deviation.

Momentum Breakout

Price moves beyond recent consolidation range.

VWAP Bounce

Price bounces from VWAP support.

--------------------------------------------------

Strategy Interface

Each strategy implements

evaluate(event)

Output

signal dictionary containing

symbol
strategy
features
price
timestamp
