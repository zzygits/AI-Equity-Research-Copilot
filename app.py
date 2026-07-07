import plotly.graph_objects as go
import streamlit as st
from utils.finance import analyze_stock
from utils.ai import generate_ai_report

st.set_page_config(page_title="AI Equity Research Copilot", layout="wide")

st.title("📊 AI Equity Research Copilot")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT)")

if st.button("Analyze"):
    if ticker:

        with st.spinner("Analyzing..."):
            result = analyze_stock(ticker)
            price_history = result["price_history"]

        price_history["SMA20"] = (
            price_history["Close"]
            .rolling(20)
            .mean()
        )

        price_history["SMA50"] = (
            price_history["Close"]
            .rolling(50)
            .mean()
        )

        company = result["company"]
        score = result["investment_score"]
        fundamentals = result["fundamentals"]
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

        # -------------------------
        # Business Summary Section
        # -------------------------

        st.subheader("📝 Business Summary")
        st.write(company["description"])    

        st.divider()

        # -------------------------
        # News Section
        # -------------------------

        news = result["news"]

        st.subheader("📰 Latest News")

        if news:
            for article in news:
                st.markdown(f"**{article['title']}**")
                st.caption(article["published"])
                st.write(article["summary"])
                st.divider()
                
        else:
            st.info("No recent news found.")

        # -------------------------
        # Investment Score Section
        # -------------------------

        st.subheader("📝 Business Summary")
        st.write(company["description"])

        st.divider()

        st.subheader("⭐ Investment Score")

        col1, col2 = st.columns([1, 3])

        with col1:
            st.metric(
                "Overall",
                f"{score['overall']}/10"
            )

        with col2:
            st.write("### Breakdown")

            for category, value in score["breakdown"].items():
                st.progress(value / 10, text=f"{category}: {value}/10")

        # -------------------------
        # Chart Section
        # -------------------------
        
        st.subheader("📈 Stock Price Chart")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=price_history["Date"],
                y=price_history["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=price_history["Date"],
                y=price_history["SMA20"],
                mode="lines",
                name="20-Day SMA"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=price_history["Date"],
                y=price_history["SMA50"],
                mode="lines",
                name="50-Day SMA"
            )
        )

        fig.update_layout(
            title="1-Year Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=500,
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------
        # Fundamental Section
        # -------------------------

        st.subheader("📊 Fundamental Analysis")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "P/E",
            f"{fundamentals['trailing_pe']:.2f}"
            if fundamentals["trailing_pe"] is not None else "N/A"
        )

        col2.metric(
            "Forward P/E",
            f"{fundamentals['forward_pe']:.2f}"
            if fundamentals["forward_pe"] is not None else "N/A"
        )

        col3.metric(
            "PEG",
            f"{fundamentals['peg_ratio']:.2f}"
            if fundamentals["peg_ratio"] is not None else "N/A"
        )

        col4.metric(
            "Price / Book",
            f"{fundamentals['price_to_book']:.2f}"
            if fundamentals["price_to_book"] is not None else "N/A"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "ROE",
            f"{fundamentals['roe']:.2%}" if fundamentals["roe"] else "N/A"
        )

        col2.metric(
            "Profit Margin",
            f"{fundamentals['profit_margin']:.2%}" if fundamentals["profit_margin"] else "N/A"
        )

        col3.metric(
            "Revenue Growth",
            f"{fundamentals['revenue_growth']:.2%}" if fundamentals["revenue_growth"] else "N/A"
        )

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
        with st.container(border=True):
            st.markdown(generate_ai_report(result))

    else:
        st.warning("Please enter a ticker")

    st.write(result["news"])