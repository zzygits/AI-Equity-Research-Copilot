import pandas as pd

from utils.finance import analyze_stock

def compare_stocks(tickers: list[str]) -> pd.DataFrame:

    comparison = []

    for ticker in tickers:

        try:

            result = analyze_stock(ticker)
            print(result.keys())

            company = result["company"]
            fundamentals = result["fundamentals"]
            tech = result["technical"]
            score = result["investment_score"]

            comparison.append({

                "Ticker": ticker,

                "Company": company["name"],

                "Current Price": f"${tech['latest_price']:.2f}",

                "Market Cap": company["market_cap"],

                "Revenue Growth": (
                    f"{fundamentals['revenue_growth']:.2%}"
                    if fundamentals["revenue_growth"] is not None
                    else "N/A"
                ),

                "Profit Margin": (
                    f"{fundamentals['profit_margin']:.2%}"
                    if fundamentals["profit_margin"] is not None
                    else "N/A"
                ),

                "P/E": (
                    round(fundamentals["trailing_pe"], 2)
                    if fundamentals["trailing_pe"] is not None
                    else "N/A"
                ),

                "Investment Score": score["overall"]

            })

        except Exception as e:
            print(f"Error analysing {ticker}: {e}")

    df = pd.DataFrame(comparison)

    df = df.sort_values(
        "Investment Score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(
        0,
        "Rank",
        range(1, len(df)+1)
    )   

    return df

    