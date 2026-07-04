# finance.py

import yfinance as yf
import pandas as pd
import numpy as np


# =========================================================
# 1. DATA FETCH LAYER
# =========================================================

def get_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError(f"No price data found for {ticker}")

    return hist


# =========================================================
# 2. COMPANY INFO LAYER
# =========================================================

def get_company_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "market_cap": info.get("marketCap"),
        "currency": info.get("currency"),
        "website": info.get("website"),
        "description": info.get("longBusinessSummary")
    }


# =========================================================
# 3. TECHNICAL ANALYSIS LAYER
# =========================================================

def compute_technical_metrics(df: pd.DataFrame) -> dict:
    df = df.copy()

    df["returns"] = df["Close"].pct_change()

    total_return = (df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1
    volatility = df["returns"].std() * np.sqrt(252)

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    max_drawdown = (df["Close"] / df["Close"].cummax() - 1).min()

    return {
        "latest_price": float(df["Close"].iloc[-1]),
        "total_return_1y": float(total_return),
        "volatility": float(volatility),
        "sma20": float(df["SMA20"].iloc[-1]),
        "sma50": float(df["SMA50"].iloc[-1]),
        "max_drawdown": float(max_drawdown)
    }


# =========================================================
# 4. RISK FEATURES (simple but powerful later for AI layer)
# =========================================================

def compute_risk_features(df: pd.DataFrame) -> dict:
    returns = df["Close"].pct_change().dropna()

    return {
        "daily_volatility": float(returns.std()),
        "positive_days_ratio": float((returns > 0).mean()),
        "worst_day": float(returns.min()),
        "best_day": float(returns.max()),
        "max_drawdown": float((df["Close"] / df["Close"].cummax() - 1).min())
    }


# =========================================================
# 5. MASTER ANALYSIS ENGINE (THIS IS WHAT APP.PY CALLS)
# =========================================================

def analyze_stock(ticker: str) -> dict:
    """
    Main entry point for AI Equity Research Copilot
    """

    price_df = get_price_history(ticker)
    company = get_company_info(ticker)

    tech = compute_technical_metrics(price_df)
    risk = compute_risk_features(price_df)

    return {
        "company": company,
        "technical": tech,
        "risk": risk
    }
