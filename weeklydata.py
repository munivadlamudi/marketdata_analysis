from nsepy import get_history
from datetime import date,datetime
import pandas as pd
import numpy as np
import pandas_ta as talib
#import talib
import matplotlib.pyplot as plt
stocks=['3MINDIA',	'ABB',	'ACC',	'AIAENG',	'APLAPOLLO',	'AUBANK',	'AARTIDRUGS',	'AAVAS',	'ABBOTINDIA',	'ADANIENT',	'ADANIGREEN',	'ADANIPORTS',	'ATGL',	'ADANITRANS',	'AWL',	'ABCAPITAL',	'ABFRL',	'ABSLAMC',	'AEGISCHEM',	'AETHER',	'AFFLE',	'AJANTPHARM',	'APLLTD',	'ALKEM',	'ALKYLAMINE',	'ALLCARGO',	'ALOKINDS',	'AMARAJABAT',	'AMBER',	'AMBUJACEM',	'ANGELONE',	'ANURAS',	'APOLLOHOSP',	'APOLLOTYRE',	'APTUS',	'ASAHIINDIA',	'ASHOKLEY',	'ASIANPAINT',	'ASTERDM',	'ASTRAZEN',	'ASTRAL',	'ATUL',	'AUROPHARMA',	'AVANTIFEED',	'DMART',	'AXISBANK',	'BASF',	'BSE',	'BAJAJ-AUTO',	'BAJAJELEC',	'BAJFINANCE',	'BAJAJFINSV',	'BAJAJHLDNG',	'BALAMINES',	'BALKRISIND',	'BALRAMCHIN',	'BANDHANBNK',	'BANKBARODA',	'BANKINDIA',	'MAHABANK',	'BATAINDIA',	'BAYERCROP',	'BERGEPAINT',	'BDL',	'BEL',	'BHARATFORG',	'BHEL',	'BPCL',	'BHARATRAS',	'BHARTIARTL',	'BIOCON',	'BIRLACORPN',	'BSOFT',	'BLUEDART',	'BLUESTARCO',	'BBTC',	'BORORENEW',	'BOSCHLTD',	'BRIGADE',	'BCG',	'BRITANNIA',	'MAPMYINDIA',	'CCL',	'CESC',	'CGPOWER',	'CRISIL',	'CSBBANK',	'CAMPUS',	'CANFINHOME',	'CANBK',	'CAPLIPOINT',	'CGCL',	'CARBORUNIV',	'CASTROLIND',	'CEATLTD',	'CENTRALBK',	'CDSL',	'CENTURYPLY',	'CENTURYTEX',	'CERA',	'CHALET',	'CHAMBLFERT',	'CHEMPLASTS',	'CHOLAHLDNG',	'CHOLAFIN',	'CIPLA',	'CUB',	'CLEAN',	'COALINDIA',	'COCHINSHIP',	'COFORGE',	'COLPAL',	'CAMS',	'CONCOR',	'COROMANDEL',	'CREDITACC',	'CROMPTON',	'CUMMINSIND',	'CYIENT',	'DCMSHRIRAM',	'DLF',	'DABUR',	'DALBHARAT',	'DEEPAKFERT',	'DEEPAKNTR',	'DELHIVERY',	'DELTACORP',	'DEVYANI',	'DHANI',	'DBL',	'DIVISLAB',	'DIXON',	'LALPATHLAB',	'DRREDDY',	'EIDPARRY',	'EIHOTEL',	'EPL',	'EASEMYTRIP',	'EDELWEISS',	'EICHERMOT',	'ELGIEQUIP',	'EMAMILTD',	'ENDURANCE',	'ENGINERSIN',	'EQUITASBNK',	'ESCORTS',	'EXIDEIND',	'FDC',	'NYKAA',	'FEDERALBNK',	'FACT',	'FINEORG',	'FINCABLES',	'FINPIPE',	'FSL',	'FORTIS',	'GRINFRA',	'GAIL',	'GMMPFAUDLR',	'GMRINFRA',	'GALAXYSURF',	'GARFIBRES',	'GICRE',	'GLAND',	'GLAXO',	'GLENMARK',	'GOCOLORS',	'GODFRYPHLP',	'GODREJAGRO',	'GODREJCP',	'GODREJIND',	'GODREJPROP',	'GRANULES',	'GRAPHITE',	'GRASIM',	'GESHIP',	'GREENPANEL',	'GRINDWELL',	'GUJALKALI',	'GAEL',	'FLUOROCHEM',	'GUJGASLTD',	'GNFC',	'GPPL',	'GSFC',	'GSPL',	'HEG',	'HCLTECH',	'HDFCAMC',	'HDFCBANK',	'HDFCLIFE',	'HFCL',	'HLEGLAS',	'HAPPSTMNDS',	'HATSUN',	'HAVELLS',	'HEROMOTOCO',	'HIKAL',	'HINDALCO',	'HGS',	'HAL',	'HINDCOPPER',	'HINDPETRO',	'HINDUNILVR',	'HINDZINC',	'POWERINDIA',	'HOMEFIRST',	'HONAUT',	'HUDCO',	'HDFC',	'ICICIBANK',	'ICICIGI',	'ICICIPRULI',	'ISEC',	'IDBI',	'IDFCFIRSTB',	'IDFC',	'IFBIND',	'IIFL',	'IIFLWAM',	'IRB',	'ITC',	'ITI',	'INDIACEM',	'IBULHSGFIN',	'IBREALEST',	'INDIAMART',	'INDIANB',	'IEX',	'INDHOTEL',	'IOC',	'IOB',	'IRCTC',	'IRFC',	'INDIGOPNTS',	'INDOCO',	'IGL',	'INDUSTOWER',	'INDUSINDBK',	'INFIBEAM',	'NAUKRI',	'INFY',	'INOXLEISUR',	'INTELLECT',	'INDIGO',	'IPCALAB',	'JBCHEPHARM',	'JKCEMENT',	'JBMA',	'JKLAKSHMI',	'JKPAPER',	'JMFINANCIL',	'JSWENERGY',	'JSWSTEEL',	'JAMNAAUTO',	'JSL',	'JINDALSTEL',	'JUBLFOOD',	'JUBLINGREA',	'JUBLPHARMA',	'JUSTDIAL',	'JYOTHYLAB',	'KPRMILL',	'KEI',	'KNRCON',	'KPITTECH',	'KRBL',	'KAJARIACER',	'KALPATPOWR',	'KALYANKJIL',	'KANSAINER',	'KARURVYSYA',	'KEC',	'KOTAKBANK',	'KIMS',	'L&TFH',	'LTTS',	'LICHSGFIN',	'LTIM',	'LAXMIMACH',	'LT',	'LATENTVIEW',	'LAURUSLABS',	'LXCHEM',	'LICI',	'LINDEINDIA',	'LUPIN',	'LUXIND',	'MMTC',	'MOIL',	'MRF',	'MTARTECH',	'LODHA',	'MGL',	'M&MFIN',	'M&M',	'MAHINDCIE',	'MHRIL',	'MAHLIFE',	'MAHLOG',	'MANAPPURAM',	'MRPL',	'MARICO',	'MARUTI',	'MASTEK',	'MFSL',	'MAXHEALTH',	'MAZDOCK',	'MEDPLUS',	'METROBRAND',	'METROPOLIS',	'MSUMI',	'MOTILALOFS',	'MPHASIS',	'MCX',	'MUTHOOTFIN',	'NATCOPHARM',	'NBCC',	'NCC',	'NHPC',	'NIITLTD',	'NLCINDIA',	'NOCIL',	'NTPC',	'NH',	'NATIONALUM',	'NAVINFLUOR',	'NAZARA',	'NESTLEIND',	'NETWORK18',	'NAM-INDIA',	'NUVOCO',	'OBEROIRLTY',	'ONGC',	'OIL',	'OLECTRA',	'PAYTM',	'OFSS',	'ORIENTELEC',	'POLICYBZR',	'PCBL',	'PIIND',	'PNBHOUSING',	'PNCINFRA',	'PVR',	'PAGEIND',	'PATANJALI',	'PERSISTENT',	'PETRONET',	'PFIZER',	'PHOENIXLTD',	'PIDILITIND',	'POLYMED',	'POLYCAB',	'POLYPLEX',	'POONAWALLA',	'PFC',	'POWERGRID',	'PRAJIND',	'PRESTIGE',	'PRINCEPIPE',	'PRSMJOHNSN',	'PRIVISCL',	'PGHL',	'PGHH',	'PNB',	'QUESS',	'RBLBANK',	'RECLTD',	'RHIM',	'RITES',	'RADICO',	'RVNL',	'RAIN',	'RAJESHEXPO',	'RALLIS',	'RCF',	'RATNAMANI',	'RTNINDIA',	'RAYMOND',	'REDINGTON',	'RELAXO',	'RELIANCE',	'RBA',	'ROSSARI',	'ROUTE',	'SBICARD',	'SBILIFE',	'SIS',	'SJVN',	'SKFINDIA',	'SRF',	'MOTHERSON',	'SANOFI',	'SAPPHIRE',	'SAREGAMA',	'SCHAEFFLER',	'SHARDACROP',	'SFL',	'SHILPAMED',	'SCI',	'SHOPERSTOP',	'SHREECEM',	'RENUKA',	'SHRIRAMFIN',	'SHYAMMETL',	'SIEMENS',	'SOBHA',	'SOLARINDS',	'SONACOMS',	'SONATSOFTW',	'STARHEALTH',	'SBIN',	'SAIL',	'SWSOLAR',	'STLTECH',	'SUDARSCHEM',	'SUMICHEM',	'SPARC',	'SUNPHARMA',	'SUNTV',	'SUNDARMFIN',	'SUNDRMFAST',	'SUNTECK',	'SUPRAJIT',	'SUPREMEIND',	'SUVENPHAR',	'SUZLON',	'SWANENERGY',	'SYMPHONY',	'SYNGENE',	'TCIEXP',	'TCNSBRANDS',	'TTKPRESTIG',	'TV18BRDCST',	'TVSMOTOR',	'TANLA',	'TATACHEM',	'TATACOFFEE',	'TATACOMM',	'TCS',	'TATACONSUM',	'TATAELXSI',	'TATAINVEST',	'TATAMTRDVR',	'TATAMOTORS',	'TATAPOWER',	'TATASTEEL',	'TTML',	'TEAMLEASE',	'TECHM',	'TEJASNET',	'NIACL',	'RAMCOCEM',	'THERMAX',	'THYROCARE',	'TIMKEN',	'TITAN',	'TORNTPHARM',	'TORNTPOWER',	'TCI',	'TRENT',	'TRIDENT',	'TRIVENI',	'TRITURBINE',	'TIINDIA',	'UFLEX',	'UNOMINDA',	'UPL',	'UTIAMC',	'ULTRACEMCO',	'UNIONBANK',	'UBL',	'MCDOWELL-N',	'VGUARD',	'VMART',	'VIPIND',	'VAIBHAVGBL',	'VTL',	'VARROC',	'VBL',	'MANYAVAR',	'VEDL',	'VIJAYA',	'VINATIORGA',	'IDEA',	'VOLTAS',	'WELCORP',	'WELSPUNIND',	'WESTLIFE',	'WHIRLPOOL',	'WIPRO',	'WOCKPHARMA',	'YESBANK',	'ZFCVINDIA',	'ZEEL',	'ZENSARTECH',	'ZOMATO',	'ZYDUSLIFE',	'ZYDUSWELL',	'ECLERX']
#stocks=[ 'ACC' ]
start_date=date(2021,1,1)
end_date=date.today()
def Importdata():
    for stock in stocks:
        rawdata = get_history(symbol=stock,start=start_date,end=end_date)
        file_name = 'data/Daily/{}.csv'.format(stock)
        file_name1 = 'data/weekly/{}.csv'.format(stock)
        df = pd.DataFrame(rawdata)
        df.to_csv(file_name,encoding='utf-8')
        rawdata.index = pd.to_datetime(rawdata.index)
        acc = rawdata.resample('W').agg({'High': 'max', 'Low': 'min', 'Close': 'last'})
        wf = pd.DataFrame(acc)
        wf.to_csv(file_name1,encoding='utf-8')
        #print(acc)
        print(stock)

