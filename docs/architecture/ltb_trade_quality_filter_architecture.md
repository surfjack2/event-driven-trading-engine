# LTB Trade Quality Filter Architecture

TradeQualityFilterWorker는 전략 신호 중 저품질 진입을 제거하기 위해 추가된 레이어이다.

--------------------------------------------------

목적

fake entry 제거
liquidity trap 방지
volatility spike 대응

--------------------------------------------------

위치

Signal Pipeline

strategy
→ ranking
→ allocation
→ trade_quality_filter
→ position_intent

--------------------------------------------------

필터 기준

1. Liquidity

volume_ratio < threshold

2. Volatility

ATR / price > threshold

3. Momentum Quality

price_change < minimum threshold

4. VWAP Fake Reclaim

VWAP reclaim 전략에서

price ≈ VWAP 인 경우 제거

--------------------------------------------------

효과

fake reclaim 감소
liquidity trap 감소
low momentum entry 제거

--------------------------------------------------

결과

trade quality 향상
drawdown 감소
