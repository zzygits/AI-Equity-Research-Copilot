import yfinance as yf
import pandas as pd
from utils.scoring import compute_investment_score
from utils.news import get_company_news

# =========================================================
# 1. HELPER FUNCTIONS
# =========================================================

def format_market_cap(value):
    """Convert market cap into human-readable format."""

    if value is None:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    return f"${value:,.0f}"


# =========================================================
# 2. DATA RETRIEVAL
# =========================================================

def get_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Download historical stock prices."""

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError(f"No price data found for {ticker}")

    hist = hist.reset_index()

    return hist


def get_company_info(ticker: str) -> dict:
    """Retrieve company information."""

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": format_market_cap(info.get("marketCap")),
        "description": info.get("longBusinessSummary"),
    }

# =========================================================
# 3. FUNDAMENTAL ANALYSIS
# =========================================================

def get_fundamental_metrics(ticker: str) -> dict:

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "peg_ratio": info.get("pegRatio"),
        "price_to_book": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "profit_margin": info.get("profitMargins"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": info.get("currentRatio"),
    }

# =========================================================
# 4. TECHNICAL ANALYSIS
# =========================================================

def compute_technical_metrics(price_df: pd.DataFrame) -> dict:

    returns = price_df["Close"].pct_change().dropna()

    latest_price = price_df["Close"].iloc[-1]

    total_return = (
        price_df["Close"].iloc[-1]
        / price_df["Close"].iloc[0]
        - 1
    )

    volatility = returns.std() * (252 ** 0.5)

    return {
        "latest_price": latest_price,
        "total_return_1y": total_return,
        "volatility": volatility,
    }


# =========================================================
# 5. RISK ANALYSIS
# =========================================================

def compute_risk_features(price_df: pd.DataFrame) -> dict:

    returns = price_df["Close"].pct_change().dropna()

    cumulative = (1 + returns).cumprod()

    rolling_max = cumulative.cummax()

    drawdown = cumulative / rolling_max - 1

    return {
        "max_drawdown": drawdown.min(),
        "best_day": returns.max(),
        "worst_day": returns.min(),
    }


# =========================================================
# 7. MASTER ANALYSIS ENGINE
# =========================================================

def analyze_stock(ticker: str) -> dict:
    """
    Main entry point for AI Equity Research Copilot.
    """

    price_history = get_price_history(ticker)
    company = get_company_info(ticker)
    fundamentals = get_fundamental_metrics(ticker)
    technical = compute_technical_metrics(price_history)
    risk = compute_risk_features(price_history)
    news = get_company_news(ticker)
    investment_score = compute_investment_score({
    "technical": technical,
    "risk": risk,
    "fundamentals": fundamentals
    })  

    return {
        "company": company,
        "fundamentals": fundamentals,
        "technical": technical,
        "risk": risk,
        "news": news,
        "price_history": price_history,
        "investment_score": investment_score,
    }
