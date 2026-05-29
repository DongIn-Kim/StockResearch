# SR Research Centre

AI 에이전트 기반 주식 리서치 + 학술연구 플랫폼.

18명의 전문 에이전트가 저평가 섹터/기업을 발굴하고, 심층 분석 리포트를 작성합니다.
별도 Quantitative Finance Lab 팀이 계량경제학·금융공학 기반 학술 논문을 작성합니다.

## 빠른 시작

```bash
# 1. 의존성 설치 + 빌드
pnpm install && pnpm --filter @paperclipai/plugin-sdk build

# 2. 환경변수 설정
cp .env.example .env   # API 키 입력 후 저장

# 3. 서버 실행
docker compose -f docker/docker-compose.yml up -d
pnpm dev

# 4. 회사·에이전트 자동 생성 (최초 1회)
python3 scripts/bootstrap.py

# 5. 인프라 키 설정
cp INFRA.example.md INFRA.md   # API 키 입력 후 저장
```

이후 Claude Code에서 바로 사용:
```
삼성전자 기업분석 해줘
/company_analysis LG화학
/sector_analysis 반도체
/academic_paper 부도확률 예측 모델
```

서버: `http://localhost:3100` (API + UI) | 자세한 설정: [SETUP.md](SETUP.md)

> 요구사항: Node.js 20+, pnpm 9.15+, Python 3.9+, Docker

## 프로젝트 구조

```
server/          Express 5 API + WebSocket
ui/              React 19 + Vite 6 + Tailwind 4 SPA
cli/             에이전트 오케스트레이션 CLI
packages/db/     Drizzle ORM + embedded PostgreSQL
packages/adapters/  AI 모델 어댑터 (claude-local, gemini 등)
packages/shared/ 공유 타입/상수
skills/          에이전트 스킬 정의
workspace/       리서치 산출물 (스크리닝, 섹터분석, 기업분석, 매크로)
doc/             내부 개발 문서
docs/            사용자 문서
```

## 주요 명령어

```bash
pnpm dev              # 개발 서버 (API + UI, watch mode)
pnpm build            # 전체 빌드
pnpm typecheck        # 타입 검사
pnpm test:run         # 테스트 실행
pnpm db:generate      # DB migration 생성
pnpm db:migrate       # migration 적용
```

## 워크플로우

### 리서치 워크플로우 (3단계)

| 단계 | 내용 |
|------|------|
| **STEP 1** | 저평가 섹터 발굴 → 리뷰 → 보드가 섹터 선택 |
| **STEP 2** | 섹터 내 저평가 기업 발굴 → 리뷰 → 보드가 기업 선택 |
| **STEP 3** | 심층 분석 + 산업/기업 리포트 → 리뷰 → 최종 보고 |

### 학술연구 워크플로우 (Quantitative Finance Lab)

```
/academic_paper <주제>
```

| 단계 | 담당 |
|------|------|
| 연구 설계·가설 정형화 | Principal Investigator |
| 데이터 수집·계량분석 | Econometrician |
| 금융공학 모델 개발 | Financial Engineer |
| IMRaD 논문 초안 작성 | Research Associate |
| 동료 검토 | Scientific Reviewer |
| 최종 수정 | Research Associate |

## 팀 구성

### 리서치팀 (13명)
- **Head of Research** — 전체 총괄·승인
- **산업분석팀** (4명) — Sector, Market, Tech, Policy & ESG Analyst
- **기업분석팀** (3명) — Company, Business, Finance Analyst
- **공통 지원** (4명) — Macro, Quant, Report Writer, Review Analyst / IT Support

### Quantitative Finance Lab (5명)
- **Principal Investigator** — 연구 총괄·설계
- **Econometrician** — 계량경제 분석
- **Financial Engineer** — 금융공학 모델
- **Research Associate** — 논문 집필
- **Scientific Reviewer** — 동료 검토

자세한 내용은 [CLAUDE.md](CLAUDE.md) 참조.

## 개발 가이드

[doc/DEVELOPING.md](doc/DEVELOPING.md) 참조.

## License

MIT
