import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from pipeline import add_features
from sqlalchemy import create_engine

# Load data
engine = create_engine("sqlite:///stonks.db")
df = pd.read_sql("SELECT * FROM prices WHERE Ticker='AAPL' ORDER BY Date", engine)
df_features = add_features(df)

# Features and target
X = df_features.drop(['Date', 'Ticker', 'Target'], axis=1)
y = df_features['Target']

# Dictionary to hold models
models = {
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
     "GradientBoosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=1000)
}

# Train models and print feature importances
for name, model in models.items():
    model.fit(X, y)
    print(f"\nFeature importances for {name}:")
    
    if name in ["XGBoost", "RandomForest", "GradientBoosting"]:
        importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        print(importances)
    elif name == "LogisticRegression":
        # Coefficients indicate importance for linear models
        importances = pd.Series(model.coef_[0], index=X.columns).sort_values(key=abs, ascending=False)
        print(importances)
