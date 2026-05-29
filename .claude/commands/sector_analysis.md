산업(섹터) 분석 이슈를 생성하고 Head of Research에게 위임합니다.

## 인수 형식

```
/sector_analysis <섹터명> [| <추가 지시사항>]
```

**예시:**
- `/sector_analysis 반도체`
- `/sector_analysis 2차전지 | 중국 경쟁 환경 심층 포함, 1.1배 분량`
- `/sector_analysis 바이오·제약 | 임상 파이프라인 분석 중점`

---

## 실행 절차

인수: `$ARGUMENTS`

### 1단계 — 인수 파싱

- `|` 앞부분: 섹터명
- `|` 뒷부분: 추가 지시사항 (없으면 빈 문자열)

### 2단계 — 섹터 슬러그 결정

섹터명을 영문 소문자 슬러그로 변환한다:

| 섹터명 예시 | 슬러그 |
|------------|--------|
| 반도체 | it-semiconductor |
| 2차전지 | energy-battery |
| 바이오·제약 | healthcare-bio |
| 금융 | financials |
| 에너지·화학 | energy-chemicals |
| 자동차 | auto-mobility |
| 건설·부동산 | construction-realestate |
| 소비재 | consumer-staples |
| 통신 | it-telecom |
| 전기장비·중공업 | industrials-electrical |

슬러그 형식: `{대분류}-{세분류}` (예: `industrials-electrical`)

### 3단계 — 저장 경로 결정

- 오늘 날짜: `date +%Y-%m-%d` 명령으로 확인
- 폴더 경로: `$(git rev-parse --show-toplevel)/workspace/sectors/YYYY-MM-DD_{슬러그}/`

### 4단계 — Paperclip 이슈 생성 및 Head of Research 배정

```bash
TODAY=$(date +%Y-%m-%d)
SECTOR_PATH="$(git rev-parse --show-toplevel)/workspace/sectors/${TODAY}_{슬러그}"

# 이슈 생성
ISSUE_ID=$(curl -s -X POST http://127.0.0.1:3100/api/companies/${SR_COMPANY_ID}/issues \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"{섹터명} 섹터 산업분석 In-Depth\",
    \"description\": \"[5단계에서 생성]\",
    \"status\": \"todo\",
    \"priority\": \"high\"
  }" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

# Head of Research 배정
curl -s -X PATCH "http://127.0.0.1:3100/api/issues/$ISSUE_ID" \
  -H "Content-Type: application/json" \
  -d '{"assigneeAgentId": "YOUR_HEAD_OF_RESEARCH_AGENT_ID"}'
```

### 5단계 — 이슈 Description 템플릿

```markdown
## 분석 대상

- **섹터**: {섹터명}
- **분석 트랙**: Track A (In-Depth) — 신규 섹터 커버
- **저장 경로**: `{SECTOR_PATH}/`

## 특별 요구사항

{추가 지시사항이 있으면 여기에 기재. 없으면 "표준 In-Depth 섹터 리포트"}

## 기본 분석 범위

### Sector Analyst (총괄)
- 섹터 스탠스(Overweight/Neutral/Underweight) + 탑픽 + 비교 테이블
- 밸류에이션 멀티플 적정 범위 및 트리거

### Market Analyst
- 산업 구조(공급망·수급·가격), 글로벌 트레이드 플로우
- 국내 주요 플레이어 포지셔닝 맵

### Tech Analyst
- 기술 트렌드, 제품 사이클, 신기술 도입 타임라인
- 특허·IP 경쟁 구도

### Policy & ESG Analyst
- 관련 규제·정책 변화, 보조금·관세 이슈
- ESG 규제 리스크 및 기회

### Macro Analyst
- 금리·환율·원자재 가격 민감도
- 경기 사이클 내 섹터 포지션

### Report Writer
- 최종 report.md 작성 → PDF 생성

## 산출물 구조

\`\`\`
{SECTOR_PATH}/
├── report.md
├── appendix.md
├── market/
│   ├── market-analysis.md
│   └── charts/specs/
├── tech/
│   ├── tech-analysis.md
│   └── charts/specs/
├── policy/
│   ├── policy-analysis.md
│   └── charts/specs/
└── data/
    ├── raw/
    └── processed/
\`\`\`
```

### 6단계 — 결과 보고

사용자에게 간결하게 보고:
- 생성된 이슈 번호 (SRR-XXX)
- 섹터명, 슬러그, 저장 경로
- 특별 요구사항 반영 여부
- Head of Research 배정 완료
