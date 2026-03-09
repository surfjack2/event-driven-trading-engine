# Git Repository Cleanup Guide (Python venv)

이 문서는 Python 프로젝트에서 잘못 commit된 venv 환경을 제거하는 방법을 설명한다.

Python 프로젝트에서는 다음 파일들이 Git에 포함되면 안된다.

venv/
__pycache__/
*.pyc
.env

이 파일들은 로컬 환경에서 생성되는 것이므로 repository에 포함될 필요가 없다.

--------------------------------------------------

1. 문제 상황

다음과 같은 상황이 발생할 수 있다.

git commit 시 다음 파일들이 포함됨

venv/lib/python3.x/site-packages/...

이 경우 repository 크기가 커지고 협업 시 문제가 발생한다.

--------------------------------------------------

2. 해결 절차

1️⃣ .gitignore 생성

프로젝트 루트에서 .gitignore 파일을 생성한다.

권장 내용

venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
logs/*.log

--------------------------------------------------

2️⃣ Git index에서 venv 제거

다음 명령 실행

git rm -r --cached venv

설명

Git에서만 제거되고 실제 파일은 삭제되지 않는다.

--------------------------------------------------

3️⃣ 변경사항 commit

git commit -m "Remove venv from repository and add gitignore"

--------------------------------------------------

3. 확인 방법

Git 상태 확인

git status

venv가 repository에서 제외된 것을 확인한다.

--------------------------------------------------

4. Python 프로젝트 권장 .gitignore

venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
logs/*.log

--------------------------------------------------

5. 주의사항

다음 파일은 Git에 commit하면 안 된다.

venv
node_modules
build artifacts
log files
local config

--------------------------------------------------

6. 결론

Python 프로젝트에서는 가상환경(venv)을 Git에 포함시키지 않는다.

Repository에는 다음만 포함된다.

source code
config template
requirements.txt
documentation
