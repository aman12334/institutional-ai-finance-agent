import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from run_report import generate_report
from agents.finance_agent_team import run_financial_intelligence
from core.analytics import build_analysis_summary

st.set_page_config(layout="wide")
st.title("AI Institutional Financial Intelligence")

ticker = st.text_input("Enter stock ticker")

if st.button("Analyze"):

    if not ticker:
        st.warning("Please enter a ticker.")
    else:

        summary = build_analysis_summary(ticker)

        if not summary.get("data_available", False):
            st.error(summary.get("message"))
        else:

            regime = summary["regime"]

            # -------------------------
            # REGIME BANNER
            # -------------------------
            if regime == "DEFENSIVE":
                st.markdown("<h2 style='color:red;'>🔴 DEFENSIVE REGIME</h2>", unsafe_allow_html=True)
            elif regime == "CAUTION":
                st.markdown("<h2 style='color:orange;'>🟡 CAUTION REGIME</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color:green;'>🟢 CONSTRUCTIVE REGIME</h2>", unsafe_allow_html=True)

            # -------------------------
            # METRICS DASHBOARD
            # -------------------------
            col1, col2, col3 = st.columns(3)

            col1.metric("Trend", summary["trend"])
            col2.metric("Volatility", summary["annualized_volatility"])
            col3.metric("Drawdown (%)", summary["max_drawdown_pct"])

            col4, col5, col6 = st.columns(3)

            col4.metric("Volatility Percentile", f"{summary['volatility_percentile']}%")
            col5.metric("Downtrend Days", summary["downtrend_days"])
            col6.metric("Recovery Probability", f"{summary['recovery_probability_pct']}%")

            st.write("### Position Sizing Suggestion")
            st.write(summary["position_size_suggestion"])

            # -------------------------
            # RUN MULTI-AGENT ANALYSIS
            # -------------------------
            st.write("---")
            st.write("## Institutional Investment Committee Analysis")

            result = run_financial_intelligence(ticker)

            # Render the memo
            st.markdown(result["agent_narrative"])

            # -------------------------
            # DOWNLOAD PDF
            # -------------------------
            output_file = f"{ticker}_institutional_report.pdf"
            generate_report(ticker, output_file)

            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Full Research Packet",
                    data=f,
                    file_name=output_file,
                    mime="application/pdf",
                )
