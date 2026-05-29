---
name: research-ideation
description: >
  학술 연구 주제를 발굴하고 연구 가설을 설계하는 스킬. 최근 시사 이슈·시장 이상현상·정책 변화에서
  연구 공백을 발견하고, 계량경제학·금융공학으로 검증 가능한 가설로 변환한다. 어떤 금융·경제
  주제에도 적용 가능하며, 데이터 가용성·방법론 적합성·학술적 기여도를 함께 평가한다.
---

# Research Ideation

시사 이슈 → 연구 공백 발견 → 검증 가능한 학술 연구 가설로 변환하는 스킬.

## 연구 주제 발굴 프레임워크

### Phase 1: 신호 포착 (Signal Detection)

시사 이슈에서 연구 가능한 신호를 포착하는 채널:

| 채널 | 유형 | 예시 |
|------|------|------|
| 시장 이상현상 | 설명 안 된 수익률 패턴 | 특정 이벤트 후 주가 드리프트 |
| 정책/규제 변화 | 외생적 충격 (자연실험) | 금리 정책 변화, 공시 규정 강화 |
| 기술 변화 | 새로운 데이터 소스 | 소셜 미디어 감성, 위성 데이터 |
| 학계 최신 논문 | 방법론 개선 여지 | 선행 연구의 미해결 한계 |
| 글로벌 이슈 | 크로스컨트리 비교 | 팬데믹, 금융위기의 국가별 영향 |

### Phase 2: 연구 공백 식별 (Gap Analysis)

연구 아이디어를 평가하는 5가지 질문:
1. **What's new?** — 기존 연구와 무엇이 다른가? (새 데이터, 새 방법론, 새 시장, 새 기간)
2. **Why now?** — 왜 지금 이 연구가 중요한가?
3. **Who cares?** — 학계/실무자/정책입안자 중 누가 관심을 갖는가?
4. **Can we test it?** — 데이터가 있고 식별 전략이 존재하는가?
5. **Is it publishable?** — 어느 저널을 타겟으로 할 수 있는가?

### Phase 3: 가설 설계 (Hypothesis Design)

**가설 유형:**
- **H1 (존재 가설)**: "X는 Y에 유의한 영향을 미친다"
- **H2 (방향 가설)**: "X의 증가는 Y의 감소와 연관된다"
- **H3 (조절 가설)**: "Z가 높을 때 X→Y 관계가 강해진다"
- **H4 (인과 가설)**: "X는 Y의 원인이다 (외생적 충격 활용)"

**가설 작성 템플릿:**
```
Main Hypothesis:
  [독립변수]의 변화는 [종속변수]에 [방향] 영향을 미친다.
  메커니즘: [경제적/행동재무적 설명]
  
Identification Strategy:
  [외생적 변동의 원천 / 도구변수 / 자연실험]
  
Data:
  - 종속변수: [변수명, 출처, 기간]
  - 독립변수: [변수명, 출처, 기간]
  - 통제변수: [목록]
  
Methodology:
  [OLS / Panel FE / DiD / IV / Event Study / etc.]
  
Target Journal:
  [Journal of Finance / JFE / RFS / JFQ / JBFA / etc.]
```

---

## 주제 발굴 레퍼런스 데이터베이스

### 최근 주요 학술지 논문 트렌드 (검색 키워드)

**JF/JFE/RFS (Top-3) 최근 5년 핫 토픽:**
- Machine learning in asset pricing
- Climate finance / ESG investing  
- FinTech & banking disruption
- Text analysis in finance (CEO speech, earnings call)
- Market microstructure & high-frequency trading
- International finance & currency
- Behavioral biases in institutional investors
- Credit risk & corporate debt markets
- Gender/diversity & corporate outcomes

**검색 소스:**
- SSRN (Social Science Research Network): https://ssrn.com
- Google Scholar: https://scholar.google.com
- NBER Working Papers: https://nber.org/papers
- arXiv (q-fin): https://arxiv.org/list/q-fin/recent

---

## 연구 주제별 아이디어 뱅크

### A. 신용리스크 / 부도확률

| 아이디어 | 핵심 신호 | 방법론 | 데이터 |
|----------|-----------|--------|--------|
| 경영진 언어 패턴과 부도 예측 | IR 자료, 실적발표 음성 | NLP + Logit PD | BigKinds, 전자공시 |
| ESG 등급과 신용스프레드 관계 | ESG 점수 | Panel IV | KIS, NICE |
| 위성 데이터로 기업 실적 선행 예측 | 야간 조명, 주차장 점유율 | ML + Event Study | Descartes Labs |
| 소셜 미디어 불안 지수와 기업 신용위험 | 트위터 감성 | GARCH + Granger | Twitter API |
| 공급망 연결성과 전염 부도위험 | SCM 네트워크 | Network Analysis + Panel | DART, 관세청 |

### B. 팩터 모델 / 알파 발굴

