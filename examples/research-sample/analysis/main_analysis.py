"""
예시 분석 코드 — 재무지표 기반 알파 팩터 검증
실제 분석에서는 이 구조로 코드를 작성합니다.
"""

import os
import pandas as pd
import numpy as np

# API 키는 환경변수에서 로드 (절대 하드코딩 금지)
DART_KEY = os.environ["DART_API_KEY"]
ECOS_KEY = os.environ["ECOS_API_KEY"]

DATA_DIR = "data/processed"
RESULTS_DIR = "results"


def compute_f_score(df: pd.DataFrame) -> pd.Series:
    """Piotroski F-Score (0–9) 계산."""
    score = pd.Series(0, index=df.index)

    # 수익성 (4점)
    score += (df["roa"] > 0).astype(int)
    score += (df["operating_cf"] > 0).astype(int)
    score += (df["roa"] > df["roa"].shift(1)).astype(int)
    score += (df["accrual"] < 0).astype(int)  # CF > 순이익

    # 레버리지·유동성 (3점)
    score += (df["long_term_debt_ratio"] < df["long_term_debt_ratio"].shift(1)).astype(int)
    score += (df["current_ratio"] > df["current_ratio"].shift(1)).astype(int)
    score += (df["shares_issued"] == 0).astype(int)

    # 운영 효율 (2점)
    score += (df["gross_margin"] > df["gross_margin"].shift(1)).astype(int)
    score += (df["asset_turnover"] > df["asset_turnover"].shift(1)).astype(int)

    return score


def build_portfolios(df: pd.DataFrame) -> dict:
    """F-Score 기준 High/Low 포트폴리오 구성."""
    return {
        "high": df[df["f_score"] >= 7],
        "low": df[df["f_score"] <= 2],
    }


def compute_portfolio_returns(portfolios: dict, prices: pd.DataFrame) -> pd.DataFrame:
    """포트폴리오 월별 수익률 계산 (동일가중)."""
    results = {}
    for name, portfolio in portfolios.items():
        tickers = portfolio["stock_code"].tolist()
        rets = prices[tickers].pct_change().mean(axis=1)
        results[name] = rets
    return pd.DataFrame(results)


if __name__ == "__main__":
    # 실제 실행 시 데이터 로드 후 분석
    print("예시 코드입니다. 실제 데이터를 연결하세요.")
    print(f"DART API Key 설정됨: {'Yes' if DART_KEY else 'No'}")
