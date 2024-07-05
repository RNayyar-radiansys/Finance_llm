import yfinance as yf


def valid_ticker(ticker):
    try:
        stock_info = yf.Ticker(ticker)
        stock_info.info["shortName"]
        return True
    except Exception:
        return False