| 아이디어 | 핵심 신호 | 방법론 | 데이터 |
|----------|-----------|--------|--------|
| 특허 출원 모멘텀 팩터 | 특허 건수/질 | Long-Short Portfolio | KIPRIS |
| CEO 트위터 활동과 정보 비대칭 | 트윗 빈도/감성 | Event Study + IV | Twitter API |
| 국민연금 수급 변화와 주가 | 연금 포트폴리오 공시 | DiD | 국민연금 공시 |
| 공매도 금지 전후 가격 효율성 | 공매도 데이터 | RDD | KRX |
| 기업설명회 참석자 이동성 (GPS) | 위치 데이터 | Panel IV | 통신사 데이터 |

### C. 텍스트 / 대안 데이터 기반

| 아이디어 | 핵심 신호 | 방법론 | 데이터 |
|----------|-----------|--------|--------|
| 유명 투자자 발언과 시장 반응 | 언론 인터뷰 텍스트 | NLP + Event Study | BigKinds, DART |
| 애널리스트 리포트 어조와 수익 예측 오차 | 리포트 감성 | NLP + Panel | FnGuide |
| 국회 발언 감성과 정책 불확실성 | 국회 회의록 | LDA + VAR | 국회 OpenAPI |
| 기업 공시 복잡성과 정보 비대칭 | Fog Index | Readability + Panel | DART |
| 소셜미디어 밈 주식 현상 분석 | Reddit/커뮤니티 | Network + GARCH | 크롤링 |

---

## 연구 실현가능성 평가 매트릭스

각 아이디어를 아래 기준으로 1~5점 평가 후 총점으로 우선순위 결정:

| 기준 | 가중치 | 평가 내용 |
|------|--------|-----------|
| 데이터 가용성 | 30% | 수집 가능, 충분한 관측치 |
| 식별 전략 강도 | 25% | 내생성 문제 해결 방법 존재 |
| 학술적 기여 | 20% | 기존 연구와 차별성 |
| 실무 관련성 | 15% | 투자자/정책입안자에게 유용 |
| 완성 기간 | 10% | 6개월 내 완성 가능 |

**총점 해석:** 4.0+ → 즉시 착수, 3.0~3.9 → 데이터 사전 탐색 후 결정, 3.0 미만 → 보류

---

## 선행 연구 기반 연구 설계 SOP (Literature-Driven Research Design)

학술 논문의 가장 강력한 접근법은 **기존 연구의 한계를 기술 발전으로 해소**하는 것이다.
"기존 연구를 참고하되 완전히 똑같이는 하지 않는다" — 기여 포인트는 반드시 있어야 한다.

### Step 1. 핵심 선행 연구 발굴

**검색 전략**:
```
Google Scholar (scholar.google.com):
  - 주제 키워드 검색: "default prediction" OR "credit risk" site:ssrn.com
  - 인용수 기준 정렬 → 상위 10편을 핵심 논문으로 선정
  - "Cited by N" 클릭 → 최신 후속 연구 파악
  - 검색 필터: since:2020 → 최근 트렌드 파악

SSRN (ssrn.com):
  - 주제 검색 → Abstract downloads 순 정렬
  - 최근 6개월 업로드 논문: 미출판 선행 연구 파악

NBER (nber.org/papers):
  - 거시·금융 주제 working papers

arXiv q-fin (arxiv.org/list/q-fin/recent):
  - ML·계량 기법 최신 논문

한국 저널:
  - 한국금융학회 (journal.kafa.or.kr)
  - RISS (riss.kr): 국내 학위논문 포함
```

**핵심 논문 선별 기준** (아래 중 2개 이상 충족):
- Google Scholar 인용수 500+ (2015년 이전 논문)
- JF/JFE/RFS/JFQA 게재
- 주제의 방법론적 출발점이 되는 논문 (seminal paper)
- 2022년 이후 → 인용수 50+ 또는 SSRN downloads 1,000+

---

### Step 2. 한계점 체계적 추출

핵심 논문마다 아래 항목을 표로 정리:

```markdown
| 논문 | 핵심 방법론 | 명시된 한계 | 암묵적 한계 | 발표 연도 |
|------|-----------|-----------|-----------|---------|
| Altman (1968) | 판별분석 Z-Score | 정적 모델, 제조업 편향 | 비선형성 무시, NLP 전무 | 1968 |
| Campbell et al. (2008) | 동적 로짓 | 텍스트 미활용, 미국 한정 | ML 비교 없음, 내생성 미처리 | 2008 |
| ... | ... | ... | ... | ... |
```

**한계 유형 분류**:
- **데이터 한계**: 특정 국가/기간, 특정 산업, 데이터 가용성
- **방법론 한계**: 비선형성 무시, 내생성 미처리, 단순 계량 모델
- **기술 한계**: 사전 기반 NLP → BERT로 대체 가능, 전통 ML → Deep Learning
- **시장 한계**: 미국 중심 → 한국/아시아 적용 미검증
- **기간 한계**: 금융위기 전 데이터 → 코로나/고금리 시기 포함 가능

