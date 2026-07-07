import yfinance as yf
import pandas as pd


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
# 3. TECHNICAL ANALYSIS
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
# 4. RISK ANALYSIS
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
# 5. MASTER ANALYSIS ENGINE
# =========================================================

def analyze_stock(ticker: str) -> dict:
    """
    Main entry point for AI Equity Research Copilot.
    """

    price_history = get_price_history(ticker)

    company = get_company_info(ticker)

    technical = compute_technical_metrics(price_history)

    risk = compute_risk_features(price_history)

    return {
        "company": company,
        "technical": technical,
        "risk": risk,
        "price_history": price_history,
    }


# =========================================================
# 6. AI ANALYST REPORT
# =========================================================

def generate_ai_report(result: dict) -> str:

    company = result["company"]
    tech = result["technical"]
    risk = result["risk"]

    # Momentum assessment
    if tech["total_return_1y"] > 0.20:
        momentum = "strong"
    elif tech["total_return_1y"] > 0:
        momentum = "positive"
    elif tech["total_return_1y"] > -0.20:
        momentum = "weak"
    else:
        momentum = "negative"

    # Volatility assessment
    if tech["volatility"] < 0.20:
        volatility = "low"
    elif tech["volatility"] < 0.35:
        volatility = "moderate"
    elif tech["volatility"] < 0.50:
        volatility = "high"
    else:
        volatility = "very high"

    report = f"""
# STOCK ANALYSIS REPORT

## Company

**{company['name']} ({company['ticker']})**

Sector: {company['sector']}

Industry: {company['industry']}

---

## Performance

- Current Price: ${tech['latest_price']:.2f}
- 1-Year Return: {tech['total_return_1y']:.2%}
- Annualized Volatility: {tech['volatility']:.2%}

---

## Risk Profile

- Maximum Drawdown: {risk['max_drawdown']:.2%}
- Best Trading Day: {risk['best_day']:.2%}
- Worst Trading Day: {risk['worst_day']:.2%}

---

## Interpretation

{company['name']} has demonstrated **{momentum} momentum** over the past year while exhibiting **{volatility} volatility**.

This report is based on historical market data and should be complemented with fundamental analysis, valuation metrics, earnings trends, and macroeconomic considerations before making an investment decision.
"""

    return report