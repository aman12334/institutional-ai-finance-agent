import os
from agents.finance_agent_team import run_financial_intelligence
from core.analytics import fetch_history
from core.charts import (
    plot_price_with_ma,
    plot_volume,
    plot_rolling_volatility,
    plot_drawdown,
    plot_returns_distribution,
)
from core.reports import ReportBuilder


def generate_report(ticker: str, output_path: str):

    result = run_financial_intelligence(ticker)
    summary = result["analysis_summary"]
    narrative = result["agent_narrative"]
    reasoning_log = result["reasoning_log"]

    rb = ReportBuilder()
    rb.add_title(f"Financial Intelligence Report: {ticker}")

    rb.add_section("Executive Summary", narrative)

    if summary.get("data_available", False):

        hist = fetch_history(ticker)

        chart_functions = {
            "price_ma.png": plot_price_with_ma,
            "volume.png": plot_volume,
            "volatility.png": plot_rolling_volatility,
            "drawdown.png": plot_drawdown,
            "returns_dist.png": plot_returns_distribution,
        }

        for filename, func in chart_functions.items():
            func(hist, filename)
            rb.add_image(filename)
            os.remove(filename)

    else:
        rb.add_section("Data Availability", summary.get("message"))

    rb.add_reasoning_log(reasoning_log)

    rb.save(output_path)
