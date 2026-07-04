import streamlit as st
from utils.finance import analyze_stock
from utils.finance import generate_ai_report


st.set_page_config(page_title="AI Equity Research Copilot", layout="wide")

st.title("📊 AI Equity Research Copilot")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT)")

if st.button("Analyze"):
    if ticker:

        with st.spinner("Analyzing..."):
            result = analyze_stock(ticker)

        company = result["company"]
        tech = result["technical"]
        risk = result["risk"]

        # -------------------------
        # Company Section
        # -------------------------
        st.subheader("🏢 Company Overview")

        st.write("Name:", company["name"])
        st.write("Sector:", company["sector"])
        st.write("Industry:", company["industry"])
        st.write("Market Cap:", company["market_cap"])
        st.subheader("📝 Business Summary")
        st.write(company["description"])    

        st.divider()

        # -------------------------
        # Technical Section
        # -------------------------
        st.subheader("📈 Technical Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Price",
            f"${tech['latest_price']:.2f}"
        )

        col2.metric(
            "1Y Return",
            f"{tech['total_return_1y']:.2%}"
        )

        col3.metric(
            "Volatility",
            f"{tech['volatility']:.2%}"
        )

        st.divider()

        # -------------------------
        # Risk Section
        # -------------------------
        st.subheader("⚠️ Risk Metrics")

        st.write(f"Max Drawdown: {risk['max_drawdown']:.2%}")
        st.write(f"Best Day: {risk['best_day']:.2%}")
        st.write(f"Worst Day: {risk['worst_day']:.2%}")

        # -------------------------
        # AI Analyst Report Section
        # -------------------------
        st.subheader("🧠 AI Analyst Report")
        st.write(generate_ai_report(result))

    else:
        st.warning("Please enter a ticker")