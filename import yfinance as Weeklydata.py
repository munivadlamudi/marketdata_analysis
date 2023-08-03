import yfinance as yf
import pandas as pd

def get_yahoo_finance_historical_data(stock_symbols, start_date, end_date):
    data = yf.download(stock_symbols, start=start_date, end=end_date)
    return data

def save_data_to_csv(stock_symbol, data, frequency='D'):
    if frequency == 'W':
        data = data.resample('W').last()  # Resample to weekly frequency, taking the last data point for each week
    filename = f"{stock_symbol}_weekly.csv"
    data.reset_index().to_csv(filename, index=False)

if __name__ == "__main__":
    stock_symbols = ["INFY.NS", "Reliance.NS"]  # Replace with the desired stock symbols followed by ".NS" for NSE stocks
    start_date = "2023-01-01"  # Replace with the desired start date
    end_date = "2023-08-02"    # Replace with the desired end date

    for stock_symbol in stock_symbols:
        try:
            stock_data = get_yahoo_finance_historical_data(stock_symbol, start_date, end_date)
            save_data_to_csv(stock_symbol, stock_data, frequency='W')
        except KeyError as e:
            print(f"Failed to fetch data for {stock_symbol}: {e}")
