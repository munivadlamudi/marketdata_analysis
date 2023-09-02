from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib
import subprocess
import time
import multiprocessing

# Your other functions and imports...

def process_stock(stock):
    try:
        # Your existing processing code for each stock here...
        # ...
        buy_entry = []
        entry_type = []
        exit_buy = []
        sell_entry = []
        exit_sell = []
        buy_list = []
        sell_list = []
        data = pd.read_csv('C:/Users/muniv/Desktop/Market/Compare_multi/{}.csv'.format(stock)) 
        out_file_name1 = 'C:/Users/muniv/Desktop/Market/Signals_multi/{}.csv'.format(stock)        
        # data = pd.read_csv('/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Compare_multi/{}.csv'.format(stock)) 
        # out_file_name1 = '/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Signals_multi/{}.csv'.format(stock)      
        buy_sell_function(data, buy_list, sell_list, buy_entry, sell_entry, exit_buy, exit_sell,entry_type)
        #report_performance(data)
        print("Name of the stock : ",stock)
        #print(buy_sell_function(data)[0])
        
        data['Buy'] =   buy_list
        data['Sell'] = sell_list
        data['Buy_Entry'] = buy_entry
        data['exit_buy'] = exit_buy
        data['sell_Entry'] = sell_entry
        data['exit_sell'] = exit_sell
        data['entry_type'] = entry_type
        
        fresh_buy = data.iloc[-1]['Buy_Entry']
        fresh_sell = data.iloc[-1]['sell_Entry']
        fresh_buy_1 = data.iloc[-2]['Buy_Entry']
        fresh_sell_1 = data.iloc[-2]['sell_Entry']
        # print("fresh_buy : ",fresh_buy)
        # print("fresh_sell : ",fresh_sell)

        ou = pd.DataFrame(data)
        ou.to_csv(out_file_name1,encoding='utf-8')

        # if not pd.isna(fresh_buy) and pd.isna(fresh_buy_1):
        if not pd.isna(fresh_buy):
            # print("Write into Buy file") 
            # Append data to buy_data list
            buy_data.append({
                'stock': stock,
                'Comment': fresh_buy,
                'Date ': data['Date_new'].iloc[-1],
                'Closing Price': data['Close'].iloc[-1],
                'entry_type':data['entry_type'].iloc[-1]
            })

        # if not pd.isna(fresh_sell) and pd.isna(fresh_sell_1):
        if not pd.isna(fresh_sell):
            # print("check signals for sell #####")
            # print("Write into Sell file")
            # Append data to sell_data list
            sell_data.append({
                'stock': stock,
                'Comment': fresh_sell,
                'Date ': data['Date_new'].iloc[-1],
                'Closing Price': data['Close'].iloc[-1]
            })

        # Create DataFrames from the lists
        Buy_result = pd.DataFrame(buy_data)
        Sell_result = pd.DataFrame(sell_data)

        # Save DataFrames to CSV files
        if not Buy_result.empty:
            Buy_result.to_csv(Buy_result_data, encoding='utf-8', index=False)

        if not Sell_result.empty:
            Sell_result.to_csv(Sell_result_data, encoding='utf-8', index=False)
    # Place the entire processing logic for a single stock here...

    except KeyError as e:
        print(f"You are in exception: {e}")
