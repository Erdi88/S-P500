import yfinance as yf
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

def load_price_data(ticker: str):# -> pd.DataFrame:
    data = yf.Ticker(ticker).history(period="50y", auto_adjust=False)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]#.to_string()
    data['Ticker'] = ticker
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'], utc=True).dt.tz_convert(None)
    return data
# print(load_price_data("AAPL").head())