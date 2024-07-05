import plotly.graph_objs as go
import streamlit as st
import requests
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup

from app_functions.yahoo_data import financial_data
from app_functions.yahoo_ticker import valid_ticker
from app_functions.llm_agents import openai_summarizer, groq_summarizer

def plot_stock_data(ticker, data):
    trace = go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name=ticker,
    )

    layout = go.Layout(title=f"{ticker} Stock Data (5 Years)")
    fig = go.Figure(data=[trace], layout=layout)
    return fig

# Set the page title and favicon
st.set_page_config(page_title="Stock TalkAI", page_icon=":chart_with_upwards_trend:")

# Add a title and description
st.title("Stock TalkAI 💸")
st.markdown("Enter a stock ticker 📈 and get a summary of its financial data using GPT-4 Language Model 🧠.")

# Get user input for the stock ticker
ticker = st.text_input("Enter the stock ticker:")

# Fetch and display financial data when the user clicks the button
if st.button("Get Summary 📊"):
    if ticker and valid_ticker(ticker):
        data, news, stock_data = financial_data(ticker)

        stock_chart = plot_stock_data(ticker, stock_data)
        st.plotly_chart(stock_chart)
        # summary = openai_summarizer(news, ticker)
        # print(summary)
        st.write("\n".join([f"- **{k}:** {v} " for k, v in data.items()]))
        # st.write(f"Is {ticker} a buy?")
        st.write(f"📰  {ticker} news summary is: ")
        st.success("OpenAI Summarizer")
        st.write(openai_summarizer(news, ticker))
        st.success("Groq Summarizer")
        st.write(groq_summarizer(news, ticker))

    else:
        st.warning("Please enter a valid stock ticker. i.e. MSFT")