def buy_sell_function(data, buy_list, sell_list, buy_entry, sell_entry, exit_buy, exit_sell,entry_type):
    
    
    fresh_long = False
    fresh_short = False
    flag_long = False
    flag_short = False
    for i in range(0,len(data)):

        close = data.iloc[i]['Close']
        open_price = data.iloc[i]['Open']
        high = data.iloc[i]['High']
        low = data.iloc[i]['Low']
        #### identificatio of streangth candle
        SC_Candle_B = False
        SC_Candle_S = False
        CH = high - low
        if close > open_price:
            BH = close - open_price
            if BH > 0: 
                SC = (BH/CH) * 100
                SC_Candle_B = False
                if SC > 50:
                    SC_Candle_B = True
    
        else:
            BH = open_price - close
            if BH > 0: 
                SC = (BH/CH) * 100
                SC_Candle_S = False
                if SC > 50:
                    SC_Candle_S = True
        
        EMAALB = (data['ema5'][i] - data['ema21'][i])/(data['ema21'][i] - data['ema55'][i])
        EMAALS = (data['ema55'][i] - data['ema21'][i])/(data['ema21'][i] - data['ema5'][i]) 
        
        EMAALrangeB = (((EMAALB >= 0.381 and EMAALB <= 2.22) and (data['cci34_1W'][i] >= 100 and data['cci34_1D'][i] >= 100)) or (data['cci34_1W'][i] >= 100 and data['cci34_1D'][i] >= 100))
        EMAALrangeB = 1 if EMAALrangeB else 0
        EMAALrangeB1 = ((data['cci34_1W'][i] > -70 and data['cci34_1D'][i] >= 100) or (data['cci34_1W'][i] > 70 and data['cci34_1D'][i] >= 0))
        EMAALrangeB1 = 1 if EMAALrangeB1 else 0
        EMAALrangeB2 = ((EMAALB >= 0.381 and EMAALB <= 2.5) and (data['cci34_1W'][i] >= 100 and data['cci34_1D'][i] >= 100))
        EMAALrangeB2 = 1 if EMAALrangeB2 else 0
        EMAALrangeS = (((EMAALS >= 0.381 and EMAALS <= 2.22) and (data['cci34_1W'][i] <= 100 and data['cci34_1D'][i] <= -100)) or (data['cci34_1W'][i] <= -100 and data['cci34_1D'][i] <= -100))
        EMAALrangeS = 1 if EMAALrangeS else 0
        EMAALrangeS1 = ((data['cci34_1W'][i] < 70 and data['cci34_1D'][i] <= -100) or (data['cci34_1W'][i] < 70 and data['cci34_1D'][i] <= 0))
        EMAALrangeS1 = 1 if EMAALrangeS1 else 0

        # if SC_Candle_B and (EMAALrangeB or EMAALrangeB1) and flag_short == False and flag_long == False :
        if ((SC_Candle_B and (EMAALrangeB or EMAALrangeB1)) or (EMAALrangeB2)) and flag_long == False :
       # if EMAALrangeB2 and flag_long == False :    
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
            fresh_long = True
            if EMAALrangeB2:
                entry_type.append("Golden entry")
            else:
                entry_type.append(np.nan)
            buy_entry.append("freshe buy")
            sell_entry.append(np.nan)
            exit_buy.append(np.nan)
            exit_sell.append(np.nan)
        elif SC_Candle_S and (EMAALrangeS or EMAALrangeS1) and flag_long == False and flag_short == False :
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = True
            fresh_short = True
            sell_entry.append("Fresh sell")
            entry_type.append(np.nan)
            buy_entry.append(np.nan)
            exit_buy.append(np.nan)
            exit_sell.append(np.nan)
        elif flag_short == True and (((data['ema5'][i] > data['ema21'][i]) or data['cci34_1D'][i] >= 0 ) and data['cci34_1W'][i] > -100):
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False
            exit_sell.append("Exit sell")
            entry_type.append(np.nan)
            exit_buy.append(np.nan)
            buy_entry.append(np.nan)
            sell_entry.append(np.nan)
        elif flag_long == True and (((data['ema5'][i] < data['ema21'][i]) or data['cci34_1D'][i] <= 0 ) and data['cci34_1W'][i] < 100):
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
            exit_buy.append("Exit buy")
            entry_type.append(np.nan)
            exit_sell.append(np.nan)
            buy_entry.append(np.nan)
            sell_entry.append(np.nan)
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
            entry_type.append(np.nan)
            buy_entry.append(np.nan)
            sell_entry.append(np.nan)
            exit_buy.append(np.nan)
            exit_sell.append(np.nan)
    return (data, buy_list, sell_list, buy_entry, sell_entry, exit_buy, exit_sell,entry_type)
def main():
    csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv'
    # csv_file_path = r'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/stock_symbols.csv' #mainlap
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    # stock_symbols = ['CHEMPLASTS.NS']
    print("Script starting")
    
    
    # Use ThreadPoolExecutor to parallelize processing for multiple stocks
    max_threads = 25 # You can adjust the number of threads as needed
    with ThreadPoolExecutor(max_threads) as executor:
        executor.map(process_stock, stock_symbols)

    print("All stocks processed")
    
def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols
def run_program1():
    subprocess.run(["python", "import yfinance as Dailydata_with_multithread.py"])

def run_program2():
    subprocess.run(["python", "import yfinance as Weeklydata_with_multithread.py"])
if __name__ == "__main__":
    buy_data = []
    sell_data = []
    Buy_result_data='C:/Users/muniv/Desktop/Market/Buy_Entry.csv'
    Sell_result_data='C:/Users/muniv/Desktop/Market/Sell_Entry.csv'
    # Buy_result_data='C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/Buy_Entry.csv'
    # Sell_result_data='C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/Sell_Entry.csv'
    start_time = time.time()
    # Load existing Buy result data if it exists
    try:
        existing_buy_data = pd.read_csv(Buy_result_data)
        buy_data.extend(existing_buy_data.to_dict('records'))
    except FileNotFoundError:
        existing_buy_data = None
    
    # Load existing Sell result data if it exists
    try:
        existing_sell_data = pd.read_csv(Sell_result_data)
        sell_data.extend(existing_sell_data.to_dict('records'))
    except FileNotFoundError:
        existing_sell_data = None
    process1 = multiprocessing.Process(target=run_program1)
    process2 = multiprocessing.Process(target=run_program2)
    # subprocess.run(["python", "import yfinance as Dailydata_with_multithread.py"])
    # subprocess.run(["python", "import yfinance as Weeklydata_with_multithread.py"])
    process1.start()
    process2.start()
    
    process1.join()
    process2.join()

    print("Both programs have finished running.")
    subprocess.run(["python", "data and analyze_adding more_with_multitreading_enhance_updated.py"])
    subprocess.run(["python", "file compare_fulllist_multithreading_enhance.py"])
    main()
    subprocess.run(["python", "Report_generation_multi_enhance.py"])
    # subprocess.run(["python", "Gmail_with_attachments_without_manual.py"])
    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total runtime: {total_time:.2f} seconds")
    print("Report generation complete.")