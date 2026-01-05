from features import (
    add_returns,
    add_moving_averages,
    add_momentum,
    add_volatility,
    add_trend_ratios,
    add_drawdown,
    add_volume_features
)

def add_features(df):
    df = df.copy()
    df = df.sort_values("Date").drop_duplicates(subset=["Date"], keep="last")
    # Call feature functions
    df = add_returns(df)
    df = add_moving_averages(df)
    df = add_momentum(df)
    df = add_volatility(df)
    df = add_trend_ratios(df)
    df = add_drawdown(df)
    df = add_volume_features(df)
    
    # Example: medium-term target (e.g., 20 trading days)
    # df['Medium_Target'] = (df['Close'].shift(-20) > df['Close']).astype(int)
    
    # Drop rows with NaNs from rolling computations
    df = df.dropna()
    
    return df
