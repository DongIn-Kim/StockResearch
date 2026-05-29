---
name: academic-paper-writing
description: >
  계량경제학·금융공학 분야 학술 논문을 IMRaD 구조로 작성하는 스킬. 초록·서론·문헌검토·방법론·
  결과·결론 각 섹션의 학술지 투고 기준 작성 표준, 표/그림 포맷, 인용 방식, 저널 타겟팅을 제공한다.
  어떤 정량적 연구 주제에도 적용 가능하며 SSRN 워킹페이퍼부터 탑저널 투고까지 지원.
---

# Academic Paper Writing

금융경제학 분야 학술 논문 작성 표준 스킬.

## 논문 구조 (IMRaD)

```
Title (제목)
Abstract (초록) — 250단어 이내
1. Introduction (서론)
2. Literature Review (문헌 검토)
3. Data and Methodology (데이터 및 방법론)
   3.1 Data Description
   3.2 Variable Construction
   3.3 Empirical Strategy
4. Empirical Results (실증 결과)
   4.1 Main Results
   4.2 Robustness Checks
   4.3 Mechanism Analysis / Heterogeneity
5. Conclusion (결론)
References (참고문헌)
Appendix (부록) — 선택
```

---

## 섹션별 작성 기준

### Abstract (초록)

**구조:** 4문장 원칙
1. **Background** — 왜 이 주제가 중요한가 (1~2문장)
2. **Method** — 무엇을 어떻게 분석했는가 (1~2문장)
3. **Finding** — 핵심 결과 (1~2문장)
4. **Implication** — 학술적/실무적 의의 (1문장)

**예시 (부도확률 논문):**
```
Corporate default prediction is central to credit risk management, 
yet existing models largely rely on traditional accounting variables. 
Using a novel dataset of 12,847 earnings call transcripts from 2010 to 2023, 
we construct a text-based financial distress indicator (TFDI) 
and integrate it with structural and reduced-form credit risk models. 
A one-standard-deviation increase in TFDI predicts a 23% higher 
one-year default probability, controlling for Altman Z-score and 
market-based distance to default. Our results suggest that managerial 
communication contains incremental information about credit risk 
beyond traditional financial ratios, with implications for 
bond pricing and bank lending decisions.
```

**금지 사항:** "This paper studies..." 로 시작 금지 (진부). 수동태 최소화.

---

### 1. Introduction (서론)

**5단락 구조 (Elton et al. 표준):**

```markdown
**단락 1 — Hook (중요성):**
연구 주제의 경제적·사회적 중요성. 실마리가 될 사실/통계 제시.
예: "Global corporate bond markets exceed $10 trillion, yet..."

**단락 2 — Gap (문제 제기):**
기존 연구의 한계. "However, little is known about..." 또는
"Existing studies have focused on X, but Y remains understudied."

**단락 3 — This Paper (우리의 접근):**
우리가 무엇을 하는가. 데이터, 식별 전략, 핵심 아이디어.
"We address this gap using [novel data/method/setting]..."

**단락 4 — Main Findings (핵심 결과):**
숫자를 포함한 구체적 결과. "We find that X is associated with Y by Z%."
로버스트니스 간략 언급.

**단락 5 — Contribution & Roadmap:**
선행 연구 3~5편과 차별성. 논문 구성 안내.
```

**서론 작성 팁:**
- 5~8페이지 적정 분량 (탑저널 기준)
- 결과를 서론에서 미리 공개 (mystery 소설 금지)
- 테이블 번호 미리 언급: "Table 2 reports..."

---

### 2. Literature Review

**구성 원칙:**
- 단순 요약 나열 금지 → 기존 연구들이 우리 질문과 어떻게 연결되는지 서술
- 3~4개 문헌 스트림으로 분류
- 각 스트림 마지막에 "Our paper differs from this literature by..."

**인용 포맷 (APA / Author-Date):**
```
Merton (1974) proposes a structural model of default...
Consistent with Altman (1968) and Campbell, Hilscher, and Szilagyi (2008)...
Recent studies (Bai, Bali, and Wen 2019; Gu, Kelly, and Xiu 2020) employ...
```

**필수 인용 체크리스트 (주제별):**

**부도확률 모델:**
- Merton (1974) — 구조 모델 원전
- Altman (1968) — Z-Score
- Shumway (2001) — 해저드 모델
- Campbell, Hilscher, Szilagyi (2008) — 시장 기반 PD
- Leland & Toft (1996) — 최적 자본구조

**팩터 모델/알파:**
- Fama & French (1993, 2015) — 3/5팩터
- Carhart (1997) — 모멘텀
- Hou, Xue, Zhang (2015) — q-factor
- Novy-Marx (2013) — 그로스 프로피터빌리티
- Frazzini & Pedersen (2014) — BAB

