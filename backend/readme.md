# Qurious Backend

## Prerequisite
--------
1. python 3.6 이상
2. Docker (Stable Version)

설치법 (Mac os 기준)
``` bash
cd backend
pip install -r deploy/requirements.txt #필요한 라이브러리 설치
./init_db.sh --migrate # Docker 내 DB 컨테이너 셋팅, Secret Key 생성, DB 마이그레이션, admin user 추가

# DB만 새로 초기화 경우
./init_db.sh
```

## Usage

### Run Backend Sever
``` bash
python manege.py runserver #백엔드 서버 가동
# PORT 번호 확인 // 주로 8000
```

### Set Target and Run Frontend Server
``` bash
cd frontend
npm install
NODE_ENV=development npm run build:dll
TARGET=http://localhost:8000 npm run dev
```
위 과정대로 하면 Backend dev서버와 연결된 Vue 서버를 켤 수 있다.

이제 init_db.sh를 통해 생성한 어드민 유저로 로그인이 가능하다. 
열려진 페이지에서 login을 누르고 ID: root, PW: rootroot 를 입력해서 로그인 성공시 모든 것이 순조롭다.

