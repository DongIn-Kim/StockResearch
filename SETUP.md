# SR Research Centre — 초기 설정 가이드

클론 후 아래 5단계만 완료하면 `/company_analysis 삼성전자` 같은 명령으로 바로 분석을 시작할 수 있습니다.

---

## 빠른 시작 (5단계)

```bash
# 1. 의존성 설치 + 빌드
pnpm install && pnpm --filter @paperclipai/plugin-sdk build

# 2. 환경변수 파일 생성
cp .env.example .env
# → .env를 열어 PAPERCLIP_AGENT_JWT_SECRET, DART_API_KEY, ECOS_API_KEY, FRED_API_KEY 입력

# 3. DB + 서버 실행 (터미널 1)
docker compose -f docker/docker-compose.yml up -d  # PostgreSQL (처음 한 번)
pnpm dev

# 4. 부트스트랩 — 회사·에이전트 18명 자동 생성 (터미널 2, 서버 실행 중에)
python3 scripts/bootstrap.py

# 5. 인프라 키 파일 생성
cp INFRA.example.md INFRA.md
# → INFRA.md 안에 실제 API 키 입력
```

이후 Claude Code를 열고 "삼성전자 기업분석 해줘" 또는 `/company_analysis 삼성전자`로 바로 시작하세요.

---

## 상세 설명

### 1. 의존성 설치

```bash
pnpm install
pnpm --filter @paperclipai/plugin-sdk build
```

> `pnpm install`만으로는 부족합니다 — plugin-sdk dist가 없으면 서버가 시작되지 않습니다.

---

### 2. 환경변수 설정 (`.env`)

```bash
cp .env.example .env
```

| 변수명 | 설명 | 발급 |
|--------|------|------|
| `PAPERCLIP_AGENT_JWT_SECRET` | 에이전트 인증 JWT | `openssl rand -base64 32` |
| `DART_API_KEY` | 금융감독원 전자공시 | [OpenDART](https://opendart.fss.or.kr/) 회원가입 |
| `ECOS_API_KEY` | 한국은행 경제통계 | [ECOS](https://ecos.bok.or.kr/) 이용신청 |
| `FRED_API_KEY` | 미국 연준 경제 데이터 | [FRED](https://fred.stlouisfed.org/docs/api/api_key.html) |
| `DATABASE_URL` | PostgreSQL 연결 문자열 | 아래 DB 설정 참고 |

`SR_COMPANY_ID`와 에이전트 ID들은 bootstrap.py가 자동으로 `.env`에 추가합니다.

---

### 3. 데이터베이스 + 서버 실행

```bash
# Docker로 PostgreSQL 실행 (처음 한 번)
docker compose -f docker/docker-compose.yml up -d

# 마이그레이션
pnpm db:migrate

# 서버 실행
pnpm dev
```

서버가 `http://127.0.0.1:3100`에서 실행되면 다음 단계로 넘어갑니다.

---

### 4. Bootstrap — 회사·에이전트 자동 생성

```bash
python3 scripts/bootstrap.py
```

스크립트가 자동으로 처리하는 내용:
- SR Research Centre 회사 생성 (이미 있으면 재사용)
- 18명의 에이전트 생성 (Head of Research, Sector/Company/Research 팀 등)
- `.env`에 `SR_COMPANY_ID` 및 모든 에이전트 ID 저장
- `.claude/commands/*.md`의 에이전트 ID 플레이스홀더 실제 ID로 교체
- `CLAUDE.md`의 플레이스홀더 교체

> 이미 실행했다면 재실행해도 안전합니다 (기존 회사·에이전트 재사용).

---

### 5. 인프라 키 파일 설정

```bash
cp INFRA.example.md INFRA.md
```

`INFRA.md`를 열고 DART, ECOS, FRED API 키를 실제 값으로 교체합니다.
이 파일은 `.gitignore`에 포함되어 있어 커밋되지 않습니다.

---

### 6. Python 패키지 설치 (데이터 수집용)

```bash
pip3 install dart-fss pykrx yfinance pandas requests python-dotenv
```

---

## 전체 체크리스트

- [ ] `pnpm install && pnpm --filter @paperclipai/plugin-sdk build`
- [ ] `.env` 작성 완료 (JWT 시크릿 + API 키 3개)
- [ ] `pnpm dev` 정상 실행 확인
- [ ] `python3 scripts/bootstrap.py` 완료
- [ ] `INFRA.md` 작성 완료
- [ ] Python 패키지 설치 완료
- [ ] Claude Code에서 `/company_analysis 삼성전자` 테스트

---

## API 키 발급 방법

| 키 | 발급 URL | 소요 시간 |
|----|----------|-----------|
| DART | https://opendart.fss.or.kr/ | 즉시 |
| ECOS | https://ecos.bok.or.kr/ | 1-2일 |
| FRED | https://fred.stlouisfed.org/docs/api/api_key.html | 즉시 |
