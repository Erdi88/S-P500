import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from pipeline import add_features
from sklearn.metrics import accuracy_score, precision_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# IMPORTANT FEATURE SETS EXTRACTED FROM PRIOR ANALYSIS
important_features = {
    "XGBoost": [
        'SMA_100', 'Volume', 'High', 'SMA_200', 'Low', 
        'Drawdown', 'SMA100_SMA200_Ratio', 'SMA_50', 'Volatility_120'
    ],
    "RandomForest": [
        'Volume_Change_60', 'Volume_Change_20', 'Volume', 
        'Momentum_60', 'Momentum_20', 'Volatility_60', 'Momentum_120'
    ],
    "GradientBoosting": [
        'Volume_Change_60', 'Volatility_60', 'Volume', 
        'Momentum_60', 'Volatility_20', 'Momentum_120'
    ],
    "LogisticRegression": [
        'Volume_MA_60', 'Volume_MA_20', 'Volume', 'High', 'Close'
    ]
}

# BASE MODELS
models = {
    "XGBoost": XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='logloss',
        random_state=42
    ),

    "RandomForest": RandomForestClassifier(
        n_estimators=500,
        max_features='sqrt',
        min_samples_split=5,
        min_samples_leaf=2,
        bootstrap=True,
        random_state=42
    ),

    "GradientBoosting": GradientBoostingClassifier(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        random_state=42
    ),

    "LogisticRegression": Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(
            max_iter=3000,
            solver='lbfgs'
        ))
    ])
}


def prepare_data(df):
    """
    Preprocess dataframe from SQL, add features & return X,y.
    df must contain Close/Volume/High/Low/Date etc BEFORE calling this.
    """

    df = add_features(df)

    X_full = df.drop(['Date', 'Ticker', 'Target'], axis=1)
    y = df['Target']
    return X_full, y



def evaluate_models_precision(X, y, test_size):
    """
    Train models on all data except last N days,
    then evaluate using precision_score on final N days.
    """

    # Time-series split
    X_train, X_test = X[:-test_size], X[-test_size:]
    y_train, y_test = y[:-test_size], y[-test_size:]

    print(f"\nTraining on {len(X_train)} samples, testing on last {test_size} days...")

    trained_models = {}
    results = {}

    for name, model in models.items():
        X_train_sel = X_train[important_features[name]]
        X_test_sel = X_test[important_features[name]]

        model.fit(X_train_sel, y_train)
        trained_models[name] = model

        preds = model.predict(X_test_sel)

        precision = precision_score(y_test, preds, pos_label=1, zero_division=0)
        results[name] = precision

        print(f"{name:<18} Precision: {precision:.4f}")

    return trained_models, results


