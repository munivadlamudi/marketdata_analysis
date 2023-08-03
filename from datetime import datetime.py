import yfinance as yf
import pandas as pd

def get_yahoo_finance_historical_data(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data

if __name__ == "__main__":
    stock_symbol = "INFY.NS"  # Replace with the desired stock symbol followed by ".NS" for NSE stocks
    start_date = "2023-01-01"  # Replace with the desired start date
    end_date = "2023-08-02"    # Replace with the desired end date

    historical_data = get_yahoo_finance_historical_data(stock_symbol, start_date, end_date)
    print(historical_data)
