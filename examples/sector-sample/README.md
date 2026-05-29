# 섹터 분석 산출물 구조 예시

`/sector_analysis <섹터명>` 커맨드 실행 시 생성되는 디렉토리 구조입니다.
실제 산출물은 `workspace/sectors/YYYY-MM-DD_{슬러그}/`에 저장됩니다.

## 디렉토리 구조

```
workspace/sectors/2026-04-05_financials/
├── report.md               ← 메인 섹터 리포트 (Overweight/Neutral/Underweight 포함)
├── appendix.md             ← 데이터 부록
├── market/
│   ├── market-analysis.md  ← 시장 구조, 수급, 글로벌 트레이드
│   └── charts/specs/       ← 차트 JSON 스펙
├── tech/
│   ├── tech-analysis.md    ← 기술 트렌드, 제품 사이클
│   └── charts/specs/
├── policy/
│   ├── policy-analysis.md  ← 규제·정책, ESG
│   └── charts/specs/
└── data/
    ├── raw/                ← 원본 데이터 (출처 주석 필수)
    └── processed/          ← 가공 데이터
```

## 리포트 구성 예시

섹터 리포트 (`report.md`) 주요 섹션:
1. **섹터 스탠스** — Overweight/Neutral/Underweight + 탑픽
2. **산업 구조** — 공급망, 수급, 주요 플레이어 맵
3. **기술 트렌드** — 제품 사이클, 신기술 도입 타임라인
4. **정책·규제** — 관련 규제, 보조금, ESG 리스크
5. **매크로 환경** — 금리·환율 민감도, 경기 사이클 포지션
6. **밸류에이션** — 섹터 PER/PBR 밴드, 히스토리컬 비교
