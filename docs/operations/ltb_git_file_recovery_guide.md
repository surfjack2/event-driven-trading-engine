# Git File Recovery Guide

## 1. Purpose

이 문서는 **Git 저장소에서 과거 특정 파일을 복구하는 방법**을 설명한다.

사용 목적

* 실수로 코드 삭제
* 전략 코드 롤백
* Worker 코드 복구
* 특정 시점 버전 확인

LTB 개발 과정에서 다음 상황이 자주 발생한다.

```id="23e7m2"
전략 파일 수정
Worker 구조 변경
리팩토링 중 코드 손실
```

이때 Git 기록을 이용해 **특정 파일만 복구할 수 있다.**

---

# 2. 현재 파일 변경 상태 확인

현재 작업 상태 확인

```bash id="1wq5dd"
git status
```

예시

```id="u2xqsk"
modified: strategy_worker.py
modified: execution_worker.py
new file: volume_breakout.py
```

---

# 3. 파일 변경 이력 확인

특정 파일의 commit 기록 확인

```bash id="7u9z7g"
git log --oneline <file_path>
```

예

```bash id="qv3y91"
git log --oneline src/ltb/runtime/workers/strategy_worker.py
```

예시 결과

```id="32y81e"
3d96a93 strategy worker update
2140608 restore strategy engine
e76e257 remove legacy strategy scanner
```

---

# 4. 특정 commit에서 파일 내용 확인

파일을 복구하기 전에 **내용만 확인할 수 있다.**

```bash id="6d8j4c"
git show <commit_id>:<file_path>
```

예

```bash id="0n7we7"
git show 2140608:src/ltb/runtime/workers/strategy_worker.py
```

이 명령은

```id="l60owv"
파일 내용을 터미널에 출력
```

한다.

---

# 5. 특정 파일 과거 버전 복구

과거 commit에서 **파일을 현재 작업 디렉토리로 복구**

```bash id="1vlvru"
git checkout <commit_id> -- <file_path>
```

예

```bash id="p6okyr"
git checkout 2140608 -- src/ltb/runtime/workers/strategy_worker.py
```

결과

```id="9x9syo"
해당 commit의 파일이 현재 디렉토리로 복원된다.
```

이때 commit 기록은 바뀌지 않는다.

---

# 6. 최신 커밋 기준으로 파일 되돌리기

현재 수정된 파일을 **HEAD 기준으로 복구**

```bash id="g6q2r3"
git restore <file_path>
```

예

```bash id="7r4wbb"
git restore src/ltb/runtime/workers/strategy_worker.py
```

효과

```id="5m63l3"
마지막 커밋 상태로 파일 복구
```

---

# 7. Stage 상태 파일 되돌리기

이미 `git add` 했을 경우

```bash id="8j94yd"
git restore --staged <file_path>
```

예

```bash id="8jtpqx"
git restore --staged src/ltb/runtime/workers/strategy_worker.py
```

---

# 8. 특정 파일만 이전 commit으로 완전 롤백

과거 버전으로 복구 후 commit

```bash id="rx0tpp"
git checkout <commit_id> -- <file_path>

git add <file_path>

git commit -m "restore file from <commit_id>"
```

예

```bash id="53k8k1"
git checkout 2140608 -- src/ltb/runtime/workers/strategy_worker.py

git add src/ltb/runtime/workers/strategy_worker.py

git commit -m "restore strategy_worker from previous version"
```

---

# 9. 파일 삭제 후 복구

파일을 삭제했을 경우

```bash id="y5h2r3"
git checkout HEAD -- <file_path>
```

예

```bash id="1mttb5"
git checkout HEAD -- src/ltb/strategy/simple_momentum_strategy.py
```

---

# 10. 특정 파일 변경 내용 비교

현재 파일과 이전 commit 비교

```bash id="3i2cs7"
git diff <commit_id> <file_path>
```

예

```bash id="8v2v8c"
git diff 2140608 src/ltb/runtime/workers/strategy_worker.py
```

---

# 11. 특정 파일 전체 변경 히스토리

파일 변경 기록

```bash id="kgn0j5"
git log -p <file_path>
```

예

```bash id="3tqv1y"
git log -p src/ltb/runtime/workers/execution_worker.py
```

---

# 12. 안전한 복구 절차 (추천)

파일 복구 시 권장 절차

```id="7e2tdg"
1. git log 로 commit 확인
2. git show 로 내용 확인
3. git checkout 으로 파일 복구
4. git commit 으로 변경 기록 저장
```

---

# 13. Example Recovery Scenario

상황

```id="p3b6b9"
StrategyWorker 코드 손상
```

복구 절차

```bash id="5ntk8g"
git log --oneline src/ltb/runtime/workers/strategy_worker.py

git show <commit_id>:src/ltb/runtime/workers/strategy_worker.py

git checkout <commit_id> -- src/ltb/runtime/workers/strategy_worker.py

git add src/ltb/runtime/workers/strategy_worker.py

git commit -m "restore strategy worker"
```

---

# 14. Notes

Git은 **파일 단위 복구가 가능하다.**

즉 다음 작업이 모두 가능하다.

```id="z0z1ru"
특정 전략 파일만 복구
Worker 코드만 복구
설정 파일만 복구
```

프로젝트 전체를 롤백할 필요는 없다.

---

# 15. Summary

가장 자주 사용하는 명령

```bash id="0v8g9z"
git log --oneline <file>

git show <commit>:<file>

git checkout <commit> -- <file>

git restore <file>
```

이 네 가지 명령만 알아도 **대부분의 파일 복구 작업이 가능하다.**
