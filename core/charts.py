import matplotlib.pyplot as plt
import numpy as np


def plot_price_with_ma(hist, output_path):
    hist = hist.copy()
    hist["ma_50"] = hist["close"].rolling(50).mean()
    hist["ma_200"] = hist["close"].rolling(200).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(hist["date"], hist["close"], label="Close")
    plt.plot(hist["date"], hist["ma_50"], label="MA 50")
    plt.plot(hist["date"], hist["ma_200"], label="MA 200")

    plt.title("Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_volume(hist, output_path):
    plt.figure(figsize=(10, 4))
    plt.bar(hist["date"], hist["volume"])
    plt.title("Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_rolling_volatility(hist, output_path):
    hist = hist.copy()
    returns = hist["close"].pct_change()
    rolling_vol = returns.rolling(30).std() * np.sqrt(252)

    plt.figure(figsize=(10, 4))
    plt.plot(hist["date"], rolling_vol)
    plt.title("30-Day Rolling Annualized Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_drawdown(hist, output_path):
    hist = hist.copy()
    cumulative_max = hist["close"].cummax()
    drawdown = hist["close"] / cumulative_max - 1

    plt.figure(figsize=(10, 4))
    plt.plot(hist["date"], drawdown)
    plt.title("Drawdown Curve")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_returns_distribution(hist, output_path):
    returns = hist["close"].pct_change().dropna()

    plt.figure(figsize=(8, 4))
    plt.hist(returns, bins=50)
    plt.title("Daily Returns Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
