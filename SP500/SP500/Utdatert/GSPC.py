from Prediction import load_price_data
import yfinance as yf
import pandas as pd
import sqlite3

DB_NAME = "GSPC.db"
TABLE_NAME = "gspc_prices"
TICKER = "^GSPC"

def save_to_database(df: pd.DataFrame, db_name: str, table_name: str) -> None:
    """
    Save DataFrame to a SQLite database.
    """
    conn = sqlite3.connect(db_name)
    df.to_sql(
        name=table_name,
        con=conn,
        if_exists="replace",  # change to "append" if updating incrementally
        index=False
    )
    conn.close()


def load_from_database(db_name: str, table_name: str) -> pd.DataFrame:
    """
    Load data from SQLite database.
    """
    conn = sqlite3.connect(db_name)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


def main():
    print("Downloading S&P 500 (^GSPC) data...")
    gspc_df = load_price_data(TICKER)

    print("Saving data to database...")
    save_to_database(gspc_df, DB_NAME, TABLE_NAME)

    print("Verifying saved data...")
    test_df = load_from_database(DB_NAME, TABLE_NAME)
    print(test_df.head())

    print("Done.")


if __name__ == "__main__":
    main()