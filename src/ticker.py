import yfinance as yf
import warnings

# Common exchange suffixes
# US FIRST is critical to avoid breaking AAPL / GOOGL
EXCHANGE_SUFFIXES = [
    "",         # US
    ".OL",      # Norway
    ".L",       # London
    ".TO",      # Toronto
    ".ST",      # Stockholm
    ".DE",      # Germany
    ".PA"       # Paris
]

# Manual mapping for tricky / ambiguous tickers
# Use this ONLY when Yahoo symbols differ from common names
MANUAL_TICKER_MAP = {
    "TELENOR": "TEL.OL",     # Telenor ASA
    "MOWI": "MOWI.OL",
    "LERØY": "LYR.OL",
    "LEROY": "LYR.OL",       # fallback without Ø
    # add more only when needed
}

def resolve_ticker(symbol: str) -> str:
    """
    Resolve a stock symbol to a valid Yahoo Finance ticker.

    Priority:
    1. Manual overrides (for known problematic names)
    2. US ticker (no suffix)
    3. International suffixes
    """
    symbol = symbol.upper()

    # 1️⃣ Manual mapping (fast + reliable)
    if symbol in MANUAL_TICKER_MAP:
        return MANUAL_TICKER_MAP[symbol]

    # 2️⃣ Try US ticker FIRST
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = yf.Ticker(symbol).history(period="15d", auto_adjust=False)

        if df is not None and not df.empty:
            return symbol
    except Exception:
        pass

    # 3️⃣ Try exchange suffixes
    for suffix in EXCHANGE_SUFFIXES[1:]:  # skip "" because already tried
        ticker = symbol + suffix
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = yf.Ticker(ticker).history(period="5d", auto_adjust=False)

            if df is not None and not df.empty:
                return ticker

        except Exception:
            continue

    # 4️⃣ Nothing worked
    raise ValueError(f"Ticker '{symbol}' not found on supported exchanges")
