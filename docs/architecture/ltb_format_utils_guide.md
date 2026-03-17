# LTB Format Utilities Guide

본 문서는 LTB 시스템에서 사용되는 공통 숫자 및 문자열 포맷 유틸리티를 설명한다.

파일 위치

src/ltb/system/format_utils.py

목적

- CLI Monitor 출력 통일
- 로그 포맷 통일
- Dashboard / API 출력 일관성 유지
- 숫자 표현 규칙 표준화

--------------------------------------------------

NUMERIC FORMAT FUNCTIONS

num(value, digits=2)

일반 숫자 출력

example

123.456 → 123.46


pct(value, digits=2)

퍼센트 표현

example

0.1234 → 12.34%


currency(value)

통화 표현

example

12345.6 → 12,345.60


compact(value)

큰 숫자 축약 표현

example

1500 → 1.50K
2500000 → 2.50M


ratio(value)

비율 표현

example

1.2345 → 1.23


integer(value)

정수 표현

example

123.9 → 123


safe(value)

None 안전 문자열 출력

example

None → "-"

--------------------------------------------------

USAGE EXAMPLES

from ltb.system.format_utils import num, pct

num(123.456)
→ 123.46

pct(0.1234)
→ 12.34%

--------------------------------------------------

LTB DISPLAY STANDARD

CLI Monitor

숫자 → num()
비율 → pct()
PnL → currency()

--------------------------------------------------

DESIGN PRINCIPLE

Formatting Logic Centralization

숫자 포맷 로직은 개별 Worker에 구현하지 않는다.

모든 포맷은 format_utils.py 에서 관리한다.

--------------------------------------------------

BENEFITS

- 출력 형식 통일
- 코드 중복 제거
- CLI / API / Dashboard 동일 출력
- 유지보수 용이
