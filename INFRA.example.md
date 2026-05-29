# SR Research Centre — 인프라 설정 (템플릿)

> 이 파일을 `INFRA.md`로 복사한 후 아래 API 키들을 실제 값으로 채우세요.
> `INFRA.md`는 `.gitignore`에 포함되어 있어 커밋되지 않습니다.

## API 키

| 키 이름 | 값 | 용도 |
|---------|-----|------|
| `DART_API_KEY` | `YOUR_DART_API_KEY` | 금융감독원 전자공시(OpenDART) — 재무제표, 공시 수집 |
| `ECOS_API_KEY` | `YOUR_ECOS_API_KEY` | 한국은행 경제통계시스템 — 금리, GDP, CPI 등 거시지표 |
| `FRED_API_KEY` | `YOUR_FRED_API_KEY` | FRED (Federal Reserve Economic Data) — 미국 금리·GDP·CPI 등 거시지표 |

### API 키 발급 방법
- **DART**: [OpenDART](https://opendart.fss.or.kr/) 회원가입 → API 신청 → 즉시 발급
- **ECOS**: [한국은행 ECOS](https://ecos.bok.or.kr/) → 이용신청 → API KEY 발급
- **FRED**: [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html) → 계정 생성 → API Key 발급 (무료)

### 사용 방법

환경변수로 주입되어 있으므로 코드에서 바로 사용 가능:

```python
import os
dart_key = os.environ.get("DART_API_KEY")
ecos_key = os.environ.get("ECOS_API_KEY")
fred_key = os.environ.get("FRED_API_KEY")
```

dart-fss 예시:
```python
import dart_fss
dart_fss.set_api_key(os.environ["DART_API_KEY"])
```

## 데이터 수집 스니펫

### pykrx 주가 수집
`KRX 로그인 실패` 경고가 뜨더라도 **정상 작동**함. 경고 무시하고 계속 진행할 것.

```python
import warnings; warnings.filterwarnings("ignore")
from pykrx import stock

df = stock.get_market_ohlcv("20260101", "20260430", "005930")
print(df)
```

### dart-fss 재무제표 수집
```python
import dart_fss
dart_fss.set_api_key(os.environ["DART_API_KEY"])
corps = dart_fss.get_corp_list()
samsung = corps.find_by_stock_code("005930")
```

### yfinance 폴백 (pykrx 실패 시 대체)
```python
import yfinance as yf
# 한국 종목 = 티커 + ".KS" (KOSPI) 또는 ".KQ" (KOSDAQ)
df = yf.download("005930.KS", start="2019-01-01", end="2024-12-31", interval="1mo")
```

## 내부 서버

| 서비스 | 주소 |
|--------|------|
| SR Research Centre API | `http://127.0.0.1:3100` |
| Company ID | `YOUR_COMPANY_ID` (플랫폼 생성 후 발급) |
