from datetime import date, datetime, timedelta
import yfinance as yf
import pandas as pd
import concurrent.futures
import multiprocessing

# Your existing functions here...
def get_yahoo_finance_historical_data(stock_symbols, start_date, end_date):
    data = yf.download(stock_symbols, start=start_date, end=end_date)
    print("data collected")
    return data

def save_data_to_csv(stock_symbol, data):
    
    #filename = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock_symbol) #jaikeerthlap
    filename = 'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All/{}.csv'.format(stock_symbol) #mainlap
    data.reset_index().to_csv(filename, index=False)

def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols

def process_stocks_chunk(stock_symbols, start_date, end_date, chunk_size=100):
    with multiprocessing.Pool() as pool:
        for i in range(0, len(stock_symbols), chunk_size):
            chunk = stock_symbols[i:i + chunk_size]
            print(f"Processing chunk {i//chunk_size + 1}")
            results = pool.starmap(get_and_save_data, [(stock_symbol, start_date, end_date) for stock_symbol in chunk])

def get_and_save_data(stock_symbol, start_date, end_date):
    try:
        stock_data = get_yahoo_finance_historical_data(stock_symbol, start_date, end_date)
        save_data_to_csv(stock_symbol, stock_data)
    except KeyError as e:
        print(f"Failed to fetch data for {stock_symbol}: {e}")
def Importdata(stock_symbols, start_date, end_date):
    for stock_symbol in stock_symbols:
        print(stock_symbol)
        try:
            stock_data = get_yahoo_finance_historical_data(stock_symbol, start_date, end_date)
            save_data_to_csv(stock_symbol, stock_data)
        except KeyError as e:
            print(f"Failed to fetch data for {stock_symbol}: {e}")

if __name__ == "__main__":
    
    # csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv' #jaikeerthlap
    csv_file_path = r'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/stock_symbols.csv' #mainlap
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    current_date = datetime.today().date()
    tomorrow_date = current_date + timedelta(days=1)
    print("Current Date:", current_date)
    print("Tomorrow's Date:", tomorrow_date)
    start_date = "2015-01-01"  # Replace with the desired start date
    end_date = tomorrow_date
    chunk_size = 100  # Number of stocks to process in each chunk
    process_stocks_chunk(stock_symbols, start_date, end_date, chunk_size)
    # Importdata(stock_symbols, start_date, end_date)
