---
name: econometric-analysis
description: >
  계량경제학 기법을 사용한 실증 연구 설계 및 분석 스킬. 회귀분석, 패널 데이터, 시계열,
  인과추론(DiD, RDD, IV), 이벤트 스터디, ML 기반 변수 선택 등 학술 논문 수준의 실증분석을
  수행한다. 금융·경제 데이터 분석에 특화되어 있으나 모든 정량적 사회과학 주제에 적용 가능.
---

# Econometric Analysis

학술 논문 수준의 계량경제학 실증분석을 수행하는 스킬.

## 분석 설계 원칙

1. **연구 질문 → 식별 전략** 순서로 접근. 데이터가 있다고 모든 방법론이 유효하지 않음
2. 인과추론(causality) vs. 상관관계(correlation) 목적을 명확히 구분
3. 가정(assumption) 검증을 방법론 적용 전에 반드시 수행
4. 내생성(endogeneity) 문제 식별 → 해결책 제시 (IV, 고정효과, 자연실험 등)
5. 표준오차(SE) 방식은 데이터 구조에 맞게 선택 (clustered, HAC, robust 등)

---

## 방법론 레퍼토리

### 1. 기초 회귀 분석

| 방법 | 적용 상황 | Python | R |
|------|-----------|--------|---|
| OLS | 기본 선형 관계 | `statsmodels.OLS` | `lm()` |
| WLS | 이분산성 존재 | `statsmodels.WLS` | `lm(weights=)` |
| GLS | 오차 상관 구조 | `statsmodels.GLS` | `gls()` in nlme |
| Logit/Probit | 이진 종속변수 | `statsmodels.Logit/Probit` | `glm(family=binomial)` |
| Tobit | 절단 데이터 | `linearmodels` | `censReg` |
| Quantile Reg | 분위수 효과 | `statsmodels.QuantReg` | `quantreg` |

**표준오차 선택 기준:**
- 이분산: `HC3` (robust)
- 패널 내 상관: `cluster` by entity
- 시계열 상관: `HAC` (Newey-West)
- 이중 클러스터: `multiway clustering`

---

### 2. 패널 데이터 분석

**방법론 결정 트리:**
```
패널 데이터
├── T > N → Fixed Effects (within estimator) 우선
├── N > T, 개체 이질성 의심 → Hausman test
│   ├── p < 0.05 → Fixed Effects (FE)
│   └── p ≥ 0.05 → Random Effects (RE) 또는 GLS
├── 처치 여부 있음 → Difference-in-Differences (DiD)
└── 다기간 처치 → Staggered DiD (Callaway-Sant'Anna / Sun-Abraham)
```

**핵심 구현:**
```python
# Python: linearmodels
from linearmodels.panel import PanelOLS, RandomEffects, BetweenOLS
from linearmodels.panel import compare

# FE 모델 (엔티티 + 시간 고정효과)
mod = PanelOLS(y, X, entity_effects=True, time_effects=True)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res.summary)

# Hausman test
fe = PanelOLS(y, X, entity_effects=True).fit()
re = RandomEffects(y, X).fit()
```

```r
# R: plm
library(plm)
pdata <- pdata.frame(df, index = c("entity", "time"))
fe <- plm(y ~ x1 + x2, data = pdata, model = "within", effect = "twoways")
re <- plm(y ~ x1 + x2, data = pdata, model = "random")
phtest(fe, re)  # Hausman test
```

**DiD 구현 (표준 2×2):**
```python
# Treated × Post 상호작용항
df['did'] = df['treated'] * df['post']
mod = PanelOLS.from_formula('y ~ did + EntityEffects + TimeEffects', df)
```

**Staggered DiD (다기간 처치):**
```r
# Callaway & Sant'Anna (2021)
library(did)
out <- att_gt(yname = "y", tname = "year", idname = "id",
              gname = "first_treat", data = df)
es <- aggte(out, type = "dynamic")
ggdid(es)
```

---

### 3. 시계열 분석

**분석 순서:**
1. 단위근 검정 (ADF, KPSS, PP)
2. 정상성 확보 (차분, 로그 변환)
3. 모형 식별 (ACF/PACF → ARIMA 오더 결정)
4. 추정 및 진단 (Ljung-Box, ARCH-LM)
5. 예측 및 신뢰구간

