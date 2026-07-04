import streamlit as st
from utils.finance import analyze_stock

st.set_page_config(page_title="AI Equity Research Copilot", layout="wide")

st.title("📊 AI Equity Research Copilot")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT)")

if st.button("Analyze"):
    if ticker:

        with st.spinner("Analyzing..."):
            result = analyze_stock(ticker)

        # -------------------------
        # Company Section
        # -------------------------
        st.subheader("🏢 Company Overview")

        st.write("Name:", result["company"]["name"])
        st.write("Sector:", result["company"]["sector"])
        st.write("Industry:", result["company"]["industry"])
        st.write("Market Cap:", result["company"]["market_cap"])

        st.divider()

        # -------------------------
        # Technical Section
        # -------------------------
        st.subheader("📈 Technical Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Price", result["technical"]["latest_price"])
        col2.metric("1Y Return", f"{round(result['technical']['total_return_1y']*100, 2)}%")
        col3.metric("Volatility", f"{round(result['technical']['volatility']*100, 2)}%")

        st.divider()

        # -------------------------
        # Risk Section
        # -------------------------
        st.subheader("⚠️ Risk Metrics")

        st.write("Max Drawdown:", result["risk"]["max_drawdown"])
        st.write("Best Day:", result["risk"]["best_day"])
        st.write("Worst Day:", result["risk"]["worst_day"])

    else:
        st.warning("Please enter a ticker")