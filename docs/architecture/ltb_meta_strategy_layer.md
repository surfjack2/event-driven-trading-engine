# LTB Meta Strategy Layer

MetaStrategyWorker는 전략 성과 기반 자동 전략 제어 레이어이다.

--------------------------------------------------

목적

전략 성과 기반 자동 제어
저성능 전략 자동 비활성화
전략 성과 회복 시 재활성

--------------------------------------------------

구성

strategy_performance_worker

↓

meta_strategy_worker

↓

strategy.enabled / strategy.disabled

↓

strategy_worker

--------------------------------------------------

동작

전략 performance score 평가

score < disable threshold

→ strategy.disabled

score > enable threshold

→ strategy.enabled

--------------------------------------------------

효과

dead strategy 자동 중단
adaptive trading system 구현
