import pandas as pd
import numpy as np

# ---------------- Price returns ----------------
def add_returns(df):
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    df['LogReturn'] = np.log(df['Close'] / df['Close'].shift(1))
    return df

# ---------------- Moving averages ----------------
def add_moving_averages(df, windows=(5, 10, 50, 100, 200, 500)):
    df = df.copy()
    for w in windows:
        df[f'SMA_{w}'] = df['Close'].rolling(w).mean()
    return df

# ---------------- Momentum ----------------
def add_momentum(df, windows=(20, 60, 120)):
    df = df.copy()
    for w in windows:
        df[f'Momentum_{w}'] = df['Close'] / df['Close'].shift(w) - 1
    return df

# ---------------- Volatility ----------------
def add_volatility(df, windows=(20, 60, 120)):
    df = df.copy()
    for w in windows:
        df[f'Volatility_{w}'] = df['Close'].pct_change().rolling(w).std()
    return df

# ---------------- Trend ratios ----------------
def add_trend_ratios(df):
    df = df.copy()
    if 'SMA_50' in df.columns and 'SMA_200' in df.columns:
        df['SMA50_SMA200_Ratio'] = df['SMA_50'] / df['SMA_200']
    if 'SMA_100' in df.columns and 'SMA_200' in df.columns:
        df['SMA100_SMA200_Ratio'] = df['SMA_100'] / df['SMA_200']
    return df

# ---------------- Drawdown ----------------
def add_drawdown(df, window=252):  # ~1 trading year
    df = df.copy()
    rolling_max = df['Close'].rolling(window, min_periods=1).max()
    df['Drawdown'] = df['Close'] / rolling_max - 1
    return df

# ---------------- Volume features ----------------
def add_volume_features(df, windows=(20, 60)):
    df = df.copy()
    for w in windows:
        df[f'Volume_MA_{w}'] = df['Volume'].rolling(w).mean()
        df[f'Volume_Change_{w}'] = df['Volume'].pct_change(w)
    return df
