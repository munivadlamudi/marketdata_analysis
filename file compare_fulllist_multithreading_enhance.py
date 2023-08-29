import concurrent.futures
import pandas as pd

def process_stock(stock):
    try:
        print("Processing stock:", stock)
        main_df = pd.read_csv(f'C:/Users/muniv/Desktop/Market/Nifty_A1426/{stock}.csv')
        weekly_df = pd.read_csv(f'C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{stock}.csv')
        # main_df = pd.read_csv(f'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All/{stock}.csv')
        # weekly_df = pd.read_csv(f'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All_weekly/{stock}.csv')
        merged_df = pd.merge(main_df, weekly_df[['Year', 'week_number', 'cci34_1W']],
                            left_on=['Year', 'week_number'], right_on=['Year', 'week_number'],
                            how='left')

        merged_df['cci34_1W'].fillna(merged_df['cci34_1W'], inplace=True)

        merged_df.to_csv(f'C:/Users/muniv/Desktop/Market/Compare_multi/{stock}.csv', index=False)
        # merged_df.to_csv(f'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Compare_multi/{stock}.csv', index=False)
    except KeyError as e:
        print(f"Exception for stock {stock}: {e}")

def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols

if __name__ == "__main__":
    csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv'
    # csv_file_path = r'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/stock_symbols.csv' #mainlap
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)

    print("Compare and cci 34 script starting")

    # Use ThreadPoolExecutor to process stocks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_stock, stock_symbols)
