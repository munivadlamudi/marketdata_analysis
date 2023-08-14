from datetime import date,datetime,timedelta
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib

def get_yahoo_finance_historical_data(stock_symbols, start_date, end_date):
    data = yf.download(stock_symbols, start=start_date, end=end_date)
    print("data collected")
    return data

def save_data_to_csv(stock_symbol, data):
    
    filename = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock_symbol)
    data.reset_index().to_csv(filename, index=False)


def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols

def Importdata(stock_symbols, start_date, end_date):
    for stock_symbol in stock_symbols:
        print(stock_symbol)
        try:
            stock_data = get_yahoo_finance_historical_data(stock_symbol, start_date, end_date)
            save_data_to_csv(stock_symbol, stock_data)
        except KeyError as e:
            print(f"Failed to fetch data for {stock_symbol}: {e}")

if __name__ == "__main__":
    csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv'
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    current_date = datetime.today().date()
    tomorrow_date = current_date + timedelta(days=1)
    print("Current Date:", current_date)
    print("Tomorrow's Date:", tomorrow_date)
    start_date = "2015-01-01"  # Replace with the desired start date
    end_date = tomorrow_date
    print("Daily data download script starting for the date:", tomorrow_date)
    Importdata(stock_symbols, start_date, end_date)