from datetime import date,datetime,timedelta
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib
import concurrent.futures



def emacross(data):
    #print("check")
    return data['ema5'] > data['ema21'] and data['ema21'] > data['ema55']

def Loaddata():
    for stock in stock_symbols:
        try:
            data = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)) 
            data1 = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock))  
            out_file_name1 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)
            out_file_name2 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock)
            print(stock) 
            print("###################################################################################################")
            close = data.iloc[-1]['Close']
            open_price = data.iloc[-1]['Open']
            high = data.iloc[-1]['High']
            low = data.iloc[-1]['Low']
#### identificatio of streangth candle
            SC_Candle = False
            CH = high - low
            if close > open_price:
                BH = close - open_price
            else:
                BH = open_price - close
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
            data['week_number'] = data["Date_new"].dt.isocalendar().week
            # weekly_data = data.resample('W').last()

            data1['cci34_1W'] =  talib.cci(data1['High'],data1['Low'],data1['Close'],length=34)
            data1['Date_new'] = pd.to_datetime(data1['Date'])
            data1['Year'] = data1['Date_new'].dt.year
            data1['week_number'] = data1["Date_new"].dt.isocalendar().week

            ou = pd.DataFrame(data)
            ou.to_csv(out_file_name1,encoding='utf-8')
          
            ouw = pd.DataFrame(data1)
            ouw.to_csv(out_file_name2,encoding='utf-8')
                     
           
        except  KeyError as e:
            print(f"you are in exception : {e}")
        

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
        data = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock))
        data1 = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock))
        # ... (rest of your data processing code)
        out_file_name1 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426/{}.csv'.format(stock)
        out_file_name2 = 'C:/Users/muniv/Desktop/Market/Nifty_A1426_weekly/{}.csv'.format(stock)
        print(stock) 
        print("###################################################################################################")
        close = data.iloc[-1]['Close']
        open_price = data.iloc[-1]['Open']
        high = data.iloc[-1]['High']
        low = data.iloc[-1]['Low']
