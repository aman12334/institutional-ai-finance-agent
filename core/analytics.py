import yfinance as yf
import pandas as pd
import numpy as np


def fetch_history(ticker: str, period="5y") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        return pd.DataFrame()

    hist = hist.reset_index()
    hist.rename(columns=str.lower, inplace=True)
    return hist


def calculate_volatility_percentile(returns: pd.Series) -> float:
    rolling_vol = returns.rolling(60).std() * np.sqrt(252)
    current_vol = rolling_vol.iloc[-1]
    percentile = (rolling_vol.rank(pct=True).iloc[-1]) * 100
    return round(float(percentile), 2)


def calculate_downtrend_duration(hist: pd.DataFrame) -> int:
    ma200 = hist["close"].rolling(200).mean()
    below_ma = hist["close"] < ma200

    duration = 0
    for val in reversed(below_ma.tolist()):
        if val:
            duration += 1
        else:
            break
    return duration


def estimate_recovery_probability(trend: str, drawdown: float, vol_percentile: float) -> float:
    score = 0

    if trend == "upward":
        score += 2
    if drawdown > -30:
        score += 1
    if vol_percentile < 50:
        score += 1

    probability = max(min((score / 4) * 100, 100), 5)
    return round(probability, 1)


def suggest_position_size(regime: str) -> str:
    if regime == "DEFENSIVE":
        return "0% – Avoid or hedge exposure"
    elif regime == "CAUTION":
        return "1%–3% tactical allocation with strict stop-loss"
    else:
        return "3%–5% core allocation within diversified portfolio"


def classify_risk_regime(summary: dict) -> dict:

    if not summary.get("data_available", False):
        return {"regime": "NO_DATA", "risk_score": None}

    trend = summary["trend"]
    volatility = summary["annualized_volatility"]
    drawdown = summary["max_drawdown_pct"]

    risk_score = 0

    if trend == "downward":
        risk_score += 2

    if volatility >= 0.40:
        risk_score += 2
    elif volatility >= 0.30:
        risk_score += 1

    if drawdown <= -60:
        risk_score += 3
    elif drawdown <= -40:
        risk_score += 2
    elif drawdown <= -25:
        risk_score += 1

    if risk_score >= 5:
        regime = "DEFENSIVE"
    elif risk_score >= 3:
        regime = "CAUTION"
    else:
        regime = "CONSTRUCTIVE"

    return {
        "regime": regime,
        "risk_score": risk_score,
    }


def build_analysis_summary(ticker: str) -> dict:

    hist = fetch_history(ticker)

    if hist.empty:
        return {
            "ticker": ticker,
            "data_available": False,
            "message": "No historical market data available for this ticker.",
        }

    returns = hist["close"].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252)
    trend = "upward" if hist["close"].iloc[-1] > hist["close"].iloc[0] else "downward"
    drawdown = (hist["close"] / hist["close"].cummax() - 1).min()

    vol_percentile = calculate_volatility_percentile(returns)
    downtrend_days = calculate_downtrend_duration(hist)
    recovery_prob = estimate_recovery_probability(trend, drawdown * 100, vol_percentile)

    summary = {
        "ticker": ticker,
        "data_available": True,
        "time_period": f"{hist['date'].min().date()} to {hist['date'].max().date()}",
        "trend": trend,
        "annualized_volatility": round(float(volatility), 3),
        "volatility_percentile": vol_percentile,
        "max_drawdown_pct": round(float(drawdown * 100), 2),
        "downtrend_days": downtrend_days,
        "recovery_probability_pct": recovery_prob,
        "observations": len(hist),
    }

    regime_data = classify_risk_regime(summary)
    summary.update(regime_data)
    summary["position_size_suggestion"] = suggest_position_size(regime_data["regime"])

    return summary