```python
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

# 단위근 검정
adf_result = adfuller(series, autolag='AIC')
kpss_result = kpss(series, regression='c')

# ARIMA
model = ARIMA(series, order=(p, d, q))
result = model.fit()

# GARCH (변동성 모델링)
garch = arch_model(returns, vol='Garch', p=1, q=1)
garch_res = garch.fit(disp='off')

# VAR (다변량 시계열)
from statsmodels.tsa.vector_ar.var_model import VAR
var_model = VAR(df[['y1', 'y2', 'y3']])
var_result = var_model.fit(maxlags=10, ic='aic')
irf = var_result.irf(10)  # Impulse Response Function
```

**공적분 분석:**
```python
from statsmodels.tsa.coint_tables import c_sja
from statsmodels.tsa.vector_ar.vecm import VECM, coint_johansen

# Johansen 공적분 검정
jres = coint_johansen(df, det_order=0, k_ar_diff=1)
# VECM
vecm = VECM(df, k_ar_diff=1, coint_rank=1)
vecm_res = vecm.fit()
```

---

### 4. 인과추론 (Causal Inference)

#### 4-1. 도구변수 (IV / 2SLS)

**유효 IV 조건:** (1) 관련성 — F-통계 > 10 (weak instrument 기준), (2) 배제 제약, (3) 단조성

```python
from linearmodels.iv import IV2SLS

# 2SLS
iv = IV2SLS.from_formula('y ~ 1 + x_exog + [x_endog ~ z_instrument]', df)
res = iv.fit(cov_type='robust')

# 약한 도구변수 검정
print(res.first_stage.diagnostics)  # F-stat, Cragg-Donald
# Anderson-Rubin 신뢰구간 (robust to weak IV)
```

#### 4-2. Regression Discontinuity Design (RDD)

**설계 원칙:** running variable 연속성, bandwidth 선택, 다항식 차수, placebo test

```r
library(rdrobust)
# 최적 bandwidth 자동 선택
rdd <- rdrobust(y = df$outcome, x = df$running_var, c = cutoff)
summary(rdd)
rdplot(y = df$outcome, x = df$running_var, c = cutoff)  # 시각화

# Manipulation test (density discontinuity)
library(rddensity)
rddensity(X = df$running_var, c = cutoff)
```

#### 4-3. Synthetic Control

```r
library(Synth)
dataprep.out <- dataprep(
  foo = df, predictors = c("gdp", "trade"),
  dependent = "outcome", unit.variable = "id",
  time.variable = "year", treatment.identifier = treated_id,
  controls.identifier = control_ids,
  time.predictors.prior = pre_period, time.optimize.ssr = pre_period,
  time.plot = all_period
)
synth.out <- synth(dataprep.out)
gaps.plot(synth.out, dataprep.out)
```

---

### 5. ML 기반 계량경제학

**변수 선택:**
```python
from sklearn.linear_model import LassoCV, ElasticNetCV
from sklearn.preprocessing import StandardScaler

# Double Selection (Belloni et al.)
# Step 1: Lasso y on X
# Step 2: Lasso d on X  
# Step 3: OLS y on d + selected controls

# High-dimensional IV (HDIV)
from econml.iv.dr import DRIV
```

**헤테로지니어스 처치 효과:**
```python
from econml.dml import CausalForestDML, LinearDML
from econml.cate_interpreter import SingleTreeCateInterpreter

# Double ML
dml = LinearDML(model_y=LassoCV(), model_t=LassoCV())
dml.fit(Y, T, X=X, W=W)
te = dml.effect(X_test)

# Causal Forest
cf = CausalForestDML()
cf.fit(Y, T, X=X, W=W)
```

---

### 6. 이벤트 스터디 (Event Study)

```python
import pandas as pd
import numpy as np
from scipy import stats

def event_study(returns_df, event_dates, estimation_window=(-250, -11), 
                event_window=(-10, 10)):
    """
    returns_df: columns=['date', 'security_return', 'market_return']
    event_dates: dict {security_id: event_date}
    """
    results = []
    for sec_id, event_date in event_dates.items():
        # 추정 기간 → 정상 수익률 모델 (시장모델)
        est = returns_df[(returns_df['date'] >= event_date + pd.DateOffset(days=estimation_window[0])) &
                         (returns_df['date'] <= event_date + pd.DateOffset(days=estimation_window[1]))]
        model = np.polyfit(est['market_return'], est[sec_id], 1)
        alpha, beta = model[1], model[0]
        
        # 이벤트 기간 → 초과 수익률 (AR)
        evt = returns_df[(returns_df['date'] >= event_date + pd.DateOffset(days=event_window[0])) &
                         (returns_df['date'] <= event_date + pd.DateOffset(days=event_window[1]))]
        evt['AR'] = evt[sec_id] - (alpha + beta * evt['market_return'])
        evt['CAR'] = evt['AR'].cumsum()
        results.append(evt)
    
    # 평균 누적 초과수익률 (CAAR) + t-검정
    aar = pd.concat(results).groupby('date')['AR'].mean()
    caar = aar.cumsum()
    t_stat = caar / (aar.std() / np.sqrt(len(event_dates)))
    return caar, t_stat
```