def buy_sell_function(data):
    buy_list = []
    sell_list = []
    flag_long = False
    flag_short = False
    for i in range(0,len(data)):
        if data['ema21'][i] < data['ema55'][i] and data['ema21'][i] > data['ema5'][i] and flag_long == False and flag_short == False:
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            flag_short = True
        elif data['ema21'][i] > data['ema55'][i] and data['ema21'][i] < data['ema5'][i] and flag_short == False and flag_long == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_short == True and data['ema5'][i] > data['ema21'][i]:
            sell_list.append(np.nan)
            buy_list.append(data['Close'][i])
            flag_short = False
        elif flag_long == True and data['ema5'][i] < data['ema21'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
    
    return (buy_list, sell_list)

def week_number_fun(data):
    # buy_list = []
    # sell_list = []
        week_number = []
    # flag_long = False
    # flag_short = False
        for i in range(0,len(data)):
            week_number.append(data['Date'][i].dt.isocalendar().week)
        
        return (week_number)
def Loaddata():
    for stock in stocks:
        try:
            data = pd.read_csv('data/Daily/{}.csv'.format(stock))
            data1 = pd.read_csv('data/weekly/{}.csv'.format(stock))  
            out_file_name1 = 'data/output/{}.csv'.format(stock)
            out_file_name2 = 'data/output_weekly/{}.csv'.format(stock)
            #print(stock) 
            #print("###################################################################################################")
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
            data['Date_new'] = pd.to_datetime(data['Date'])
            data['Year'] = data['Date_new'].dt.year
            data["week_number"] = data["Date_new"].dt.isocalendar().week
            
                      
            data1['cci34_1W'] =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=34)
            data1['Date_new'] = pd.to_datetime(data1['Date'])
            data1['Year'] = data1['Date_new'].dt.year
            data1["week_number"] = data1["Date_new"].dt.isocalendar().week

            
            result = data1.dtypes
            print(result)
            #writting new file for daily data in /data/output
            ou = pd.DataFrame(data)
            ou.to_csv(out_file_name1,encoding='utf-8')
           #writting new file for weekly data in /data/output_weekly
            ouw = pd.DataFrame(data1)
            ouw.to_csv(out_file_name2,encoding='utf-8')

            buy_sell_function(data)
            data['Buy'] =  buy_sell_function(data)[0]
            data['Sell'] = buy_sell_function(data)[1]
           
            

            #cci34 =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=34)
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ : ", data.iloc[-1])
            
            # if (data1.iloc[-1]['cci34_1W'] >= 100 and data.iloc[-1]['cci34_1D'] >= 100) or (data1.iloc[-1]['cci34_1W'] >= -70 and data.iloc[-1]['cci34_1D'] >= 100):
            #     print("##############################################################################")
            #     print(stock)
            #     print(data.iloc[-1]['Date'])
            #     print(data.iloc[-1]['Close'])
            #     print(data.iloc[-1]['cci8'])
            #     print(data.iloc[-1]['cci34_1D'])
            #     print("!!!!!!!!!!!!!!!!!!!! : ",data1.iloc[-1]['cci34_1W'])
            #     print(" you can buy this stock  : ", stock)
            #     try:
            #         # buydata = 'buydata.csv'
            #         # bd = pd.DataFrame(stock)
            #         # bd.to_csv(buydata,encoding='utf-8')
            #         with open('buydata.txt', 'w') as b:
            #             b.write("22222 \n")

            #             #buyfile.write(stock)
            #     except Exception as be:
            #         print("Buy exception ", be)
            # if (data1.iloc[-1]['cci34_1W'] <= -100 and data.iloc[-1]['cci34_1D'] <= -100) or (data1.iloc[-1]['cci34_1W'] < 70 and data.iloc[-1]['cci34_1D'] <= -100):
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            #     print(stock)
            #     print(data.iloc[-1]['Close'])
            #     print(data.iloc[-1]['cci8'])
            #     print(data.iloc[-1]['cci34_1D'])
            #     print("!!!!!!!!!!!!!!!!!!!! : ",data1.iloc[-1]['cci34_1W'])
            #     print(" you can sell this stock  : ", stock)
            #     try:
            #         with open('selldata.txt', 'w') as s:
            #             s.write(" 3333333 \n")
            #             #sellfile.write(stock)
            #     except Exception as se:
            #         print("sell exception ", se)
        except Exception as e:
            print("you are in exception", e)
            pass
         
# Importdata()
Loaddata()