from datetime import date
import pandas as pd
import concurrent.futures
import pandas_ta as talib

def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols

def process_stock(stock):
    try:
        # Load data for processing
        data = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock))
        data1 = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock))
        print("stock name : ",stock)              
        # Save processed data
        out_file_name1 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)
        out_file_name2 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock)

        data['ema5']  = talib.ema(data['Close'], length=5)
        data['ema21']  = talib.ema(data['Close'], length=21)
        data['ema55']  = talib.ema(data['Close'], length=55)
        data['cci8'] =  talib.cci(data['High'],data['Low'],data['Close'],length=8)
        data['cci34_1D'] =  talib.cci(data['High'],data['Low'],data['Close'],length=34)
        data['Date_new'] = pd.to_datetime(data['Date'])
        data['Year'] = data['Date_new'].dt.year
        data['week_number'] = data["Date_new"].dt.isocalendar().week
        # weekly_data = data.resample('W').last()

        data1['ema5']  = talib.ema(data1['Close'], length=5)
        data1['ema21']  = talib.ema(data1['Close'], length=21)
        data1['ema55']  = talib.ema(data1['Close'], length=55)
        # data1['cci8'] =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=8)
        data1['cci34_1W'] =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=34)
        data1['Date_new'] = pd.to_datetime(data1['Date'])
        data1['Year'] = data1['Date_new'].dt.year
        data1['week_number'] = data1["Date_new"].dt.isocalendar().week

        ou = pd.DataFrame(data)
        ou.to_csv(out_file_name1, encoding='utf-8')
        ouw = pd.DataFrame(data1)
        ouw.to_csv(out_file_name2, encoding='utf-8')
        
        return stock, data, data1
    except KeyError as e:
        print(f"Exception processing {stock}: {e}")
        return None

def process_stocks(stock_symbols):
    processed_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_stock, stock_symbols)
        for result in results:
            if result is not None:
                processed_data.append(result)
    return processed_data

if __name__ == "__main__":
    csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv'
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    processed_data = process_stocks(stock_symbols)
    print("Processing complete.")
