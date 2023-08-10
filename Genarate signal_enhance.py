from datetime import date,datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib
import subprocess

def Loaddata():
    buy_data = []
    sell_data = []
    Buy_result_data='C:/Users/muniv/Desktop/Market/marketdata_analysis/Buy_Entry.csv'
    Sell_result_data='C:/Users/muniv/Desktop/Market/marketdata_analysis/Sell_Entry.csv'
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
    
    for stock in stock_symbols:
        try:
            buy_entry = []
            exit_buy = []
            sell_entry = []
            exit_sell = []
            buy_list = []
            sell_list = []
            data = pd.read_csv('C:/Users/muniv/Desktop/Market/Compare/{}.csv'.format(stock)) 
            out_file_name1 = 'C:/Users/muniv/Desktop/Market/Signals/{}.csv'.format(stock)         
            buy_sell_function(data, buy_list, sell_list, buy_entry, sell_entry, exit_buy, exit_sell)
            #report_performance(data)
            print("Name of the stock : ",stock)
            #print(buy_sell_function(data)[0])
            
            data['Buy'] =   buy_list
            data['Sell'] = sell_list
            data['Buy_Entry'] = buy_entry
            data['exit_buy'] = exit_buy
            data['sell_Entry'] = sell_entry
            data['exit_sell'] = exit_sell
            
            fresh_buy = data.iloc[-1]['Buy_Entry']
            fresh_sell = data.iloc[-1]['sell_Entry']
            fresh_buy_1 = data.iloc[-2]['Buy_Entry']
            fresh_sell_1 = data.iloc[-2]['sell_Entry']
            print("fresh_buy : ",fresh_buy)
            print("fresh_sell : ",fresh_sell)

            ou = pd.DataFrame(data)
            ou.to_csv(out_file_name1,encoding='utf-8')

            # if not pd.isna(fresh_buy) and pd.isna(fresh_buy_1):
            if not pd.isna(fresh_buy):
                print("Write into Buy file") 
                # Append data to buy_data list
                buy_data.append({
                    'stock': stock,
                    'Comment': fresh_buy,
                    'Date ': data['Date_new'].iloc[-1],
                    'Closing Price': data['Close'].iloc[-1]
                })

            # if not pd.isna(fresh_sell) and pd.isna(fresh_sell_1):
            if not pd.isna(fresh_sell):
                print("check signals for sell #####")
                print("Write into Sell file")
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
           
        except  KeyError as e:
            print(f"you are in exception : {e}")
        

def buy_sell_function(data, buy_list, sell_list, buy_entry, sell_entry, exit_buy, exit_sell):
    
    
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
        EMAALrangeS = (((EMAALS >= 0.381 and EMAALS <= 2.22) and (data['cci8'][i] >= 100 and data['cci34_1D'][i] <= -100)) or (data['cci34_1W'][i] <= -100 and data['cci34_1D'][i] <= -100))
        EMAALrangeS = 1 if EMAALrangeS else 0
        EMAALrangeS1 = (data['cci34_1W'][i] < 70 and data['cci34_1D'][i] <= -100)
        EMAALrangeS1 = 1 if EMAALrangeS1 else 0

        if SC_Candle_B and (EMAALrangeB or EMAALrangeB1) and flag_short == False and flag_long == False :
        
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
            fresh_long = True
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
            buy_entry.append(np.nan)
            exit_buy.append(np.nan)
            exit_sell.append(np.nan)
        elif flag_short == True and ((data['ema5'][i] > data['ema21'][i]) or data['cci34_1D'][i] >= 0 ):
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False
            exit_sell.append("Exit sell")
            exit_buy.append(np.nan)
            buy_entry.append(np.nan)
            sell_entry.append(np.nan)
        elif flag_long == True and ((data['ema5'][i] < data['ema21'][i]) or data['cci34_1D'][i] <= 0 ):
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
            exit_buy.append("Exit buy")
            exit_sell.append(np.nan)
            buy_entry.append(np.nan)
            sell_entry.append(np.nan)
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
            buy_entry.append(np.nan)
            sell_entry.append(np.nan)
            exit_buy.append(np.nan)
            exit_sell.append(np.nan)
    return (data, buy_list, sell_list, buy_entry, sell_entry, exit_buy, exit_sell)