#### identificatio of streangth candle
        SC_Candle = False
        CH = high - low
        if close > open_price:
            BH = close - open_price
        else:
            BH = open_price - close
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
    # Replace with the desired stock symbols followed by ".NS" for NSE stocks
    #stock_symbols = ['3MINDIA.NS',	'AARTIDRUGS.NS',	'AAVAS.NS',	'ABB.NS',	'ABBOTINDIA.NS',	'ABCAPITAL.NS',	'ABFRL.NS',	'ABSLAMC.NS',	'ACC.NS',	'ADANIENT.NS',	'ADANIGREEN.NS',	'ADANIPORTS.NS',	'ADANITRANS.NS',	'AEGISCHEM.NS',	'AETHER.NS',	'AFFLE.NS',	'AIAENG.NS',	'AJANTPHARM.NS',	'ALKEM.NS',	'ALKYLAMINE.NS',	'ALLCARGO.NS',	'ALOKINDS.NS',	'AMARAJABAT.NS',	'AMBER.NS',	'AMBUJACEM.NS',	'ANGELONE.NS',	'ANURAS.NS',	'APLAPOLLO.NS',	'APLLTD.NS',	'APOLLOHOSP.NS',	'APOLLOTYRE.NS',	'APTUS.NS',	'ASAHIINDIA.NS',	'ASHOKLEY.NS',	'ASIANPAINT.NS',	'ASTERDM.NS',	'ASTRAL.NS',	'ASTRAZEN.NS',	'ATGL.NS',	'ATUL.NS',	'AUBANK.NS',	'AUROPHARMA.NS',	'AVANTIFEED.NS',	'AWL.NS',	'AXISBANK.NS',	'BAJAJ-AUTO.NS',	'BAJAJELEC.NS',	'BAJAJFINSV.NS',	'BAJAJHLDNG.NS',	'BAJFINANCE.NS',	'BALAMINES.NS',	'BALKRISIND.NS',	'BALRAMCHIN.NS',	'BANDHANBNK.NS',	'BANKBARODA.NS',	'BANKINDIA.NS',	'BASF.NS',	'BATAINDIA.NS',	'BAYERCROP.NS',	'BBTC.NS',	'BCG.NS',	'BDL.NS',	'BEL.NS',	'BERGEPAINT.NS',	'BHARATFORG.NS',	'BHARATRAS.NS',	'BHARTIARTL.NS',	'BHEL.NS',	'BIOCON.NS',	'BIRLACORPN.NS',	'BLUEDART.NS',	'BLUESTARCO.NS',	'BORORENEW.NS',	'BOSCHLTD.NS',	'BPCL.NS',	'BRIGADE.NS',	'BRITANNIA.NS',	'BSE.NS',	'BSOFT.NS',	'CAMPUS.NS',	'CAMS.NS',	'CANBK.NS',	'CANFINHOME.NS',	'CAPLIPOINT.NS',	'CARBORUNIV.NS',	'CASTROLIND.NS',	'CCL.NS',	'CDSL.NS',	'CEATLTD.NS',	'CENTRALBK.NS',	'CENTURYPLY.NS',	'CENTURYTEX.NS',	'CERA.NS',	'CESC.NS',	'CGCL.NS',	'CGPOWER.NS',	'CHALET.NS',	'CHAMBLFERT.NS',	'CHEMPLASTS.NS',	'CHOLAFIN.NS',	'CHOLAHLDNG.NS',	'CIPLA.NS',	'CLEAN.NS',	'COALINDIA.NS',	'COCHINSHIP.NS',	'COFORGE.NS',	'COLPAL.NS',	'CONCOR.NS',	'COROMANDEL.NS',	'CREDITACC.NS',	'CRISIL.NS',	'CROMPTON.NS',	'CSBBANK.NS',	'CUB.NS',	'CUMMINSIND.NS',	'CYIENT.NS',	'DABUR.NS',	'DALBHARAT.NS',	'DBL.NS',	'DCMSHRIRAM.NS',	'DEEPAKFERT.NS',	'DEEPAKNTR.NS',	'DELHIVERY.NS',	'DELTACORP.NS',	'DEVYANI.NS',	'DHANI.NS',	'DIVISLAB.NS',	'DIXON.NS',	'DLF.NS',	'DMART.NS',	'DRREDDY.NS',	'EASEMYTRIP.NS',	'ECLERX.NS',	'EDELWEISS.NS',	'EICHERMOT.NS',	'EIDPARRY.NS',	'EIHOTEL.NS',	'ELGIEQUIP.NS',	'EMAMILTD.NS',	'ENDURANCE.NS',	'ENGINERSIN.NS',	'EPL.NS',	'EQUITASBNK.NS',	'ESCORTS.NS',	'EXIDEIND.NS',	'FACT.NS',	'FDC.NS',	'FEDERALBNK.NS',	'FINCABLES.NS',	'FINEORG.NS',	'FINPIPE.NS',	'FLUOROCHEM.NS',	'FORTIS.NS',	'FSL.NS',	'GAEL.NS',	'GAIL.NS',	'GALAXYSURF.NS',	'GARFIBRES.NS',	'GESHIP.NS',	'GICRE.NS',	'GLAND.NS',	'GLAXO.NS',	'GLENMARK.NS',	'GMMPFAUDLR.NS',	'GMRINFRA.NS',	'GNFC.NS',	'GOCOLORS.NS',	'GODFRYPHLP.NS',	'GODREJAGRO.NS',	'GODREJCP.NS',	'GODREJIND.NS',	'GODREJPROP.NS',	'GPPL.NS',	'GRANULES.NS',	'GRAPHITE.NS',	'GRASIM.NS',	'GREENPANEL.NS',	'GRINDWELL.NS',	'GRINFRA.NS',	'GSFC.NS',	'GSPL.NS',	'GUJALKALI.NS',	'GUJGASLTD.NS',	'HAL.NS',	'HAPPSTMNDS.NS',	'HATSUN.NS',	'HAVELLS.NS',	'HCLTECH.NS',	'HDFCAMC.NS',	'HDFCBANK.NS',	'HDFCLIFE.NS',	'HEG.NS',	'HEROMOTOCO.NS',	'HFCL.NS',	'HGS.NS',	'HIKAL.NS',	'HINDALCO.NS',	'HINDCOPPER.NS',	'HINDPETRO.NS',	'HINDUNILVR.NS',	'HINDZINC.NS',	'HLEGLAS.NS',	'HOMEFIRST.NS',	'HONAUT.NS',	'HUDCO.NS',	'IBREALEST.NS',	'IBULHSGFIN.NS',	'ICICIBANK.NS',	'ICICIGI.NS',	'ICICIPRULI.NS',	'IDBI.NS',	'IDEA.NS',	'IDFC.NS',	'IDFCFIRSTB.NS',	'IEX.NS',	'IFBIND.NS',	'IGL.NS',	'IIFL.NS',	'INDHOTEL.NS',	'INDIACEM.NS',	'INDIAMART.NS',	'INDIANB.NS',	'INDIGO.NS',	'INDIGOPNTS.NS',	'INDOCO.NS',	'INDUSINDBK.NS',	'INDUSTOWER.NS',	'INFIBEAM.NS',	'INFY.NS',	'INOXLEISUR.NS',	'INTELLECT.NS',	'IOB.NS',	'IOC.NS',	'IPCALAB.NS',	'IRB.NS',	'IRCTC.NS',	'IRFC.NS',	'ISEC.NS',	'ITC.NS',	'ITI.NS',	'JAMNAAUTO.NS',	'JBCHEPHARM.NS',	'JBMA.NS',	'JINDALSTEL.NS',	'JKCEMENT.NS',	'JKLAKSHMI.NS',	'JKPAPER.NS',	'JMFINANCIL.NS',	'JSL.NS',	'JSWENERGY.NS',	'JSWSTEEL.NS',	'JUBLFOOD.NS',	'JUBLINGREA.NS',	'JUBLPHARMA.NS',	'JUSTDIAL.NS',	'JYOTHYLAB.NS',	'KAJARIACER.NS',	'KALYANKJIL.NS',	'KANSAINER.NS',	'KARURVYSYA.NS',	'KEC.NS',	'KEI.NS',	'KIMS.NS',	'KNRCON.NS',	'KOTAKBANK.NS',	'KPITTECH.NS',	'KPRMILL.NS',	'KRBL.NS',	'L&TFH.NS',	'LALPATHLAB.NS',	'LATENTVIEW.NS',	'LAURUSLABS.NS',	'LAXMIMACH.NS',	'LICHSGFIN.NS',	'LICI.NS',	'LINDEINDIA.NS',	'LODHA.NS',	'LT.NS',	'LTIM.NS',	'LTTS.NS',	'LUPIN.NS',	'LUXIND.NS',	'LXCHEM.NS',	'M&M.NS',	'M&MFIN.NS',	'MAHABANK.NS',	'MAHINDCIE.NS',	'MAHLIFE.NS',	'MAHLOG.NS',	'MANAPPURAM.NS',	'MANYAVAR.NS',	'MAPMYINDIA.NS',	'MARICO.NS',	'MARUTI.NS',	'MASTEK.NS',	'MAXHEALTH.NS',	'MAZDOCK.NS',	'MCDOWELL-N.NS',	'MCX.NS',	'MEDPLUS.NS',	'METROBRAND.NS',	'METROPOLIS.NS',	'MFSL.NS',	'MGL.NS',	'MHRIL.NS',	'MMTC.NS',	'MOIL.NS',	'MOTHERSON.NS',	'MOTILALOFS.NS',	'MPHASIS.NS',	'MRF.NS',	'MRPL.NS',	'MSUMI.NS',	'MTARTECH.NS',	'MUTHOOTFIN.NS',	'NAM-INDIA.NS',	'NATCOPHARM.NS',	'NATIONALUM.NS',	'NAUKRI.NS',	'NAVINFLUOR.NS',	'NAZARA.NS',	'NBCC.NS',	'NCC.NS',	'NESTLEIND.NS',	'NETWORK18.NS',	'NH.NS',	'NHPC.NS',	'NIACL.NS',	'NIITLTD.NS',	'NLCINDIA.NS',	'NOCIL.NS',	'NTPC.NS',	'NUVOCO.NS',	'NYKAA.NS',	'OBEROIRLTY.NS',	'OFSS.NS',	'OIL.NS',	'OLECTRA.NS',	'ONGC.NS',	'ORIENTELEC.NS',	'PAGEIND.NS',	'PATANJALI.NS',	'PAYTM.NS',	'PCBL.NS',	'PERSISTENT.NS',	'PETRONET.NS',	'PFC.NS',	'PFIZER.NS',	'PGHH.NS',	'PGHL.NS',	'PHOENIXLTD.NS',	'PIDILITIND.NS',	'PIIND.NS',	'PNB.NS',	'PNBHOUSING.NS',	'PNCINFRA.NS',	'POLICYBZR.NS',	'POLYCAB.NS',	'POLYMED.NS',	'POLYPLEX.NS',	'POONAWALLA.NS',	'POWERGRID.NS',	'POWERINDIA.NS',	'PRAJIND.NS',	'PRESTIGE.NS',	'PRINCEPIPE.NS',	'PRIVISCL.NS',	'PRSMJOHNSN.NS',	'QUESS.NS',	'RADICO.NS',	'RAIN.NS',	'RAJESHEXPO.NS',	'RALLIS.NS',	'RAMCOCEM.NS',	'RATNAMANI.NS',	'RAYMOND.NS',	'RBA.NS',	'RBLBANK.NS',	'RCF.NS',	'RECLTD.NS',	'REDINGTON.NS',	'RELAXO.NS',	'RELIANCE.NS',	'RENUKA.NS',	'RHIM.NS',	'RITES.NS',	'ROSSARI.NS',	'ROUTE.NS',	'RTNINDIA.NS',	'RVNL.NS',	'SAIL.NS',	'SANOFI.NS',	'SAPPHIRE.NS',	'SAREGAMA.NS',	'SBILIFE.NS',	'SBIN.NS',	'SCHAEFFLER.NS',	'SCI.NS',	'SFL.NS',	'SHARDACROP.NS',	'SHILPAMED.NS',	'SHOPERSTOP.NS',	'SHREECEM.NS',	'SHRIRAMFIN.NS',	'SHYAMMETL.NS',	'SIEMENS.NS',	'SIS.NS',	'SJVN.NS',	'SKFINDIA.NS',	'SOBHA.NS',	'SOLARINDS.NS',	'SONACOMS.NS',	'SONATSOFTW.NS',	'SPARC.NS',	'SRF.NS',	'STARHEALTH.NS',	'STLTECH.NS',	'SUDARSCHEM.NS',	'SUMICHEM.NS',	'SUNDARMFIN.NS',	'SUNDRMFAST.NS',	'SUNPHARMA.NS',	'SUNTECK.NS',	'SUNTV.NS',	'SUPRAJIT.NS',	'SUPREMEIND.NS',	'SUVENPHAR.NS',	'SUZLON.NS',	'SWANENERGY.NS',	'SWSOLAR.NS',	'SYMPHONY.NS',	'SYNGENE.NS',	'TANLA.NS',	'TATACHEM.NS',	'TATACOFFEE.NS',	'TATACOMM.NS',	'TATACONSUM.NS',	'TATAELXSI.NS',	'TATAINVEST.NS',	'TATAMOTORS.NS',	'TATAMTRDVR.NS',	'TATAPOWER.NS',	'TATASTEEL.NS',	'TCI.NS',	'TCIEXP.NS',	'TCNSBRANDS.NS',	'TCS.NS',	'TEAMLEASE.NS',	'TECHM.NS',	'TEJASNET.NS',	'THERMAX.NS',	'THYROCARE.NS',	'TIINDIA.NS',	'TIMKEN.NS',	'TITAN.NS',	'TORNTPHARM.NS',	'TORNTPOWER.NS',	'TRENT.NS',	'TRIDENT.NS',	'TRITURBINE.NS',	'TRIVENI.NS',	'TTKPRESTIG.NS',	'TTML.NS',	'TV18BRDCST.NS',	'TVSMOTOR.NS',	'UBL.NS',	'UFLEX.NS',	'ULTRACEMCO.NS',	'UNIONBANK.NS',	'UNOMINDA.NS',	'UPL.NS',	'UTIAMC.NS',	'VAIBHAVGBL.NS',	'VARROC.NS',	'VBL.NS',	'VEDL.NS',	'VGUARD.NS',	'VIJAYA.NS',	'VINATIORGA.NS',	'VIPIND.NS',	'VMART.NS',	'VOLTAS.NS',	'VTL.NS',	'WELCORP.NS',	'WELSPUNIND.NS',	'WESTLIFE.NS',	'WHIRLPOOL.NS',	'WIPRO.NS',	'WOCKPHARMA.NS',	'YESBANK.NS',	'ZEEL.NS',	'ZENSARTECH.NS',	'ZFCVINDIA.NS',	'ZOMATO.NS',	'ZYDUSLIFE.NS',	'ZYDUSWELL.NS']
    #stock_symbols = ['3MINDIA.NS',	'ABB.NS',	'ACC.NS',	'AIAENG.NS']

    csv_file_path = r'C:\Users\muniv\Desktop\Market\marketdata_analysis\stock_symbols.csv'
    stock_symbols = import_stock_symbols_from_csv(csv_file_path)
    start_date = "2023-01-01"  # Replace with the desired start date
  
    end_date = date.today()
    print("EMA CCI ploting script starting")
    #Importdata()   
    processed_data = process_stocks(stock_symbols)
    # Loaddata()