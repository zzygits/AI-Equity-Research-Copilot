# =========================================================
# 8. AI ANALYST REPORT
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