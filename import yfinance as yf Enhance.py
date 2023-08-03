
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib

def get_yahoo_finance_historical_data(stock_symbols, start_date, end_date):
    data = yf.download(stock_symbols, start=start_date, end=end_date)
    print("data collected")
    return data

def save_data_to_csv(stock_symbol, data):
    print("chekc")
    # filename = f"{stock_symbol}.csv"
    filename = 'C:/Users/mvadlamudi/Desktop/activity/Python/Nifty_All500/{}.csv'.format(stock_symbol)
    data.reset_index().to_csv(filename, index=False)

def emacross(data):
    #print("check")
    return data['ema5'] > data['ema21'] and data['ema21'] > data['ema55']

def Loaddata():
    for stock in stock_symbols:
        try:
            data = pd.read_csv('C:/Users/mvadlamudi/Desktop/activity/Python/Nifty_All500/{}.csv'.format(stock)) 
            print(stock) 
            print("###################################################################################################")
            close = data.iloc[-1]['Close']
            open = data.iloc[-1]['Open']
            high = data.iloc[-1]['High']
            low = data.iloc[-1]['Low']
#### identificatio of streangth candle
            SC_Candle = False
            CH = high - low
            if close > open:
                BH = close - open
            else:
                BH = open - close
            if BH > 0: 
                SC = (BH/CH) * 100
                SC_Candle = False
                if SC > 50:
                    SC_Candle = True

            data['ema5']  = talib.ema(data['Close'], length=5)
            data['ema21']  = talib.ema(data['Close'], length=21)
            data['ema55']  = talib.ema(data['Close'], length=55)
            data['cci8'] =  talib.cci(data['High'],data['Low'],data['Close'],length=8)
            data['cci34_1D'] =  talib.cci(data['High'],data['Low'],data['Close'],length=34)
            data['cci34_1W'] =  talib.cci(data['High'],data['Low'],data['Close'],length=34)
            buy_sell_function(data)
            #report_performance(data)

            #print(buy_sell_function(data)[0])
            data['Buy'] =   buy_sell_function(data)[0]
            data['Sell'] = buy_sell_function(data)[1]
            fresh_buy = data.iloc[-1]['Buy']
            fresh_sell = data.iloc[-1]['Sell']
            print(fresh_buy)
            print(fresh_sell)
            # print(buy_sell_function(data)[fresh_long])
            # print(fresh_short)
            if fresh_buy > 0:
                print("EMA cross fresh Buy : ", data.iloc[-1]['Symbol'])
                print(data.iloc[-1])
                with open("Buy_file.txt", "a") as f:
                    f.write("new text")
            if fresh_sell > 0:
                print("EMA cross fresh Sell : ", data.iloc[-1]['Symbol'])
                with open("Sell_file.txt", "a") as f:
                    f.write("new text")

            #print(data.iloc[-1])
            #data['emacross'] = data.apply(emacross, axis=1)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # if data.iloc[-1]['emacross']:
            #     print("@@@@@@@@@@@    ema cross over @@@@@@@@@@@@")
            #     print(stock)
            #     #print(rawdata)
        except:
            print("you are in exception")
            pass

def buy_sell_function(data):
    buy_list = []
    sell_list = []
    fresh_long = False
    fresh_short = False
    flag_long = False
    flag_short = False
    for i in range(0,len(data)):
        if data['ema21'][i] < data['ema55'][i] and data['ema21'][i] > data['ema5'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_short = True
            fresh_short = True
        elif data['ema21'][i] > data['ema55'][i] and data['ema21'][i] < data['ema5'][i] and flag_short == False and flag_long == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
            fresh_long = True
        elif flag_short == True and data['ema5'][i] > data['ema21'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False
        elif flag_long == True and data['ema5'][i] < data['ema21'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
    
    return (buy_list, sell_list,fresh_short,fresh_long)

def Importdata():
       for stock_symbol in stock_symbols:
        print(stock_symbol)
        try:
            stock_data = get_yahoo_finance_historical_data(stock_symbol, start_date, end_date)
            save_data_to_csv(stock_symbol, stock_data)
        except KeyError as e:
            print(f"Failed to fetch data for {stock_symbol}: {e}")

if __name__ == "__main__":
    # Replace with the desired stock symbols followed by ".NS" for NSE stocks
    stock_symbols = ['ADANIENT.NS',	'TCS.NS',	'RELIANCE.NS',	'AXISBANK.NS',	'INDUSINDBK.NS',	'ULTRACEMCO.NS',	'ICICIBANK.NS',	'NESTLEIND.NS',	'WIPRO.NS',	'SBIN.NS',	'ONGC.NS',	'DIVISLAB.NS',	'HCLTECH.NS',	'INFY.NS',	'TATACONSUM.NS',	'ASIANPAINT.NS',	'SUNPHARMA.NS',	'ITC.NS',	'BAJAJFINSV.NS',	'HDFC.NS',	'APOLLOHOSP.NS',	'CIPLA.NS',	'BAJAJ-AUTO.NS',	'JSWSTEEL.NS',	'KOTAKBANK.NS',	'TITAN.NS',	'COALINDIA.NS',	'GRASIM.NS',	'BPCL.NS',	'HINDALCO.NS',	'HDFCBANK.NS',	'HEROMOTOCO.NS',	'DRREDDY.NS',	'BAJFINANCE.NS',	'TATASTEEL.NS',	'TECHM.NS',	'POWERGRID.NS',	'HDFCLIFE.NS',	'ADANIPORTS.NS',	'NTPC.NS',	'BRITANNIA.NS',	'MARUTI.NS',	'LT.NS',	'M&M.NS',	'BHARTIARTL.NS',	'HINDUNILVR.NS',	'TATAMOTORS.NS',	'UPL.NS',	'EICHERMOT.NS',	'SBILIFE.NS',] 
    start_date = "2023-01-01"  # Replace with the desired start date
    end_date = "2023-08-02"    # Replace with the desired end date
    print("script starting")
    Importdata()   
    Loaddata()