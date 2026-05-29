# 기업 분석 산출물 구조 예시

`/company_analysis <회사명>` 커맨드 실행 시 생성되는 디렉토리 구조입니다.
실제 산출물은 `workspace/companies/YYYY-MM-DD_{티커}_{종목명}/`에 저장됩니다.

## 디렉토리 구조

```
workspace/companies/2026-04-10_005930_삼성전자/
├── report.md               ← 메인 기업 리포트 (투자의견 + 목표주가)
├── appendix.md             ← 재무 부록 (3개년 실적 + 2개년 전망)
├── valuation.md            ← 밸류에이션 상세 (SOTP 또는 Target Multiple)
├── business/
│   ├── business-analysis.md  ← 사업부 분석, 경쟁 포지셔닝
│   └── charts/specs/
├── finance/
│   ├── finance-analysis.md   ← 재무 모델, 분기 전망표
│   ├── financial-model.csv   ← 수치 원본
│   └── charts/specs/
└── tech/
    ├── tech-analysis.md      ← 기술 로드맵, 특허
    └── charts/specs/
```

## 리포트 구성 예시

기업 리포트 (`report.md`) 주요 섹션:
1. **투자의견 요약** — Buy/Hold/Sell, 목표주가, 업사이드/다운사이드
2. **사업 분석** — 핵심 사업부 포지셔닝, Value chain, 경영진 전략
3. **재무 분석** — P&L/B/S/CF 추이, ROE vs Peer, ROIC vs WACC
4. **기술 경쟁력** — 기술 로드맵, R&D 성과, 특허 포지션
5. **시장 환경** — 산업 구조, 수급, 글로벌 가격 트렌드
6. **밸류에이션** — SOTP 또는 Target Multiple, 목표주가 산출 근거
7. **리스크 요인** — 다운사이드 시나리오