**텍스트 분석:**
- Tetlock (2007) — 미디어 감성과 주가
- Loughran & McDonald (2011) — 금융 감성 사전
- Buehlmaier & Whited (2018) — 텍스트 기반 재무 제약
- Ke, Kelly, Xiu (2019) — Predicting Returns with Text Data

---

### 3. Data and Methodology

#### 3.1 Data Description

**표준 Table 1 구조 (Summary Statistics):**

```
Table 1. Summary Statistics
Panel A: Main Variables
Variable          | N      | Mean   | Std    | p10    | p25    | Median | p75    | p90
------------------|--------|--------|--------|--------|--------|--------|--------|--------
Default (0/1)     | 15,234 | 0.023  | 0.150  | 0      | 0      | 0      | 0      | 0
Leverage          | 15,234 | 0.412  | 0.213  | 0.112  | 0.248  | 0.402  | 0.572  | 0.693
ROA               | 15,234 | 0.041  | 0.087  | -0.043 | 0.012  | 0.038  | 0.073  | 0.115
[기타 변수...]

Panel B: By Default Status
              | Non-Default (N=14,884) | Default (N=350) | t-stat
Leverage      | 0.398                  | 0.621           | 12.34***
ROA           | 0.043                  | -0.012          | -8.91***
```

**데이터 섹션 필수 기재:**
- 샘플 기간, 국가/시장
- 최종 샘플 도달 과정 (결측값 처리, 필터링 기준 — attrition table)
- 주요 변수 구성 방법 (계산식 명시)
- 데이터 소스별 출처 각주

#### 3.2 Empirical Strategy

**식별 전략 섹션 필수 내용:**
```markdown
## 3.2 Empirical Strategy

Our baseline specification is:

Y_{i,t} = α + β₁X_{i,t} + γControls_{i,t} + μ_i + λ_t + ε_{i,t}    (1)

where Y_{i,t} is [종속변수 설명], X_{i,t} is [주요 독립변수], 
μ_i and λ_t denote firm and year fixed effects, respectively.
Standard errors are clustered at the firm level.

**Identification Concern:** The main threat to identification is [내생성 우려].
We address this by [해결 방법: IV / DiD / RDD / 자연실험].

[IV 사용시] The instrument [Z] satisfies the relevance condition 
(first-stage F-statistic = XX.X, p < 0.001) and the exclusion restriction 
because [경제적 논리].
```

---

### 4. Empirical Results

#### 4.1 회귀 결과 표 포맷

```
Table 2. Baseline Results: Effect of X on Y
                    (1)         (2)         (3)         (4)
                    OLS         OLS         FE          IV
---------------------------------------------------------------
X (주요변수)        0.234***    0.189***    0.156***    0.201***
                   (0.043)     (0.038)     (0.035)     (0.047)

Control A                      0.012*      0.009       0.011
                               (0.007)     (0.007)     (0.007)

Control B                      -0.034**    -0.028**    -0.032**
                               (0.016)     (0.014)     (0.015)

Constant           0.412***    0.356***
                   (0.089)     (0.082)
---------------------------------------------------------------
Firm FE            No          No          Yes         Yes
Year FE            No          No          Yes         Yes
N                  15,234      15,234      15,234      14,891
Adj. R²            0.124       0.198       0.312       —
F-stat (1st stage)                                     43.2
---------------------------------------------------------------
Notes: ***, **, * denote significance at 1%, 5%, 10% levels.
Robust standard errors clustered by firm in parentheses.
Sample: [기간], [시장]. [데이터 소스] 각주.
```

#### 4.2 Robustness Checks 체크리스트

논문 제출 전 반드시 수행:
- [ ] 표준오차 변형: 이중 클러스터링 (firm × year), Newey-West
- [ ] 샘플 변형: 극단값 처리 방법 변경, 다른 기간, 서브샘플
- [ ] 변수 측정 변형: 대안 변수 정의 (예: 레버리지 측정 방식)
- [ ] 대안 모형: 다항식 차수 변경 (RDD), 다른 고정효과 조합
- [ ] Placebo test: 처치 집단/시기를 가짜로 바꿔 유의하지 않음 확인
- [ ] Falsification test: 인과 방향의 역방향이 유의하지 않음 확인

#### 4.3 Mechanism / Heterogeneity Analysis

```markdown
We explore the mechanisms driving our findings...

[채널 분석] If our hypothesis is correct, the effect should be stronger when 
[중개 변수가 높은/낮은 집단].

[이질성 분석] We split the sample by [기업규모/산업/기간] and find...
The coefficient is X.XX in [집단 A] vs. X.XX in [집단 B], 
with the difference statistically significant (p = 0.XXX).
```

