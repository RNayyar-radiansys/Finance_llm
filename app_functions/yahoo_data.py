import pandas as pd
import yfinance as yf

from app_functions.news import article_content

def financial_data(ticker,year, month, limit=12000):
    stock_data = yf.Ticker(ticker)

    hist_data = stock_data_with_time(stock_data, year, month)

    data = stock_data.info
    keep_keys = {
        "longName": "Name",
        "averageAnalystRating": "Analyst rating",
        "forwardPE": "Forward PE",
        "epsForward": "Forward eps",
        "fiftyTwoWeekRange": "One year range",
    }

    data = {keep_keys[k]: v for k, v in data.items() if k in list(keep_keys.keys())}

    news = stock_data.news
    news_links = [n["link"] for n in news if "link" in n]
    news_articles = [article_content(url) for url in news_links]
    news_articles = [n for n in news_articles if n is not None]
    try:
        recommendations = f"{stock_data.recommendations_summary}"
    except:
        recommendations = ""
    news_data = recommendations + "\n\n".join(news_articles)
    if len(news_data) > limit:
        news_data = news_data[:limit]

    return data, news_data, hist_data


def stock_data_with_time(stock_data, year, month):
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(years = year, months = month)
    hist_data = stock_data.history(start=start_date, end=end_date)
    return hist_data