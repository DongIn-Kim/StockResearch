---
name: report-formatting
description: >
  MD 리서치 리포트를 전문 애널리스트 리포트 수준의 PDF/HTML로 변환하는 스킬.
  Report Writer가 report.md 작성 완료 후 호출하여 시각화(차트)와 전문적 레이아웃이 적용된
  최종 산출물을 생성한다. 산업분석(sector-analysis)과 기업분석(company-analysis) 템플릿을 지원.
---

# report-formatting

MD 리서치 리포트를 전문 PDF로 변환하는 스킬.

## 리포트 작성 가이드

report.md 본문 작성 시 아래 가이드를 참조한다. 가이드는 목차·판단 기준·산출물 형식을 정의하며,
산업/기업별 구체 내용은 에이전트가 런타임에 결정한다.

- **산업분석**: `workspace/templates/sector-report-guide.md`
- **기업분석**: `workspace/templates/company-report-guide.md`

## 사용 시점

- Report Writer가 `report.md` 작성을 완료한 후
- Head of Research가 최종 산출물 포맷팅을 지시할 때
- Review Analyst가 검토 완료 후 최종 배포용 PDF를 요청할 때

## 사전 조건

리포트 디렉토리에 다음 파일이 존재해야 한다:
- `report.md` — 리포트 본문 (필수)
- `data/processed/*.csv` — 차트 생성용 가공 데이터 (선택, 있으면 자동 차트 생성)
- `data/raw/*.csv` — 원본 데이터 (선택)

## 실행 방법

### 변환 명령어

```bash
# 산업분석 리포트 → PDF
/Users/pc/Documents/sr_research_centre/workspace/templates/scripts/format-report.sh \
  <report-directory> \
  sector-analysis \
  pdf

# 기업분석 리포트 → PDF
/Users/pc/Documents/sr_research_centre/workspace/templates/scripts/format-report.sh \
  <report-directory> \
  company-analysis \
  pdf

# HTML만 생성 (차트 확인용)
/Users/pc/Documents/sr_research_centre/workspace/templates/scripts/format-report.sh \
  <report-directory> \
  sector-analysis \
  html

# HTML + PDF 모두 생성
/Users/pc/Documents/sr_research_centre/workspace/templates/scripts/format-report.sh \
  <report-directory> \
  sector-analysis \
  both
```

### report-directory 경로 규칙

- **절대 경로** 또는 **workspace/ 기준 상대 경로** 모두 지원
- 산업분석: `sectors/{sector-slug}/YYYY-MM-DD_{report-type}/`
- 기업분석: `companies/{ticker}_{name}/YYYY-MM-DD_{report-type}/`
- 스크리닝: `screening/YYYY-MM-DD_{screen-name}/`

### 예시

```bash
# 기존 섹터 스크리닝 결과 포맷팅
/Users/pc/Documents/sr_research_centre/workspace/templates/scripts/format-report.sh \
  /Users/pc/Documents/sr_research_centre/workspace/screening/2026-04-05_sector-valuation \
  sector-analysis \
  pdf
```

## 템플릿 유형

### sector-analysis (산업분석)

**적용 대상:** 섹터 스크리닝, 산업 분석, 섹터 비교 리포트

**자동 생성 차트:**
- 섹터별 밸류에이션 비교 (Fwd PER + PBR 가로 바 차트)
- PER vs PBR 산점도 (Tier별 색상 구분)
- 복합 스코어 분포 (색상 코딩된 바 차트)

**필요한 CSV 컬럼 (data/processed/):**
- `sector`, `fwd_per`, `pbr_current`, `composite_score`, `recommendation`
- 추가 권장: `pbr_5y_pctile`, `per_5y_pctile`, `roe_trend`, `value_trap_flag`

### company-analysis (기업분석)

**적용 대상:** 기업 initiation, 기업 업데이트, 기업 심층 분석 리포트

**자동 생성 차트:**
- 실적 추이 (매출/영업이익 바 + 영업이익률 라인)
- 밸류에이션 밴드 (주가 + PER 밴드)
- 동종업계 비교 레이더 차트
- 매출 구성 (도넛 차트) — `revenue_mix.csv` 존재 시
- 시나리오별 목표주가 비교 (그룹 바 차트) — `scenarios.csv` 존재 시
- 민감도 분석 히트맵 — `sensitivity.csv` 존재 시

**필요한 CSV:**
- `data/raw/financials.csv` — 실적 데이터 (revenue, operating_profit, op_margin)
- `data/raw/peer_comparison.csv` — 동종업계 비교 지표
- `data/processed/dcf_model.csv` — DCF 모델 (선택)
- `data/processed/revenue_mix.csv` — 매출 구성 (선택, 컬럼: segment, revenue)
- `data/processed/scenarios.csv` — 시나리오 비교 (선택, 컬럼: metric, bull, base, bear)
- `data/processed/sensitivity.csv` — 민감도 매트릭스 (선택, 첫 열: Y축 라벨, 나머지 열: X축 값)

## 산출물

| 파일 | 설명 |
|------|------|
| `report.html` | 스타일이 적용된 HTML (브라우저에서 열 수 있음) |
| `report.pdf` | A4 PDF (Chrome headless로 생성) |

## 변환 파이프라인

```
report.md + data/*.csv
       ↓
csv-to-chartdata.py → chart-data.json
       ↓
pandoc --template → report.html (+ 차트 데이터 인라인)
       ↓
Chrome headless --print-to-pdf → report.pdf
```

## 커스터마이징

### 메타데이터 오버라이드

report.md 상단에 YAML frontmatter를 추가하면 자동 감지된 메타데이터를 오버라이드할 수 있다:

**산업분석 frontmatter:**
```yaml
---
title: "2026년 금융 섹터 투자 전략"
author: "Sector Analyst"
date: "2026-04-05"
sector: "금융(은행/증권/보험)"
rating: "Overweight"
rating-class: "buy"
confidence: "8.5"
summary: "금융 섹터는 역사적 저평가 구간에 진입하였으며..."
---
```

**기업분석 frontmatter:**
```yaml
---
title: "삼성전자 — Initiation of Coverage"
author: "Sector Analyst"
date: "2026-04-05"
company: "삼성전자"
ticker: "005930.KS"
sector: "반도체/IT하드웨어"
rating: "BUY"
rating-class: "buy"
target-price: "95,000원"
current-price: "72,000원"
upside: "+31.9%"
confidence: "8.0"
summary: "AI/HBM 수퍼사이클 수혜 + 파운드리 턴어라운드 기대"
---
```

### 새 템플릿 추가

1. `templates/` 디렉토리에 `{type-name}.html` 파일 생성 (pandoc 템플릿 문법)
2. `csv-to-chartdata.py`에 해당 타입의 차트 생성 함수 추가
3. `format-report.sh`는 자동으로 새 템플릿 인식

## 의존성

- `pandoc` >= 3.0 (brew install pandoc)
- `python3` (표준 라이브러리만 사용: csv, json, os, sys)
- Google Chrome (PDF 변환용, headless 모드)
