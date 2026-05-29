# SR Research Centre

- Server: http://127.0.0.1:3100 | Dev: `pnpm dev`
- Company: `YOUR_COMPANY_ID` | Issue prefix: `SRR-*`
- 언어: 전체 한국어 (금융 약어 영문 허용)
- 리서치 아웃풋: `$(git rev-parse --show-toplevel)/workspace/`
- API 키·인프라: `INFRA.example.md` → `INFRA.md` 복사 후 키 입력. (DART, ECOS 등)
- **데이터 수집 효율화**: `workspace/scripts/AGENT_DATA_GUIDE.md` 참고. WebSearch 대신 Python API 우선 사용.
- Git: remote 미연결 — 로컬 작업만 (push/PR 불필요)
- **플랫폼 개선 이력**: `PATCHNOTES.md` 참고. 버그 수정·로직 변경 시 해당 파일에 기록할 것.

## 주요 명령어
- `pnpm dev` — 서버+UI 동시 실행 | `pnpm test:run` — 단위 테스트 | `pnpm typecheck` — 타입 검사
- `pnpm db:generate` — migration 생성 | `pnpm db:migrate` — migration 적용

## 프로젝트 구조
`server/` Express 5 API | `ui/` React 19+Vite | `cli/` 오케스트레이션 | `packages/db/` Drizzle+PG | `packages/adapters/` AI 어댑터

---

## ⚠️ 에이전트 공통 필수 규칙

### 1. 이슈 태그
모든 이슈(루트+서브태스크)에 동일한 프로젝트 슬러그 태그 부착. 예: `pd-prediction`, `alpha-factors`, `celebrity-indicator`.
서브태스크는 부모 태그를 그대로 상속. 태그 형식: 소문자 영문+하이픈.

### 2. 중복 태스크 방지
서브태스크 생성 전 반드시 조회:
`GET /api/companies/{companyId}/issues?parentId={이슈ID}&status=todo,in_progress,done,blocked`
동일 담당자+유사 제목 이슈가 있으면 **새로 만들지 않고 재활용**. checkout 직후 산출물 경로 먼저 확인 후 착수.

### 3. 중간 저장
논리적 단위마다 즉시 파일 저장. heartbeat 종료 전 반드시 이슈 comment에 저장 상태 기록.
단계별: 수집→`data/raw/` / 전처리→`data/processed/` / 분석→`analysis/` / 논문→`paper/draft.md`
**파일 형식 변경 시**: 계획과 다른 형식(예: parquet→CSV)으로 저장한 경우 반드시 이슈 comment에 명시. 후속 단계가 잘못된 형식을 기다리는 것을 방지.

### 4. 컨텍스트 스위칭
`in_progress`=지금 직접 작업 중 / `todo`=서브태스크 대기 중 / `blocked`=외부 블로커.
서브태스크 위임 후 → 부모를 `todo`로 되돌리고 heartbeat 종료 → 다른 이슈 착수 → @mention 받으면 재개.

### 5. 공유 데이터
수집 전 `$(git rev-parse --show-toplevel)/workspace/shared-data/CATALOG.md` 확인.
카탈로그에 있으면 재수집 금지. 신규 수집 시 `shared-data/` 하위 저장 후 CATALOG.md 등록.

### 6. 실제 데이터만 사용 (절대 원칙)
**시뮬레이션·합성 데이터 절대 금지.** 수집 불가 시 즉시 `blocked` 처리 후 IT Support에 보고.
선행 이슈 의존성 있을 때: 선행 이슈가 `done`이 될 때까지 **절대 착수 금지**. "병렬 진행"은 무관한 이슈에만 해당.

### 7. 데이터 최신성
실적·시장 수치: 공개된 가장 최신 수치 사용. 주가·시총: 당일 종가(장 중이면 전일). 이슈 description 수치 복사 금지.
상세 기준: `workspace/templates/company-report-guide.md` 및 `sector-report-guide.md` 참조.

