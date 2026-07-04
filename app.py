import streamlit as st

st.title("AI Equity Research Copilot")

ticker = st.text_input("Enter Stock Ticker")

if st.button("Analyze"):
    st.write(f"Analyzing {ticker}...")