if __name__ == "__main__":
    # Replace with the desired stock symbols followed by ".NS" for NSE stocks

    stock_symbols = ['3MINDIA.NS',	'AARTIDRUGS.NS',	'AAVAS.NS',	'ABB.NS',	'ABBOTINDIA.NS',	'ABCAPITAL.NS',	'ABFRL.NS',	'ABSLAMC.NS',	'ACC.NS',	'ADANIENT.NS',	'ADANIGREEN.NS',	'ADANIPORTS.NS',	'ADANITRANS.NS',	'AEGISCHEM.NS',	'AETHER.NS',	'AFFLE.NS',	'AIAENG.NS',	'AJANTPHARM.NS',	'ALKEM.NS',	'ALKYLAMINE.NS',	'ALLCARGO.NS',	'ALOKINDS.NS',	'AMARAJABAT.NS',	'AMBER.NS',	'AMBUJACEM.NS',	'ANGELONE.NS',	'ANURAS.NS',	'APLAPOLLO.NS',	'APLLTD.NS',	'APOLLOHOSP.NS',	'APOLLOTYRE.NS',	'APTUS.NS',	'ASAHIINDIA.NS',	'ASHOKLEY.NS',	'ASIANPAINT.NS',	'ASTERDM.NS',	'ASTRAL.NS',	'ASTRAZEN.NS',	'ATGL.NS',	'ATUL.NS',	'AUBANK.NS',	'AUROPHARMA.NS',	'AVANTIFEED.NS',	'AWL.NS',	'AXISBANK.NS',	'BAJAJ-AUTO.NS',	'BAJAJELEC.NS',	'BAJAJFINSV.NS',	'BAJAJHLDNG.NS',	'BAJFINANCE.NS',	'BALAMINES.NS',	'BALKRISIND.NS',	'BALRAMCHIN.NS',	'BANDHANBNK.NS',	'BANKBARODA.NS',	'BANKINDIA.NS',	'BASF.NS',	'BATAINDIA.NS',	'BAYERCROP.NS',	'BBTC.NS',	'BCG.NS',	'BDL.NS',	'BEL.NS',	'BERGEPAINT.NS',	'BHARATFORG.NS',	'BHARATRAS.NS',	'BHARTIARTL.NS',	'BHEL.NS',	'BIOCON.NS',	'BIRLACORPN.NS',	'BLUEDART.NS',	'BLUESTARCO.NS',	'BORORENEW.NS',	'BOSCHLTD.NS',	'BPCL.NS',	'BRIGADE.NS',	'BRITANNIA.NS',	'BSE.NS',	'BSOFT.NS',	'CAMPUS.NS',	'CAMS.NS',	'CANBK.NS',	'CANFINHOME.NS',	'CAPLIPOINT.NS',	'CARBORUNIV.NS',	'CASTROLIND.NS',	'CCL.NS',	'CDSL.NS',	'CEATLTD.NS',	'CENTRALBK.NS',	'CENTURYPLY.NS',	'CENTURYTEX.NS',	'CERA.NS',	'CESC.NS',	'CGCL.NS',	'CGPOWER.NS',	'CHALET.NS',	'CHAMBLFERT.NS',	'CHEMPLASTS.NS',	'CHOLAFIN.NS',	'CHOLAHLDNG.NS',	'CIPLA.NS',	'CLEAN.NS',	'COALINDIA.NS',	'COCHINSHIP.NS',	'COFORGE.NS',	'COLPAL.NS',	'CONCOR.NS',	'COROMANDEL.NS',	'CREDITACC.NS',	'CRISIL.NS',	'CROMPTON.NS',	'CSBBANK.NS',	'CUB.NS',	'CUMMINSIND.NS',	'CYIENT.NS',	'DABUR.NS',	'DALBHARAT.NS',	'DBL.NS',	'DCMSHRIRAM.NS',	'DEEPAKFERT.NS',	'DEEPAKNTR.NS',	'DELHIVERY.NS',	'DELTACORP.NS',	'DEVYANI.NS',	'DHANI.NS',	'DIVISLAB.NS',	'DIXON.NS',	'DLF.NS',	'DMART.NS',	'DRREDDY.NS',	'EASEMYTRIP.NS',	'ECLERX.NS',	'EDELWEISS.NS',	'EICHERMOT.NS',	'EIDPARRY.NS',	'EIHOTEL.NS',	'ELGIEQUIP.NS',	'EMAMILTD.NS',	'ENDURANCE.NS',	'ENGINERSIN.NS',	'EPL.NS',	'EQUITASBNK.NS',	'ESCORTS.NS',	'EXIDEIND.NS',	'FACT.NS',	'FDC.NS',	'FEDERALBNK.NS',	'FINCABLES.NS',	'FINEORG.NS',	'FINPIPE.NS',	'FLUOROCHEM.NS',	'FORTIS.NS',	'FSL.NS',	'GAEL.NS',	'GAIL.NS',	'GALAXYSURF.NS',	'GARFIBRES.NS',	'GESHIP.NS',	'GICRE.NS',	'GLAND.NS',	'GLAXO.NS',	'GLENMARK.NS',	'GMMPFAUDLR.NS',	'GMRINFRA.NS',	'GNFC.NS',	'GOCOLORS.NS',	'GODFRYPHLP.NS',	'GODREJAGRO.NS',	'GODREJCP.NS',	'GODREJIND.NS',	'GODREJPROP.NS',	'GPPL.NS',	'GRANULES.NS',	'GRAPHITE.NS',	'GRASIM.NS',	'GREENPANEL.NS',	'GRINDWELL.NS',	'GRINFRA.NS',	'GSFC.NS',	'GSPL.NS',	'GUJALKALI.NS',	'GUJGASLTD.NS',	'HAL.NS',	'HAPPSTMNDS.NS',	'HATSUN.NS',	'HAVELLS.NS',	'HCLTECH.NS',	'HDFCAMC.NS',	'HDFCBANK.NS',	'HDFCLIFE.NS',	'HEG.NS',	'HEROMOTOCO.NS',	'HFCL.NS',	'HGS.NS',	'HIKAL.NS',	'HINDALCO.NS',	'HINDCOPPER.NS',	'HINDPETRO.NS',	'HINDUNILVR.NS',	'HINDZINC.NS',	'HLEGLAS.NS',	'HOMEFIRST.NS',	'HONAUT.NS',	'HUDCO.NS',	'IBREALEST.NS',	'IBULHSGFIN.NS',	'ICICIBANK.NS',	'ICICIGI.NS',	'ICICIPRULI.NS',	'IDBI.NS',	'IDEA.NS',	'IDFC.NS',	'IDFCFIRSTB.NS',	'IEX.NS',	'IFBIND.NS',	'IGL.NS',	'IIFL.NS',	'INDHOTEL.NS',	'INDIACEM.NS',	'INDIAMART.NS',	'INDIANB.NS',	'INDIGO.NS',	'INDIGOPNTS.NS',	'INDOCO.NS',	'INDUSINDBK.NS',	'INDUSTOWER.NS',	'INFIBEAM.NS',	'INFY.NS',	'INOXLEISUR.NS',	'INTELLECT.NS',	'IOB.NS',	'IOC.NS',	'IPCALAB.NS',	'IRB.NS',	'IRCTC.NS',	'IRFC.NS',	'ISEC.NS',	'ITC.NS',	'ITI.NS',	'JAMNAAUTO.NS',	'JBCHEPHARM.NS',	'JBMA.NS',	'JINDALSTEL.NS',	'JKCEMENT.NS',	'JKLAKSHMI.NS',	'JKPAPER.NS',	'JMFINANCIL.NS',	'JSL.NS',	'JSWENERGY.NS',	'JSWSTEEL.NS',	'JUBLFOOD.NS',	'JUBLINGREA.NS',	'JUBLPHARMA.NS',	'JUSTDIAL.NS',	'JYOTHYLAB.NS',	'KAJARIACER.NS', 'KALYANKJIL.NS',	'KANSAINER.NS',	'KARURVYSYA.NS',	'KEC.NS',	'KEI.NS',	'KIMS.NS',	'KNRCON.NS',	'KOTAKBANK.NS',	'KPITTECH.NS',	'KPRMILL.NS',	'KRBL.NS',	'L&TFH.NS',	'LALPATHLAB.NS',	'LATENTVIEW.NS',	'LAURUSLABS.NS',	'LAXMIMACH.NS',	'LICHSGFIN.NS',	'LICI.NS',	'LINDEINDIA.NS',	'LODHA.NS',	'LT.NS',	'LTIM.NS',	'LTTS.NS',	'LUPIN.NS',	'LUXIND.NS',	'LXCHEM.NS',	'M&M.NS',	'M&MFIN.NS',	'MAHABANK.NS',	'MAHINDCIE.NS',	'MAHLIFE.NS',	'MAHLOG.NS',	'MANAPPURAM.NS',	'MANYAVAR.NS',	'MAPMYINDIA.NS',	'MARICO.NS',	'MARUTI.NS',	'MASTEK.NS',	'MAXHEALTH.NS',	'MAZDOCK.NS',	'MCDOWELL-N.NS',	'MCX.NS',	'MEDPLUS.NS',	'METROBRAND.NS',	'METROPOLIS.NS',	'MFSL.NS',	'MGL.NS',	'MHRIL.NS',	'MMTC.NS',	'MOIL.NS',	'MOTHERSON.NS',	'MOTILALOFS.NS',	'MPHASIS.NS',	'MRF.NS',	'MRPL.NS',	'MSUMI.NS',	'MTARTECH.NS',	'MUTHOOTFIN.NS',	'NAM-INDIA.NS',	'NATCOPHARM.NS',	'NATIONALUM.NS',	'NAUKRI.NS',	'NAVINFLUOR.NS',	'NAZARA.NS',	'NBCC.NS',	'NCC.NS',	'NESTLEIND.NS',	'NETWORK18.NS',	'NH.NS',	'NHPC.NS',	'NIACL.NS',	'NIITLTD.NS',	'NLCINDIA.NS',	'NOCIL.NS',	'NTPC.NS',	'NUVOCO.NS',	'NYKAA.NS',	'OBEROIRLTY.NS',	'OFSS.NS',	'OIL.NS',	'OLECTRA.NS',	'ONGC.NS',	'ORIENTELEC.NS',	'PAGEIND.NS',	'PATANJALI.NS',	'PAYTM.NS',	'PCBL.NS',	'PERSISTENT.NS',	'PETRONET.NS',	'PFC.NS',	'PFIZER.NS',	'PGHH.NS',	'PGHL.NS',	'PHOENIXLTD.NS',	'PIDILITIND.NS',	'PIIND.NS',	'PNB.NS',	'PNBHOUSING.NS',	'PNCINFRA.NS',	'POLICYBZR.NS',	'POLYCAB.NS',	'POLYMED.NS',	'POLYPLEX.NS',	'POONAWALLA.NS',	'POWERGRID.NS',	'POWERINDIA.NS',	'PRAJIND.NS',	'PRESTIGE.NS',	'PRINCEPIPE.NS',	'PRIVISCL.NS',	'PRSMJOHNSN.NS',	'QUESS.NS',	'RADICO.NS',	'RAIN.NS',	'RAJESHEXPO.NS',	'RALLIS.NS',	'RAMCOCEM.NS',	'RATNAMANI.NS',	'RAYMOND.NS',	'RBA.NS',	'RBLBANK.NS',	'RCF.NS',	'RECLTD.NS',	'REDINGTON.NS',	'RELAXO.NS',	'RELIANCE.NS',	'RENUKA.NS',	'RHIM.NS',	'RITES.NS',	'ROSSARI.NS',	'ROUTE.NS',	'RTNINDIA.NS',	'RVNL.NS',	'SAIL.NS',	'SANOFI.NS',	'SAPPHIRE.NS',	'SAREGAMA.NS',	'SBILIFE.NS',	'SBIN.NS',	'SCHAEFFLER.NS',	'SCI.NS',	'SFL.NS',	'SHARDACROP.NS',	'SHILPAMED.NS',	'SHOPERSTOP.NS',	'SHREECEM.NS',	'SHRIRAMFIN.NS',	'SHYAMMETL.NS',	'SIEMENS.NS',	'SIS.NS',	'SJVN.NS',	'SKFINDIA.NS',	'SOBHA.NS',	'SOLARINDS.NS',	'SONACOMS.NS',	'SONATSOFTW.NS',	'SPARC.NS',	'SRF.NS',	'STARHEALTH.NS',	'STLTECH.NS',	'SUDARSCHEM.NS',	'SUMICHEM.NS',	'SUNDARMFIN.NS',	'SUNDRMFAST.NS',	'SUNPHARMA.NS',	'SUNTECK.NS',	'SUNTV.NS',	'SUPRAJIT.NS',	'SUPREMEIND.NS',	'SUVENPHAR.NS',	'SUZLON.NS',	'SWANENERGY.NS',	'SWSOLAR.NS',	'SYMPHONY.NS',	'SYNGENE.NS',	'TANLA.NS',	'TATACHEM.NS',	'TATACOFFEE.NS',	'TATACOMM.NS',	'TATACONSUM.NS',	'TATAELXSI.NS',	'TATAINVEST.NS',	'TATAMOTORS.NS',	'TATAMTRDVR.NS',	'TATAPOWER.NS',	'TATASTEEL.NS',	'TCI.NS',	'TCIEXP.NS',	'TCNSBRANDS.NS',	'TCS.NS',	'TEAMLEASE.NS',	'TECHM.NS',	'TEJASNET.NS',	'THERMAX.NS',	'THYROCARE.NS',	'TIINDIA.NS',	'TIMKEN.NS',	'TITAN.NS',	'TORNTPHARM.NS',	'TORNTPOWER.NS',	'TRENT.NS',	'TRIDENT.NS',	'TRITURBINE.NS',	'TRIVENI.NS',	'TTKPRESTIG.NS',	'TTML.NS',	'TV18BRDCST.NS',	'TVSMOTOR.NS',	'UBL.NS',	'UFLEX.NS',	'ULTRACEMCO.NS',	'UNIONBANK.NS',	'UNOMINDA.NS',	'UPL.NS',	'UTIAMC.NS',	'VAIBHAVGBL.NS',	'VARROC.NS',	'VBL.NS',	'VEDL.NS',	'VGUARD.NS',	'VIJAYA.NS',	'VINATIORGA.NS',	'VIPIND.NS',	'VMART.NS',	'VOLTAS.NS',	'VTL.NS',	'WELCORP.NS',	'WELSPUNIND.NS',	'WESTLIFE.NS',	'WHIRLPOOL.NS',	'WIPRO.NS',	'WOCKPHARMA.NS',	'YESBANK.NS',	'ZEEL.NS',	'ZENSARTECH.NS',	'ZFCVINDIA.NS',	'ZOMATO.NS',	'ZYDUSLIFE.NS',	'ZYDUSWELL.NS']

    print("script starting")
    subprocess.run(["python", "import yfinance as Dailydata.py"])
    subprocess.run(["python", "import yfinance as Weeklydata.py"])
    subprocess.run(["python", "data and analyze_adding more.py"])
    subprocess.run(["python", "file compare_fulllist.py"])
    
    Loaddata()
    subprocess.run(["python", "Report_generation.py"])