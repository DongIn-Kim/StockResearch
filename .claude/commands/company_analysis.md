기업분석 이슈를 생성하고 Head of Research에게 위임합니다.

## 인수 형식

```
/company_analysis <회사명> [| <추가 지시사항>]
```

**예시:**
- `/company_analysis 삼성전자`
- `/company_analysis LG화학 | 1.1배 분량, 배터리 사업부 중점`
- `/company_analysis 카카오뱅크 (323410) | 핀테크 경쟁 환경 심층 분석 포함`

---

## 실행 절차

인수: `$ARGUMENTS`

### 1단계 — 인수 파싱

`$ARGUMENTS`를 다음 규칙으로 파싱한다:

- `|` 앞부분: 회사명 (+ 선택적으로 괄호 안에 티커 코드 포함 가능)
  - 예: `삼성전자` → 회사명=삼성전자
  - 예: `LG화학 (051910)` → 회사명=LG화학, 티커=051910
- `|` 뒷부분: 추가 지시사항 (없으면 빈 문자열)
- `|` 구분자가 없으면 전체가 회사명

### 2단계 — 티커 및 공식 회사명 확인 (⚠️ pykrx 필수)

티커를 특정한 후 **반드시 pykrx로 공식 회사명을 조회**한다. 사용자 입력값·내부 지식으로 회사명을 결정하지 않는다.

```python
import warnings; warnings.filterwarnings("ignore")
from pykrx import stock

# 티커가 명시된 경우 그대로 사용, 없으면 아래로 검색
TICKER = "105560"  # 예시

# ① 공식 회사명 조회 (이 값만 회사명으로 사용)
OFFICIAL_NAME = stock.get_market_ticker_name(TICKER)
print(f"공식 회사명: {OFFICIAL_NAME}")  # 예: "KB금융"

# ② 현재가 조회 — 날짜 명시 필수
import datetime
today = datetime.date.today().strftime("%Y%m%d")
df = stock.get_market_ohlcv(today, today, TICKER)
if df.empty:
    # 장 마감 전이거나 휴장일이면 전 거래일 기준
    prev = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    df = stock.get_market_ohlcv(prev, prev, TICKER)
    price_date = prev
else:
    price_date = today
current_price = int(df["종가"].iloc[-1])
print(f"현재가: {current_price:,}원 ({price_date[:4]}-{price_date[4:6]}-{price_date[6:]} 종가 기준)")
```

- 티커 미명시 시: DART corp_list에서 검색하거나 사용자에게 확인
- `OFFICIAL_NAME`이 빈 문자열이면 사용자에게 티커 재확인 요청
- **현재가는 반드시 `YYYY-MM-DD 종가 기준`으로 리포트에 명시**

### 3단계 — 저장 경로 및 날짜 결정

- 오늘 날짜: `date +%Y-%m-%d` 명령으로 확인
- 폴더 경로: `$(git rev-parse --show-toplevel)/workspace/companies/YYYY-MM-DD_{티커}_{회사명}/`

### 4단계 — Paperclip 이슈 생성

아래 curl 명령으로 이슈를 생성한다:

```bash
TODAY=$(date +%Y-%m-%d)
REPORT_PATH="$(git rev-parse --show-toplevel)/workspace/companies/${TODAY}_{티커}_{회사명}"

curl -s -X POST http://127.0.0.1:3100/api/companies/${SR_COMPANY_ID}/issues \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"{티커} {회사명} 기업분석 Initiation\",
    \"description\": \"[이슈 description — 5단계에서 생성]\",
    \"status\": \"todo\",
    \"priority\": \"high\"
  }"
```

### 5단계 — 이슈 Description 작성

아래 템플릿을 기반으로 description을 작성한다. `{추가 지시사항}`이 있으면 **특별 요구사항** 섹션에 반영한다:

```markdown
## 분석 대상

- **종목**: {OFFICIAL_NAME} ({티커}, KOSPI/KOSDAQ)  ← pykrx 조회값 사용
- **현재가**: {current_price}원 ({price_date} 종가 기준)  ← 반드시 날짜 명시
- **분석 트랙**: Track A (Initiation) — 커버리지 신규 개시
- **저장 경로**: `{REPORT_PATH}/`

## 특별 요구사항

{추가 지시사항이 있으면 여기에 기재. 없으면 "표준 Initiation 리포트"}

## 기본 분석 범위

### 사업 분석 (Business Analyst)
- 핵심 사업부별 경쟁 포지셔닝, 시장 지위
- 경영진 전략 방향, M&A/투자 이력
- Value chain, 고객·공급업체 관계

### 재무 분석 (Finance Analyst)
- P&L / B/S / CF 3개년 추이 + 2개년 예측
- 분기별 실적 전망표 (사업부별 QoQ/YoY 분해)
- ROE 추이 + Peer 비교, ROIC vs WACC 스프레드
- 컨센서스(FnGuide) 대비 당사 추정치 비교

### 기술 분석 (Tech Analyst)
- 핵심 기술 로드맵 및 특허 포지션
- 제품 경쟁력, R&D 투자 대비 성과
- 기술 차별화 지속 가능성

### 시장 분석 (Market Analyst)
- 산업 구조(공급망, 수급), 글로벌 가격 트렌드
- 주요 지역별 수요 동향

### 종합·밸류에이션 (Company Analyst)
- 위 분석 종합 + 투자 테제 수립
- 밸류에이션: SOTP 또는 Target Multiple (사업 특성에 따라 선택)
- 목표주가, 투자의견

## 산출물 구조

\`\`\`
{REPORT_PATH}/
├── report.md               ← 메인 리포트
├── appendix.md             ← 재무 부록
├── valuation.md            ← 밸류에이션 상세
├── business/
│   ├── business-analysis.md
│   └── charts/specs/
├── finance/
│   ├── finance-analysis.md
│   ├── financial-model.csv
│   └── charts/specs/
└── tech/
    ├── tech-analysis.md
    └── charts/specs/
\`\`\`

## 진행 순서 (Head of Research 조율)

1. Business Analyst → 사업부별 정성 분석 + 경쟁 포지셔닝
2. Finance Analyst → 재무 모델 + 분기 전망표
3. Tech Analyst → 기술 로드맵 + 차별화 분석
4. Market Analyst → 시장 구조, 수급, 가격 트렌드
5. Company Analyst → 전체 종합 + 밸류에이션 + 투자의견
6. Report Writer → 최종 report.md 작성 → PDF 생성
7. Review Analyst → 검증 (B등급 이상까지 반복)
```

### 6단계 — Head of Research에게 배정

이슈 생성 후 즉시 Head of Research에게 배정한다:

```bash
curl -s -X PATCH "http://127.0.0.1:3100/api/issues/{생성된_이슈_ID}" \
  -H "Content-Type: application/json" \
  -d '{"assigneeAgentId": "YOUR_HEAD_OF_RESEARCH_AGENT_ID"}'
```

### 7단계 — 결과 보고

사용자에게 다음을 간결하게 보고한다:
- 생성된 이슈 번호 (SRR-XXX)
- 회사명, 티커, 저장 경로
- 특별 요구사항이 반영됐는지 확인
- Head of Research 배정 완료 확인
