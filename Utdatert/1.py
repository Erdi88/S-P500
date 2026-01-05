import pandas as pd
from sqlalchemy import create_engine

# Connect to your database
engine = create_engine("sqlite:///stonks.db")

# Query all AAPL rows
df_aapl = pd.read_sql("SELECT * FROM prices WHERE Ticker='AAPL'", engine)

# Show first 5 rows
# print(df_aapl.head())
# print(df_aapl.tail())

# Extra info
print("\nTotal rows:", len(df_aapl))
print("Date range:", df_aapl['Date'].min(), "→", df_aapl['Date'].max())

distinct_tickers = pd.read_sql("SELECT DISTINCT Ticker FROM prices", engine)
tickers = pd.read_sql("SELECT Ticker FROM prices", engine)

print("Number of unique tickers in DB:", len(distinct_tickers))
print("Number of tickers in DB:", len(tickers))
# print("Tickers:", tickers['Ticker'].tolist())

#Printing out all column names


print("Column names:", df_aapl.columns.tolist())