### 8. 기업명·현재가 검증 (기업분석 필수)
- **공식 회사명**: 반드시 `pykrx.stock.get_market_ticker_name(ticker)`로 조회. 사용자 입력값·내부 지식으로 결정 금지.
- **현재가**: `pykrx.stock.get_market_ohlcv()`로 실제 조회 후 **`YYYY-MM-DD 종가 기준`** 명시 필수. 날짜 없는 현재가 기재 금지.
- 폴더명·이슈 제목·리포트 헤더 모두 pykrx 공식 회사명 사용.

---

## 산출물 저장 경로 (절대 경로 필수)

| 유형 | 경로 |
|------|------|
| 스크리닝 | `workspace/screening/YYYY-MM-DD_{name}/` |
| 산업분석 | `workspace/sectors/YYYY-MM-DD_{섹터슬러그}/` |
| 기업분석 | `workspace/companies/YYYY-MM-DD_{티커}_{종목명}/` |
| 매크로 | `workspace/macro/{daily,weekly}/` |
| 학술연구 | `workspace/research/YYYY-MM-DD_{paper-slug}/` |

Raw CSV 첫 3줄: `# source:`, `# url:`, `# retrieved:` 출처 주석 필수. 레지스트리: `workspace/sources.md`
리포트 가이드: `workspace/templates/sector-report-guide.md` / `company-report-guide.md` / `scripts/format-report.sh`

---

## 워크플로우 (3단계)
1. **STEP 1**: 저평가 섹터 발굴 → 리뷰 → 보드 섹터 선택
2. **STEP 2**: 섹터 내 저평가 기업 발굴 → 리뷰 → 보드 기업 선택
3. **STEP 3**: 심층 분석 + 산업/기업 리포트 → 리뷰 → 최종 보고

**STEP 1 결과**: 진행 후 이 줄에 선택 섹터 기록.

---

## 팀 구성

| Agent | Role | 스킬 |
|-------|------|------|
| Head of Research | ceo | 전체 총괄·승인 |
| Macro Analyst | researcher | market-analysis |
| Quant Analyst | researcher | quant-modeling, undervalue-screening |
| Report Writer | general | report-writing |
| Review Analyst | qa | critical-review |
| **IT Support** | general | 패키지·환경변수 전담 |
| Sector Analyst | researcher | sector-research |
| Market Analyst | researcher | sector-research, market-analysis (**공유**) |
| Tech Analyst | researcher | sector-research, market-analysis (**공유**) |
| Policy & ESG Analyst | researcher | sector-research, market-analysis (**공유**) |
| Company Analyst | researcher | equity-valuation |
| Business Analyst | researcher | equity-valuation |
| Finance Analyst | researcher | equity-valuation |
| Principal Investigator | researcher | research-ideation, academic-paper-writing |
| Econometrician | researcher | econometric-analysis |
| Financial Engineer | researcher | financial-engineering, econometric-analysis |
| Research Associate | general | academic-paper-writing |
| Scientific Reviewer | qa | econometric-analysis, academic-paper-writing |

> Agent ID는 플랫폼에서 에이전트 생성 후 발급됩니다. `.claude/commands/` 파일의 `YOUR_*_AGENT_ID` 플레이스홀더를 실제 ID로 교체하세요.

**IT Support 서브이슈 형식** (인프라 블로커 시 직접 해결 말고 위임):
`title: "[IT] <작업 요약>"` / `assigneeAgentId: "YOUR_IT_SUPPORT_AGENT_ID"` / 허용: pip/npm/brew install, .env 추가

---

## 학술연구팀 (Quantitative Finance Lab)

진입 커맨드: `/academic_paper <주제>`

**워크플로우**: PI(설계) → Econ+FE 병렬(데이터+모델) → PI(결과 취합) → RA(IMRaD 초안) → SR(동료 검토) → RA(수정본)

**논문 작성 가이드**: `workspace/templates/academic-paper-guide.md` — PAP→검증→집필→1회 체크리스트 리뷰 프로세스. **착수 전 반드시 읽을 것.**

**산출물**: `workspace/research/YYYY-MM-DD_{slug}/` 하위 `ideation/` `data/` `code/` `analysis/` `results/` `tables/` `figures/` `paper/`
