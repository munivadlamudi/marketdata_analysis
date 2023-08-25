from datetime import date,datetime,timedelta
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib
import concurrent.futures



# def emacross(data):
#     #print("check")
#     return data['ema5'] > data['ema21'] and data['ema21'] > data['ema55']

# def Loaddata():
#     for stock in stock_symbols:
#         try:
#             data = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)) 
#             data1 = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock))  
#             out_file_name1 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)
#             out_file_name2 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock)
#             print(stock) 
#             print("###################################################################################################")
#             close = data.iloc[-1]['Close']
#             open_price = data.iloc[-1]['Open']
#             high = data.iloc[-1]['High']
#             low = data.iloc[-1]['Low']
# #### identificatio of streangth candle
#             SC_Candle = False
#             CH = high - low
#             if close > open_price:
#                 BH = close - open_price
#             else:
#                 BH = open_price - close
#             if BH > 0: 
#                 SC = (BH/CH) * 100
#                 SC_Candle = False
#                 if SC > 50:
#                     SC_Candle = True

#             data['ema5']  = talib.ema(data['Close'], length=5)
#             data['ema21']  = talib.ema(data['Close'], length=21)
#             data['ema55']  = talib.ema(data['Close'], length=55)
#             data['cci8'] =  talib.cci(data['High'],data['Low'],data['Close'],length=8)
#             data['cci34_1D'] =  talib.cci(data['High'],data['Low'],data['Close'],length=34)
#             data['Date_new'] = pd.to_datetime(data['Date'])
#             data['Year'] = data['Date_new'].dt.year
#             data['week_number'] = data["Date_new"].dt.isocalendar().week
#             # weekly_data = data.resample('W').last()

#             data1['cci34_1W'] =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=34)
#             data1['Date_new'] = pd.to_datetime(data1['Date'])
#             data1['Year'] = data1['Date_new'].dt.year
#             data1['week_number'] = data1["Date_new"].dt.isocalendar().week

#             ou = pd.DataFrame(data)
#             ou.to_csv(out_file_name1,encoding='utf-8')
          
#             ouw = pd.DataFrame(data1)
#             ouw.to_csv(out_file_name2,encoding='utf-8')
                     
           
#         except  KeyError as e:
#             print(f"you are in exception : {e}")
        

# def buy_sell_function(data):
#     buy_list = []
#     sell_list = []
#     fresh_long = False
#     fresh_short = False
#     flag_long = False
#     flag_short = False
#     for i in range(0,len(data)):
#         if data['ema21'][i] < data['ema55'][i] and data['ema21'][i] > data['ema5'][i] and flag_long == False and flag_short == False:
#             buy_list.append(data['Close'][i])
#             sell_list.append(np.nan)
#             flag_short = True
#             fresh_short = True
#         elif data['ema21'][i] > data['ema55'][i] and data['ema21'][i] < data['ema5'][i] and flag_short == False and flag_long == False:
#             buy_list.append(data['Close'][i])
#             sell_list.append(np.nan)
#             flag_long = True
#             fresh_long = True
#         elif flag_short == True and data['ema5'][i] > data['ema21'][i]:
#             sell_list.append(data['Close'][i])
#             buy_list.append(np.nan)
#             flag_short = False
#         elif flag_long == True and data['ema5'][i] < data['ema21'][i]:
#             sell_list.append(data['Close'][i])
#             buy_list.append(np.nan)
#             flag_long = False
#         else:
#             buy_list.append(np.nan)
#             sell_list.append(np.nan)
    
#     return (buy_list, sell_list,fresh_short,fresh_long)
def import_stock_symbols_from_csv(filename):
    symbol_df = pd.read_csv(filename)
    stock_symbols = symbol_df['stock_symbol'].tolist()
    return stock_symbols
def process_stocks(stock_symbols):
    processed_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_stock, stock_symbols)
        for result in results:
            if result is not None:
                processed_data.append(result)
    return processed_data
def process_stock(stock):
    try:
        # data = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock))
        # data1 = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock))
        data = pd.read_csv('C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All/{}.csv'.format(stock))
        data1 = pd.read_csv('C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All_weekly/{}.csv'.format(stock))
        # ... (rest of your data processing code)
        # out_file_name1 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)
        # out_file_name2 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock)

        out_file_name1 = 'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All/{}.csv'.format(stock)
        out_file_name2 = 'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Nifty_All_weekly/{}.csv'.format(stock)
        print(stock) 
        print("###################################################################################################")
        close = data.iloc[-1]['Close']
        open_price = data.iloc[-1]['Open']
        high = data.iloc[-1]['High']
        low = data.iloc[-1]['Low']
#### identificatio of streangth candle
        # SC_Candle = False
        # CH = high - low
        # if close > open_price:
        #     BH = close - open_price
        # else:
        #     BH = open_price - close
        # if BH > 0: 
        #     SC = (BH/CH) * 100
        #     SC_Candle = False
        #     if SC > 50:
        #         SC_Candle = True

        data['ema5']  = talib.ema(data['Close'], length=5)
        data['ema21']  = talib.ema(data['Close'], length=21)
        data['ema55']  = talib.ema(data['Close'], length=55)
        data['cci8'] =  talib.cci(data['High'],data['Low'],data['Close'],length=8)
        data['cci34_1D'] =  talib.cci(data['High'],data['Low'],data['Close'],length=34)
        data['Date_new'] = pd.to_datetime(data['Date'])
        data['Year'] = data['Date_new'].dt.year
        data['week_number'] = data["Date_new"].dt.isocalendar().week
        # weekly_data = data.resample('W').last()

        data1['cci34_1W'] =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=34)
        data1['Date_new'] = pd.to_datetime(data1['Date'])
        data1['Year'] = data1['Date_new'].dt.year
        data1['week_number'] = data1["Date_new"].dt.isocalendar().week

        ou = pd.DataFrame(data)
        ou.to_csv(out_file_name1,encoding='utf-8')
        #writting new file for weekly data in /data/output_weekly
        ouw = pd.DataFrame(data1)
        ouw.to_csv(out_file_name2,encoding='utf-8')
        
        return stock, data, data1
    except KeyError as e:
        print(f"Exception processing {stock}: {e}")
        return None
if __name__ == "__main__":
    
    # csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv'
    csv_file_path = r'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/marketdata_analysis/stock_symbols.csv' #mainlap
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    start_date = "2023-01-01"  # Replace with the desired start date
  
    end_date = date.today()
    print("EMA CCI ploting script starting")
    #Importdata()   
    processed_data = process_stocks(stock_symbols)
    # Loaddata()