---

### 5. Conclusion

**4단락 구조:**
1. 연구 요약 (무엇을 했는가)
2. 핵심 발견 (무엇을 찾았는가) — Introduction과 다른 표현으로
3. 이론적 기여 + 실무적 함의
4. 한계점 + 향후 연구 방향

**한계점 작성 팁:** 한계를 먼저 인정하면 리뷰어가 덜 공격적. "One limitation is that... Future research could..."

---

## 저널 타겟팅 가이드

### A등급 저널 (탑 3)

| 저널 | Impact Factor | 수락률 | 특징 |
|------|---------------|--------|------|
| Journal of Finance (JF) | ~9.0 | ~7% | 이론+실증, 폭넓은 금융 |
| Journal of Financial Economics (JFE) | ~8.5 | ~8% | 기업금융, 자산가격 |
| Review of Financial Studies (RFS) | ~7.5 | ~8% | 최신 방법론 우호 |

### B등급 저널 (첫 투고 타겟)

| 저널 | 특징 |
|------|------|
| Journal of Financial and Quantitative Analysis (JFQA) | 계량 우호 |
| Journal of Banking & Finance (JBF) | 금융 실무 관련 |
| Review of Finance | 유럽, 빠른 리뷰 |
| Pacific-Basin Finance Journal | 아시아 시장 특화 |
| Finance Research Letters | 단편 연구 (3,000단어) |

### 워킹페이퍼 → 컨퍼런스 → 저널 전략

```
1단계: SSRN 업로드 (워킹페이퍼)
   → 피드백 수집, 다운로드 카운트로 관심도 측정

2단계: 컨퍼런스 발표 (6~12개월 후)
   → AFA, WFA, SFS Cavalcade, KFA (한국재무학회)
   → 디스커턴트 피드백으로 논문 개선

3단계: 저널 투고 (컨퍼런스 발표 후)
   → 1지망 → Reject → 2지망 순차 진행
   → R&R (Revise & Resubmit) 시 3개월 내 회신 목표
```

---

## 표/그림 작성 표준

### 표 (Tables)

- 제목: Table N. [결과 설명] (예: Table 3. Robustness Checks)
- 모든 계수 아래에 표준오차를 괄호로 표시
- 유의수준: `***` p<0.01, `**` p<0.05, `*` p<0.10
- Notes 섹션: 클러스터링 방법, 고정효과, 샘플 설명 반드시 포함
- 컬럼 라벨: (1), (2), (3)... 로 일련번호

### 그림 (Figures)

- 제목: Figure N. [그림 설명]
- 축 라벨, 단위 필수 표시
- 범례(legend) 포함
- 해상도: 최소 300 DPI (인쇄용)
- 포맷: PDF 또는 EPS (벡터) 우선, PNG 허용
- 이벤트 스터디: CAR(%) on y-axis, 이벤트일 기준 상대 일수 on x-axis

---

## 산출물 저장 경로

```
/Users/pc/Documents/sr_research_centre/workspace/research/YYYY-MM-DD_{paper-slug}/
├── paper/
│   ├── draft.md              ← 논문 본문 (마크다운)
│   ├── draft.pdf             ← PDF 변환본
│   ├── appendix.md           ← 부록
│   ├── references.bib        ← BibTeX 참고문헌
│   └── revisions/            ← 리비전 이력
│       └── v2_YYYY-MM-DD.md
├── tables/
│   ├── table1_summary.csv    ← 기초 통계
│   ├── table2_baseline.csv   ← 기본 회귀
│   └── ...
└── figures/
    ├── fig1_timeline.png
    ├── fig2_event_study.svg
    └── ...
```

**출처 기록 (REQUIRED):**
```csv
# source: 기관명
# url: https://실제URL
# retrieved: YYYY-MM-DD
```

---

## 완료 후 리뷰 (REQUIRED)

논문 초안 완성 후 Scientific Reviewer에게 동료 검토 서브이슈를 생성한다:

```bash
curl -s -X POST "$PAPERCLIP_API_URL/api/companies/$PAPERCLIP_COMPANY_ID/issues" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID" \
  -d "{
    \"title\": \"[리뷰] 논문 동료 검토 — $(현재이슈제목)\",
    \"description\": \"학술 논문 동료 검토 요청\\n\\n검토 항목:\\n- 연구 설계 타당성\\n- 식별 전략 강도\\n- 결과 해석 적절성\\n- 문헌 충분성\\n- 작성 품질 (명확성, 논리 흐름)\",
    \"status\": \"todo\",
    \"parentId\": \"$PAPERCLIP_TASK_ID\"
  }"
```
