import pandas as pd
import yfinance as yf
import requests
from sqlalchemy import create_engine

# ───────────── 1. Get S&P500 tickers ─────────────
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    sp500 = pd.read_html(requests.get(url, headers=headers).text)[0]
    tickers = sp500["Symbol"].str.replace(".", "-", regex=False).tolist()
    return tickers

# ───────────── 2. Build database ─────────────
def build_database(db_name="stonks.db", years="20y"):
    engine = create_engine(f"sqlite:///{db_name}")
    tickers = get_sp500_tickers()

    for t in tickers:
        print(f"Downloading: {t}")
        data = yf.Ticker(t).history(period=years, auto_adjust=True)  # auto_adjust=True

        if data.empty:
            print(f"No data for {t}")
            continue

        data.reset_index(inplace=True)
        data['Ticker'] = t

        # Target: 1 if tomorrow's adjusted price > today's
        data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

        # Drop unnecessary columns (Dividends and Stock Splits)
        data = data.drop(columns=['Dividends', 'Stock Splits'], errors='ignore')

        # ─── Drop duplicates per Date ───
        data = data.sort_values("Date").drop_duplicates(subset=["Date"], keep="last")

        # ─── Append to SQL ───
        data.to_sql("prices", engine, if_exists="append", index=False)

    print("\nDatabase created successfully!")

# ───────────── 3. Run it ─────────────
build_database()




#import yfinance as yf import requests from sqlalchemy import create_engine # ───────────── 1. Get S&P500 tickers ───────────── def get_sp500_tickers(): url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" headers = {"User-Agent": "Mozilla/5.0"} sp500 = pd.read_html(requests.get(url, headers=headers).text)[0] tickers = sp500["Symbol"].str.replace(".", "-", regex=False).tolist() return tickers # ───────────── 2. Build database ───────────── def build_database(db_name="stonks.db", years="20y"): engine = create_engine(f"sqlite:///{db_name}") tickers = get_sp500_tickers() tickers = get_sp500_tickers() for t in tickers: print(f"Downloading: {t}") data = yf.Ticker(t).history(period=years, auto_adjust=True) # auto_adjust=True if data.empty: print(f"No data for {t}") continue data.reset_index(inplace=True) data['Ticker'] = t # Target: 1 if tomorrow's adjusted price > today's data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int) # Drop unnecessary columns (Dividends and Stock Splits) data = data.drop(columns=['Dividends', 'Stock Splits'], errors='ignore') data.to_sql("prices", engine, if_exists="append", index=False) print("\nDatabase created successfully!") # ───────────── 3. Run it ───────────── build_database()