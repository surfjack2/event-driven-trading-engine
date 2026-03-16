# LTB Strategy Set

현재 전략

--------------------------------------------------

Simple Momentum

Trend following 전략

조건

price > EMA
price > VWAP
RSI threshold
volume expansion

--------------------------------------------------

VWAP Reclaim

VWAP reclaim breakout 전략

조건

prev < VWAP
price >= VWAP
volume expansion

개선

fake reclaim filter
volatility filter

--------------------------------------------------

VWAP Band Bounce

VWAP mean reversion 전략

조건

price touches lower VWAP band
reversal confirmation
volume expansion

개선

touch cooldown
volatility guard
