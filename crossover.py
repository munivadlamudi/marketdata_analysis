import yfinance as yf
import pandas as pd
import concurrent.futures


def analyze_stock(stock, data):
    # Your existing analysis logic for each stock
    print("Stock name : ",stock)
    try:
        # stock_data = fetch_stock_data(stock)
        # stock_data = calculate_emas(stock_data, ema_periods)
        crossovers = analyze_crossovers(stock_data)
        
        if len(crossovers) > 0:
            print("EMA Crossovers:",stock)
            for crossover in crossovers:
                print(f"{crossover[0]} - {crossover[1]}")
        else:
            print("No crossovers found.")
        print()
                            
    except FileNotFoundError as e:
            print(f"File not found: {e}")

    


# Define the EMAs you want to calculate
ema_periods = [5, 21, 55]

# Fetch historical stock data
def fetch_stock_data(symbol):
    stock_data = yf.download(symbol, start="2015-01-01", end="2023-01-01")
    return stock_data

# Calculate EMAs
def calculate_emas(data, periods):
    for period in periods:
        data[f'EMA_{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
    return data

# Perform EMA crossover analysis
def analyze_crossovers(data):
    crossovers = []
    for i in range(len(data) - 1):
        if data['ema5'][i] < data['ema21'][i] and data['ema5'][i + 1] > data['ema21'][i + 1]:
            crossovers.append((data.index[i + 1], "Golden Cross"))
        elif data['ema5'][i] > data['ema21'][i] and data['ema5'][i + 1] < data['ema21'][i + 1]:
            crossovers.append((data.index[i + 1], "Death Cross"))
    return crossovers
def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols


if __name__ == "__main__":
    csv_file_path = r'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/stock_symbols.csv' #mainlap
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    max_threads = 50  # Adjust the number of threads as needed
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        # Create a dictionary to map stock symbols to their respective dataframes
        stock_data = {}
        for stock in stock_symbols:
            try:
                data = pd.read_csv(f'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Signals_multi/{stock}.csv')
                stock_data[stock] = data
            except FileNotFoundError as e:
                print(f"File not found: {e}")
        
        # Submit tasks to the thread pool for analysis
        future_to_stock = {executor.submit(analyze_stock, stock, data): stock for stock, data in stock_data.items()}
        
        # Wait for the tasks to complete
        for future in concurrent.futures.as_completed(future_to_stock):
            stock = future_to_stock[future]
            try:
                future.result()
                print(f"Analysis complete for {stock}")
            except Exception as exc:
                print(f"Analysis for {stock} generated an exception: {exc}")