---

## 진단 테스트 체크리스트

| 검정 | 목적 | 기준 |
|------|------|------|
| VIF | 다중공선성 | VIF < 10 |
| Breusch-Pagan | 이분산성 | p > 0.05 이면 등분산 |
| Durbin-Watson | 자기상관 | DW ≈ 2 이상적 |
| Hausman | FE vs RE | p < 0.05 → FE 선택 |
| F-통계 (1단계) | 약한 IV | > 10 (Stock-Yogo) |
| Sargan/Hansen J | 과식별 제약 | p > 0.05 (도구변수 유효) |
| ARCH-LM | 변동성 군집 | p < 0.05 → GARCH 필요 |

---

## 데이터 수집 및 처리

### 주요 데이터 소스

| 데이터 | 소스 | 접근 방법 |
|--------|------|-----------|
| 한국 주가/재무 | FnGuide, KRX | 웹 스크래핑 또는 API |
| 미국 주가 | CRSP, Compustat | WRDS (대학 구독) |
| 무료 대안 | Yahoo Finance | `yfinance` 라이브러리 |
| 매크로 지표 | FRED (미연준) | `fredapi` 라이브러리 |
| 한국 거시 | ECOS (한국은행) | ECOS OpenAPI |
| 특허/뉴스 | KIPRIS, BigKinds | OpenAPI |

```python
import yfinance as yf
import pandas_datareader as pdr
from fredapi import Fred

# FRED (거시 데이터)
fred = Fred(api_key='YOUR_KEY')
gdp = fred.get_series('GDP')
vix = fred.get_series('VIXCLS')

# yfinance (주가)
ticker = yf.Ticker("005930.KS")  # 삼성전자
hist = ticker.history(period="5y")

# ECOS (한국은행)
import requests
url = f"https://ecos.bok.or.kr/api/StatisticSearch/{ECOS_KEY}/json/kr/1/100/101Y001/A/2010/2025"
data = requests.get(url).json()
```

---

## 산출물 저장 경로

모든 분석 산출물은 아래 **절대 경로**에 저장한다:

```
/Users/pc/Documents/sr_research_centre/workspace/research/YYYY-MM-DD_{paper-slug}/
├── paper/
│   ├── draft.md              ← 논문 초안
│   └── appendix.md           ← 부록 (추가 결과표, 로버스트니스 체크)
├── analysis/
│   ├── main_analysis.py      ← 주분석 코드
│   ├── robustness.py         ← 로버스트니스 체크
│   └── figures/              ← 차트/그림 (PNG/SVG)
└── data/
    ├── raw/                  ← 원본 데이터 (수정 금지)
    │   └── source_note.csv   ← 첫 3줄: # source, # url, # retrieved
    └── processed/            ← 가공 데이터
```

**raw CSV 출처 주석 (REQUIRED):**
```csv
# source: 기관명 (예: FRED, FnGuide, KRX)
# url: https://실제URL
# retrieved: YYYY-MM-DD
```

---

## 완료 후 리뷰 요청 (REQUIRED)

분석 완료 후 Statistical Reviewer에게 리뷰 서브이슈를 생성한다:

```bash
curl -s -X POST "$PAPERCLIP_API_URL/api/companies/$PAPERCLIP_COMPANY_ID/issues" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID" \
  -d "{
    \"title\": \"[리뷰] 계량분석 검증 — $(현재이슈제목)\",
    \"description\": \"계량경제학 분석 결과 검증 요청\\n\\n- 모델 가정 충족 여부\\n- 식별 전략 타당성\\n- 진단 테스트 결과\\n- 결과 해석 적절성\",
    \"status\": \"todo\",
    \"parentId\": \"$PAPERCLIP_TASK_ID\"
  }"
```
