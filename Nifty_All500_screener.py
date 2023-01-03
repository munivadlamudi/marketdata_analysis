from nsepy import get_history
from datetime import date,datetime
import pandas as pd
import numpy as np
import pandas_ta as talib
#import talib
import matplotlib.pyplot as plt

#stocks=[ 'ACC',	 'ACCELYA',	'ACCURACY', 'ACE', 'ACEINTEG', 'ACI', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ADANITRANS', 'ADFFOODS', 'ADL', 'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR', 'ADVENZYMES',]
#stocks=['ADANIENT',	'TCS',	'RELIANCE',	'AXISBANK',	'INDUSINDBK',	'ULTRACEMCO',	'ICICIBANK',	'NESTLEIND',	'WIPRO',	'SBIN',	'ONGC',	'DIVISLAB',	'HCLTECH',	'INFY',	'TATACONSUM',	'ASIANPAINT',	'SUNPHARMA',	'ITC',	'BAJAJFINSV',	'HDFC',	'APOLLOHOSP',	'CIPLA',	'BAJAJ-AUTO',	'JSWSTEEL',	'KOTAKBANK',	'TITAN',	'COALINDIA',	'GRASIM',	'BPCL',	'HINDALCO',	'HDFCBANK',	'HEROMOTOCO',	'DRREDDY',	'BAJFINANCE',	'TATASTEEL',	'TECHM',	'POWERGRID',	'HDFCLIFE',	'ADANIPORTS',	'NTPC',	'BRITANNIA',	'MARUTI',	'LT',	'M&M',	'BHARTIARTL',	'HINDUNILVR',	'TATAMOTORS',	'UPL',	'EICHERMOT',	'SBILIFE',]
#stocks=['INDIGO','ZOMATO','MPHASIS','BANKBARODA','BAJAJHLDNG','BEL','HAVELLS','BOSCHLTD','TATAPOWER','NAUKRI','LICI','PAYTM','GAIL','HAL',	'ADANITRANS',	'MCDOWELL-N',	'CHOLAFIN',	'ICICIPRULI',	'MARICO',	'BERGEPAINT',	'SRF',	'SIEMENS',	'SBICARD',	'ATGL',	'DMART',	'COLPAL',	'IRCTC',	'PGHH',	'BIOCON',	'ADANIGREEN',	'LTIM',	'BANDHANBNK',	'MUTHOOTFIN',	'AMBUJACEM',	'IOC',	'SHREECEM',	'VEDL',	'PIIND',	'PIDILITIND',	'ICICIGI',	'HDFCAMC',	'GODREJCP',	'MOTHERSON',	'NYKAA',	'DABUR',	'ACC',	'TORNTPHARM',	'DLF',	'GLAND',	'INDUSTOWER',]
stocks=['3MINDIA',	'ABB',	'ACC',	'AIAENG',	'APLAPOLLO',	'AUBANK',	'AARTIDRUGS',	'AAVAS',	'ABBOTINDIA',	'ADANIENT',	'ADANIGREEN',	'ADANIPORTS',	'ATGL',	'ADANITRANS',	'AWL',	'ABCAPITAL',	'ABFRL',	'ABSLAMC',	'AEGISCHEM',	'AETHER',	'AFFLE',	'AJANTPHARM',	'APLLTD',	'ALKEM',	'ALKYLAMINE',	'ALLCARGO',	'ALOKINDS',	'AMARAJABAT',	'AMBER',	'AMBUJACEM',	'ANGELONE',	'ANURAS',	'APOLLOHOSP',	'APOLLOTYRE',	'APTUS',	'ASAHIINDIA',	'ASHOKLEY',	'ASIANPAINT',	'ASTERDM',	'ASTRAZEN',	'ASTRAL',	'ATUL',	'AUROPHARMA',	'AVANTIFEED',	'DMART',	'AXISBANK',	'BASF',	'BSE',	'BAJAJ-AUTO',	'BAJAJELEC',	'BAJFINANCE',	'BAJAJFINSV',	'BAJAJHLDNG',	'BALAMINES',	'BALKRISIND',	'BALRAMCHIN',	'BANDHANBNK',	'BANKBARODA',	'BANKINDIA',	'MAHABANK',	'BATAINDIA',	'BAYERCROP',	'BERGEPAINT',	'BDL',	'BEL',	'BHARATFORG',	'BHEL',	'BPCL',	'BHARATRAS',	'BHARTIARTL',	'BIOCON',	'BIRLACORPN',	'BSOFT',	'BLUEDART',	'BLUESTARCO',	'BBTC',	'BORORENEW',	'BOSCHLTD',	'BRIGADE',	'BCG',	'BRITANNIA',	'MAPMYINDIA',	'CCL',	'CESC',	'CGPOWER',	'CRISIL',	'CSBBANK',	'CAMPUS',	'CANFINHOME',	'CANBK',	'CAPLIPOINT',	'CGCL',	'CARBORUNIV',	'CASTROLIND',	'CEATLTD',	'CENTRALBK',	'CDSL',	'CENTURYPLY',	'CENTURYTEX',	'CERA',	'CHALET',	'CHAMBLFERT',	'CHEMPLASTS',	'CHOLAHLDNG',	'CHOLAFIN',	'CIPLA',	'CUB',	'CLEAN',	'COALINDIA',	'COCHINSHIP',	'COFORGE',	'COLPAL',	'CAMS',	'CONCOR',	'COROMANDEL',	'CREDITACC',	'CROMPTON',	'CUMMINSIND',	'CYIENT',	'DCMSHRIRAM',	'DLF',	'DABUR',	'DALBHARAT',	'DEEPAKFERT',	'DEEPAKNTR',	'DELHIVERY',	'DELTACORP',	'DEVYANI',	'DHANI',	'DBL',	'DIVISLAB',	'DIXON',	'LALPATHLAB',	'DRREDDY',	'EIDPARRY',	'EIHOTEL',	'EPL',	'EASEMYTRIP',	'EDELWEISS',	'EICHERMOT',	'ELGIEQUIP',	'EMAMILTD',	'ENDURANCE',	'ENGINERSIN',	'EQUITASBNK',	'ESCORTS',	'EXIDEIND',	'FDC',	'NYKAA',	'FEDERALBNK',	'FACT',	'FINEORG',	'FINCABLES',	'FINPIPE',	'FSL',	'FORTIS',	'GRINFRA',	'GAIL',	'GMMPFAUDLR',	'GMRINFRA',	'GALAXYSURF',	'GARFIBRES',	'GICRE',	'GLAND',	'GLAXO',	'GLENMARK',	'GOCOLORS',	'GODFRYPHLP',	'GODREJAGRO',	'GODREJCP',	'GODREJIND',	'GODREJPROP',	'GRANULES',	'GRAPHITE',	'GRASIM',	'GESHIP',	'GREENPANEL',	'GRINDWELL',	'GUJALKALI',	'GAEL',	'FLUOROCHEM',	'GUJGASLTD',	'GNFC',	'GPPL',	'GSFC',	'GSPL',	'HEG',	'HCLTECH',	'HDFCAMC',	'HDFCBANK',	'HDFCLIFE',	'HFCL',	'HLEGLAS',	'HAPPSTMNDS',	'HATSUN',	'HAVELLS',	'HEROMOTOCO',	'HIKAL',	'HINDALCO',	'HGS',	'HAL',	'HINDCOPPER',	'HINDPETRO',	'HINDUNILVR',	'HINDZINC',	'POWERINDIA',	'HOMEFIRST',	'HONAUT',	'HUDCO',	'HDFC',	'ICICIBANK',	'ICICIGI',	'ICICIPRULI',	'ISEC',	'IDBI',	'IDFCFIRSTB',	'IDFC',	'IFBIND',	'IIFL',	'IIFLWAM',	'IRB',	'ITC',	'ITI',	'INDIACEM',	'IBULHSGFIN',	'IBREALEST',	'INDIAMART',	'INDIANB',	'IEX',	'INDHOTEL',	'IOC',	'IOB',	'IRCTC',	'IRFC',	'INDIGOPNTS',	'INDOCO',	'IGL',	'INDUSTOWER',	'INDUSINDBK',	'INFIBEAM',	'NAUKRI',	'INFY',	'INOXLEISUR',	'INTELLECT',	'INDIGO',	'IPCALAB',	'JBCHEPHARM',	'JKCEMENT',	'JBMA',	'JKLAKSHMI',	'JKPAPER',	'JMFINANCIL',	'JSWENERGY',	'JSWSTEEL',	'JAMNAAUTO',	'JSL',	'JINDALSTEL',	'JUBLFOOD',	'JUBLINGREA',	'JUBLPHARMA',	'JUSTDIAL',	'JYOTHYLAB',	'KPRMILL',	'KEI',	'KNRCON',	'KPITTECH',	'KRBL',	'KAJARIACER',	'KALPATPOWR',	'KALYANKJIL',	'KANSAINER',	'KARURVYSYA',	'KEC',	'KOTAKBANK',	'KIMS',	'L&TFH',	'LTTS',	'LICHSGFIN',	'LTIM',	'LAXMIMACH',	'LT',	'LATENTVIEW',	'LAURUSLABS',	'LXCHEM',	'LICI',	'LINDEINDIA',	'LUPIN',	'LUXIND',	'MMTC',	'MOIL',	'MRF',	'MTARTECH',	'LODHA',	'MGL',	'M&MFIN',	'M&M',	'MAHINDCIE',	'MHRIL',	'MAHLIFE',	'MAHLOG',	'MANAPPURAM',	'MRPL',	'MARICO',	'MARUTI',	'MASTEK',	'MFSL',	'MAXHEALTH',	'MAZDOCK',	'MEDPLUS',	'METROBRAND',	'METROPOLIS',	'MSUMI',	'MOTILALOFS',	'MPHASIS',	'MCX',	'MUTHOOTFIN',	'NATCOPHARM',	'NBCC',	'NCC',	'NHPC',	'NIITLTD',	'NLCINDIA',	'NOCIL',	'NTPC',	'NH',	'NATIONALUM',	'NAVINFLUOR',	'NAZARA',	'NESTLEIND',	'NETWORK18',	'NAM-INDIA',	'NUVOCO',	'OBEROIRLTY',	'ONGC',	'OIL',	'OLECTRA',	'PAYTM',	'OFSS',	'ORIENTELEC',	'POLICYBZR',	'PCBL',	'PIIND',	'PNBHOUSING',	'PNCINFRA',	'PVR',	'PAGEIND',	'PATANJALI',	'PERSISTENT',	'PETRONET',	'PFIZER',	'PHOENIXLTD',	'PIDILITIND',	'POLYMED',	'POLYCAB',	'POLYPLEX',	'POONAWALLA',	'PFC',	'POWERGRID',	'PRAJIND',	'PRESTIGE',	'PRINCEPIPE',	'PRSMJOHNSN',	'PRIVISCL',	'PGHL',	'PGHH',	'PNB',	'QUESS',	'RBLBANK',	'RECLTD',	'RHIM',	'RITES',	'RADICO',	'RVNL',	'RAIN',	'RAJESHEXPO',	'RALLIS',	'RCF',	'RATNAMANI',	'RTNINDIA',	'RAYMOND',	'REDINGTON',	'RELAXO',	'RELIANCE',	'RBA',	'ROSSARI',	'ROUTE',	'SBICARD',	'SBILIFE',	'SIS',	'SJVN',	'SKFINDIA',	'SRF',	'MOTHERSON',	'SANOFI',	'SAPPHIRE',	'SAREGAMA',	'SCHAEFFLER',	'SHARDACROP',	'SFL',	'SHILPAMED',	'SCI',	'SHOPERSTOP',	'SHREECEM',	'RENUKA',	'SHRIRAMFIN',	'SHYAMMETL',	'SIEMENS',	'SOBHA',	'SOLARINDS',	'SONACOMS',	'SONATSOFTW',	'STARHEALTH',	'SBIN',	'SAIL',	'SWSOLAR',	'STLTECH',	'SUDARSCHEM',	'SUMICHEM',	'SPARC',	'SUNPHARMA',	'SUNTV',	'SUNDARMFIN',	'SUNDRMFAST',	'SUNTECK',	'SUPRAJIT',	'SUPREMEIND',	'SUVENPHAR',	'SUZLON',	'SWANENERGY',	'SYMPHONY',	'SYNGENE',	'TCIEXP',	'TCNSBRANDS',	'TTKPRESTIG',	'TV18BRDCST',	'TVSMOTOR',	'TANLA',	'TATACHEM',	'TATACOFFEE',	'TATACOMM',	'TCS',	'TATACONSUM',	'TATAELXSI',	'TATAINVEST',	'TATAMTRDVR',	'TATAMOTORS',	'TATAPOWER',	'TATASTEEL',	'TTML',	'TEAMLEASE',	'TECHM',	'TEJASNET',	'NIACL',	'RAMCOCEM',	'THERMAX',	'THYROCARE',	'TIMKEN',	'TITAN',	'TORNTPHARM',	'TORNTPOWER',	'TCI',	'TRENT',	'TRIDENT',	'TRIVENI',	'TRITURBINE',	'TIINDIA',	'UFLEX',	'UNOMINDA',	'UPL',	'UTIAMC',	'ULTRACEMCO',	'UNIONBANK',	'UBL',	'MCDOWELL-N',	'VGUARD',	'VMART',	'VIPIND',	'VAIBHAVGBL',	'VTL',	'VARROC',	'VBL',	'MANYAVAR',	'VEDL',	'VIJAYA',	'VINATIORGA',	'IDEA',	'VOLTAS',	'WELCORP',	'WELSPUNIND',	'WESTLIFE',	'WHIRLPOOL',	'WIPRO',	'WOCKPHARMA',	'YESBANK',	'ZFCVINDIA',	'ZEEL',	'ZENSARTECH',	'ZOMATO',	'ZYDUSLIFE',	'ZYDUSWELL',	'ECLERX']
start_date=date(2021,1,1)
end_date=date.today()
def Importdata():
    for stock in stocks:
        rawdata = get_history(symbol=stock,start=start_date,end=end_date)
        file_name = 'Nifty_All500/daily/{}.csv'.format(stock)
        file_name1 = 'Nifty_All500/weekly/{}.csv'.format(stock)
        df = pd.DataFrame(rawdata)
        df.to_csv(file_name,encoding='utf-8')
        rawdata.index = pd.to_datetime(rawdata.index)
        acc = rawdata.resample('W').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})
        wf = pd.DataFrame(acc)
        wf.to_csv(file_name1,encoding='utf-8')
        print(stock)
def buy_sell_function(data):
    buy_list = []
    sell_list = []
    flag_long = False
    flag_short = False
    for i in range(0,len(data)):
        if data['ema21'][i] < data['ema55'][i] and data['ema21'][i] > data['ema5'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif data['ema21'][i] > data['ema55'][i] and data['ema21'][i] < data['ema5'][i] and flag_short == False and flag_long == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
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
    
    return (buy_list, sell_list,flag_long,flag_short)
def emacross(data):
    #print("check")
    return data['ema5'] > data['ema21'] and data['ema21'] > data['ema55']

def Loaddata():
    for stock in stocks:
        try:
            data = pd.read_csv('Nifty_All500/daily/{}.csv'.format(stock)) 
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
            buy_sell_function(data)

            #print(buy_sell_function(data)[0])
            data['Buy'] =   buy_sell_function(data)[0]
            data['Sell'] = buy_sell_function(data)[1]
            fresh_buy = data.iloc[-1]['Buy']
            fresh_sell = data.iloc[-1]['Sell']
            print(fresh_buy)
            print(fresh_sell)
            if fresh_buy > 0:
                print("EMA cross fresh Buy : ", data.iloc[-1]['Symbol'])
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
#Importdata()
Loaddata()            
