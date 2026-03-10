# LTB Git Commit Guidelines

이 문서는 LTB (Live Trading Bot) 프로젝트에서 사용하는 Git 커밋 관리 기준을 정의한다.

목적

- 커밋 히스토리를 명확하게 유지
- 기능 단위 개발 추적 가능
- 문제 발생 시 롤백 용이
- 프로젝트 변경 이력 문서화

---

# 1. 기본 원칙

LTB 프로젝트는 다음 원칙을 따른다.

1. 기능 단위 커밋
2. 의미 있는 커밋 메시지
3. 불필요한 파일 커밋 금지
4. 운영 로그 및 환경 파일 제외

특히 다음 파일은 절대 커밋하지 않는다.

- venv
- logs
- cache
- runtime 임시파일
- docker runtime 데이터

---

# 2. 커밋 전 확인

커밋 전에 반드시 상태를 확인한다.

git status

목적

- 의도하지 않은 파일 커밋 방지
- venv 포함 여부 확인
- 로그 파일 포함 여부 확인

---

# 3. 기본 커밋 절차

LTB 프로젝트에서 사용하는 기본 커밋 절차

1단계 변경파일 추가

git add .

또는 특정 파일만 추가

git add src/
git add docs/
git add web/

---

2단계 커밋

git commit -m "commit message"

---

3단계 커밋 확인

git log --oneline -5

---

# 4. 권장 커밋 메시지 규칙

LTB 프로젝트에서는 다음 형식을 권장한다.

type: short description

예시

feat: strategy engine improvements  
feat: admin console API added  
feat: swagger management interface  
fix: order execution bug  
fix: logging configuration issue  
docs: trading system operations guide  
refactor: strategy worker cleanup  

---

# 5. Commit Type 정의

| Type | 설명 |
|-----|-----|
| feat | 새로운 기능 |
| fix | 버그 수정 |
| docs | 문서 변경 |
| refactor | 코드 구조 개선 |
| test | 테스트 코드 |
| chore | 기타 유지보수 |

---

# 6. 잘못된 커밋 수정

마지막 커밋 취소 (파일 유지)

git reset --soft HEAD~1

마지막 커밋 완전 삭제

git reset --hard HEAD~1

---

# 7. 커밋 확인 명령

최근 커밋 확인

git log --oneline

최근 5개 커밋 확인

git log --oneline -5

---

# 8. LTB 프로젝트 커밋 예시

feat: LTB admin console and Swagger integration  
feat: runtime event driven engine  
feat: strategy worker framework  
fix: order executor retry logic  
docs: LTB trading system validation guide  

---

# 9. 권장 개발 방식

LTB 프로젝트는 다음 순서로 개발한다.

1 전략 개발  
2 전략 테스트  
3 로그 검증  
4 운영 기능 추가  
5 문서 업데이트  
6 커밋  

즉

코드 → 검증 → 문서 → 커밋

순서를 유지한다.

---

# 10. 결론

좋은 커밋 히스토리는 다음을 가능하게 한다.

- 문제 발생 시 빠른 롤백
- 기능 변경 추적
- 프로젝트 구조 이해
- 협업 및 유지보수

LTB 프로젝트에서는

작은 단위 커밋 + 명확한 메시지

를 기본 원칙으로 유지한다.
