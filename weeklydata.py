from nsepy import get_history
from datetime import date, datetime
import pandas as pd
#import talib
import matplotlib.pyplot as plt

#stocks=[ 'ACC',	 'ACCELYA',	'ACCURACY', 'ACE', 'ACEINTEG', 'ACI', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ADANITRANS', 'ADFFOODS', 'ADL', 'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR', 'ADVENZYMES',]
stocks=[ 'ACC' ]
start_date=date(2021,1,1)
end_date=date.today()
def Importdata():
    for stock in stocks:
        rawdata = get_history(symbol=stock,start=start_date,end=end_date)
        file_name = 'data/{}.csv'.format(stock)
        file_name1 = 'data/weekly/{}.csv'.format(stock)
        df = pd.DataFrame(rawdata)
        df.to_csv(file_name,encoding='utf-8')
        rawdata.index = pd.to_datetime(rawdata.index)
        acc = rawdata.resample('W').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})
        wf = pd.DataFrame(acc)
        wf.to_csv(file_name1,encoding='utf-8')
        print(acc)
        print(stock)

def Loaddata():
    for stock in stocks:
        try:
            rawdata = pd.read_csv('data/{}.csv'.format(stock))     
            
            print(stock)
            print(rawdata)
        except:
            pass
#Loaddata()            
Importdata()