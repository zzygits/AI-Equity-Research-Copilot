# =========================================================
# INVESTMENT SCORING ENGINE
# =========================================================

def compute_investment_score(result: dict) -> dict:

    tech = result["technical"]
    risk = result["risk"]
    fundamentals = result["fundamentals"]

    scores = {}

    growth = fundamentals["revenue_growth"]

    if growth is None:
        growth_score = 5

    elif growth >= 0.30:
        growth_score = 10

    elif growth >= 0.20:
        growth_score = 9

    elif growth >= 0.10:
        growth_score = 8

    elif growth >= 0:
        growth_score = 7

    else:
        growth_score = 4

    scores["Growth"] = growth_score

    margin = fundamentals["profit_margin"]

    if margin is None:
        profit_score = 5

    elif margin >= 0.30:
        profit_score = 10

    elif margin >= 0.20:
        profit_score = 9

    elif margin >= 0.10:
        profit_score = 8

    else:
        profit_score = 6

    scores["Profitability"] = profit_score

    ret = tech["total_return_1y"]

    if ret >= 0.40:
        momentum = 10

    elif ret >= 0.20:
        momentum = 9

    elif ret >= 0:
        momentum = 7

    elif ret >= -0.20:
        momentum = 5

    else:
        momentum = 3

    scores["Momentum"] = momentum

    dd = abs(risk["max_drawdown"])

    if dd <= 0.10:
        risk_score = 10

    elif dd <= 0.20:
        risk_score = 9

    elif dd <= 0.35:
        risk_score = 8

    elif dd <= 0.50:
        risk_score = 6

    else:
        risk_score = 4

    scores["Risk"] = risk_score

    pe = fundamentals["trailing_pe"]

    if pe is None:
        valuation = 5

    elif pe <= 15:
        valuation = 10

    elif pe <= 25:
        valuation = 9

    elif pe <= 35:
        valuation = 8

    elif pe <= 50:
        valuation = 6

    else:
        valuation = 4

    scores["Valuation"] = valuation

    overall = round(sum(scores.values()) / len(scores), 1)

    return {
        "overall": overall,
        "breakdown": scores
    }