---

### Step 3. 기술 발전 매핑 (한계 → 해결책)

| 기존 한계 | 해결 기술 | 적용 방법 |
|---------|---------|---------|
| 사전 기반 NLP (LM Dictionary) | BERT 계열 LLM (FinBERT, KoBERT, KLUE) | 문맥 인식 감성 분석 |
| 정적 로짓 모델 | 동적 패널 + ML 앙상블 | XGBoost/LightGBM 비교 |
| 내생성 미처리 | 시차 변수, IV, 의무 공시 외생성 활용 | 2SLS, Lagged spec |
| 미국 데이터 한정 | 한국 KRX/DART 데이터 | 새로운 시장 기여 |
| 단일 모델 비교 없음 | Bakeoff 프레임워크 | 체계적 모델 비교 표 |
| 경제적 유의성 미검증 | 포트폴리오 백테스팅 | 롱숏 전략, FF 알파 |
| 이질성 분석 없음 | 서브샘플 + 상호작용항 | 기업규모 × NLP 효과 |

**기술 발전 활용 체크리스트**:
- [ ] LLM/BERT 계열 활용 가능한가? (텍스트 데이터 있을 경우)
- [ ] ML 앙상블로 비선형 패턴 포착 가능한가?
- [ ] 최근 더 긴 기간·더 많은 데이터 사용 가능한가?
- [ ] 더 정교한 식별 전략(자연실험, IV)이 있는가?
- [ ] 한국/아시아 시장 특수성이 새로운 기여점이 되는가?

---

### Step 4. 연구 기여 포지셔닝

기존 연구와 본 연구의 차별점을 문장으로 정형화:

```
"We build on [기존 연구] but differ in three ways:
First, [차별점 1 — 새로운 데이터/시장/기간].
Second, [차별점 2 — 방법론 개선, 특히 기술 발전 활용].
Third, [차별점 3 — 새로운 메커니즘/이질성 분석]."
```

**기여 강도 등급**:
- ★★★ 완전히 새로운 데이터 + 새로운 방법론
- ★★☆ 기존 방법론 + 새로운 시장/데이터
- ★☆☆ 기존 데이터 + 방법론 개선만

→ 탑티어(JF/JFE/RFS) 목표: ★★ 이상 필요

---

### Step 5. 노벨티 검증 (이미 누군가 했는지 확인)

연구 설계 완료 후 아래 검색으로 중복 확인:
```
Google Scholar 검색: "[핵심 방법론] [시장] [기간]"
예: "FinBERT default prediction Korea DART"
예: "BERT bankruptcy prediction Korean firms"

SSRN 검색: 동일 키워드 → 최근 12개월 논문 집중 확인
```

→ 유사 논문 발견 시: 해당 논문이 다루지 못한 추가 차별점 발굴

---

## 시사 이슈 → 연구 가설 변환 SOP

```
1. [시사 이슈 포착]
   - 최근 뉴스, 정책 발표, 시장 이벤트 모니터링
   - "왜 그럴까?" "이것이 가격에 반영됐을까?" 질문

2. [관련 선행 연구 탐색]
   - Google Scholar / SSRN에서 키워드 검색 (위 Step 1 프로세스 적용)
   - 최근 3년 JF/JFE/RFS 논문 확인
   - 한국 시장 특수성 있는지 확인 (제도, 규제, 투자자 구성)

3. [한계점 추출 및 기술 발전 매핑 (위 Step 2~3 적용)]
   - 기존 연구의 명시적·암묵적 한계 표로 정리
   - 최신 기술(LLM, ML, 더 나은 식별전략)로 해소 가능한 한계 선별

4. [데이터 탐색]
   - 필요한 변수 목록 작성
   - 수집 가능한 소스 확인
   - 샘플 수집 → 기초 통계 확인

5. [가설 정형화]
   - 위 "가설 작성 템플릿" 적용
   - 기여 포인트: "We build on X but differ in Y" 형식으로 명확화
   - Principal Investigator에게 리뷰 요청

6. [연구 계획서 작성]
   - 3~5페이지 분량
   - Research Question, Contribution (vs. prior literature), Data, Methodology, Timeline
```

---

## 산출물 저장 경로

```
/Users/pc/Documents/sr_research_centre/workspace/research/YYYY-MM-DD_{paper-slug}/
├── ideation/
│   ├── topic-memo.md          ← 최초 아이디어 메모 (2~3페이지)
│   ├── literature-map.md      ← 선행 연구 요약
│   ├── feasibility-matrix.md  ← 실현가능성 평가
│   └── research-proposal.md  ← 최종 연구 계획서
└── data/
    └── raw/
        └── pilot_sample.csv  ← 초기 데이터 탐색
```
