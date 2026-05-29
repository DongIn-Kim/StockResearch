학술 연구 논문 이슈를 생성하고 Principal Investigator에게 위임합니다.

## 인수 형식

```
/academic_paper <연구 주제 또는 제목> [| <추가 지시사항>]
```

**예시:**
- `/academic_paper 부도확률 예측 모델`
- `/academic_paper 재무지표 기반 알파 팩터 | IQC 출전용, 백테스팅 포함`
- `/academic_paper 유명인 SNS 텍스트와 주가 반응 | SSRN 워킹페이퍼 수준`
- `/academic_paper 공매도 금지 규제와 가격 효율성 — 한국 시장 RDD 분석`

---

## 실행 절차

인수: `$ARGUMENTS`

### 1단계 — 인수 파싱

`$ARGUMENTS`를 다음 규칙으로 파싱한다:
- `|` 앞부분: 연구 주제 또는 논문 제목 (영문 허용)
- `|` 뒷부분: 추가 지시사항 (없으면 빈 문자열)
- `|` 구분자가 없으면 전체가 연구 주제

### 2단계 — 슬러그 및 저장 경로 결정

- 오늘 날짜: `date +%Y-%m-%d` 명령으로 확인
- 슬러그: 연구 주제를 영문 소문자 + 하이픈으로 변환 (예: `pd-prediction-nlp`)
- 폴더 경로: `$(git rev-parse --show-toplevel)/workspace/research/YYYY-MM-DD_{슬러그}/`

### 3단계 — Paperclip 이슈 생성

```bash
TODAY=$(date +%Y-%m-%d)
SLUG="{슬러그}"
REPORT_PATH="$(git rev-parse --show-toplevel)/workspace/research/${TODAY}_${SLUG}"

curl -s -X POST http://127.0.0.1:3100/api/companies/${SR_COMPANY_ID}/issues \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"[Academic] {연구 주제}\",
    \"description\": \"[이슈 description — 4단계에서 생성]\",
    \"status\": \"todo\",
    \"priority\": \"high\"
  }"
```

### 4단계 — 이슈 Description 작성

아래 템플릿으로 description을 작성한다. `{추가 지시사항}`이 있으면 **특별 요구사항** 섹션에 반영:

```markdown
## 연구 개요

- **주제**: {연구 주제}
- **저장 경로**: `{REPORT_PATH}/`
- **목표 산출물**: 학술 논문 초안 (IMRaD 구조)

## 특별 요구사항

{추가 지시사항이 있으면 기재. 없으면 "표준 학술 논문 (SSRN 워킹페이퍼 수준)"}

## 연구 수행 절차

### Phase 1 — 연구 설계 (Principal Investigator + Econometrician)
- 연구 질문 정형화 및 가설 설계
- 선행 연구 탐색 및 연구 공백 확인
- 데이터 소스 확정 및 수집 계획
- 식별 전략 설계 (내생성 문제 해결)
- 연구 계획서 작성 (`ideation/research-proposal.md`)

### Phase 2 — 데이터 수집 및 분석 (Econometrician + Financial Engineer)
- 데이터 수집 및 전처리 (원본 출처 CSV 주석 필수)
- 기초 통계 (Table 1)
- 주요 분석 실행 (베이스라인 + 로버스트니스)
- 시각화 (그림 + 표)

### Phase 3 — 논문 작성 (Research Associate)
- IMRaD 구조 초안 작성
- 표/그림 포맷팅 (저널 기준)
- 참고문헌 정리 (BibTeX)

### Phase 4 — 동료 검토 (Scientific Reviewer)
- 방법론 타당성 검증
- 결과 해석 적절성 확인
- 수정 제안 → Research Associate 반영

## 산출물 구조

\`\`\`
{REPORT_PATH}/
├── ideation/
│   ├── topic-memo.md              ← 연구 아이디어 메모
│   ├── literature-map.md          ← 선행 연구 요약
│   └── research-proposal.md      ← 연구 계획서
├── paper/
│   ├── draft.md                   ← 논문 초안 (IMRaD)
│   ├── appendix.md                ← 부록
│   └── references.bib             ← 참고문헌
├── analysis/
│   ├── main_analysis.py           ← 주분석 코드
│   ├── robustness.py              ← 로버스트니스
│   └── figures/                   ← 차트
├── tables/
│   ├── table1_summary.csv
│   └── table2_baseline.csv
└── data/
    ├── raw/                       ← 원본 (출처 주석 필수)
    └── processed/                 ← 가공 데이터
\`\`\`

## 진행 순서 (Principal Investigator 조율)

1. Principal Investigator → 연구 설계 + 가설 정형화
2. Econometrician → 데이터 수집 + 계량분석
3. Financial Engineer → 금융공학 모델 (해당 시)
4. Research Associate → 논문 초안 작성
5. Scientific Reviewer → 동료 검토 + 피드백
6. Research Associate → 최종 수정
```

### 5단계 — Principal Investigator에게 배정

이슈 생성 후 즉시 Principal Investigator에게 배정한다:

```bash
curl -s -X PATCH "http://127.0.0.1:3100/api/issues/{생성된_이슈_ID}" \
  -H "Content-Type: application/json" \
  -d '{"assigneeAgentId": "YOUR_PRINCIPAL_INVESTIGATOR_AGENT_ID"}'
```

### 6단계 — 결과 보고

사용자에게 다음을 보고한다:
- 생성된 이슈 번호 (SRR-XXX)
- 연구 주제, 저장 경로
- 특별 요구사항 반영 여부
- 배정된 에이전트 확인
