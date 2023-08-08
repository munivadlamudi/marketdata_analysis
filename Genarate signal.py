from datetime import date,datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib

def Loaddata():
    for stock in stock_symbols:
        try:
            data = pd.read_csv('C:/Users/muniv/Desktop/Market/Compare/{}.csv'.format(stock)) 
            out_file_name1 = 'C:/Users/muniv/Desktop/Market/Compare/{}.csv'.format(stock)         
            buy_sell_function(data)
            #report_performance(data)
            print("Name of the stock : ",stock)
            #print(buy_sell_function(data)[0])
            data['Buy'] =   buy_sell_function(data)[0]
            data['Sell'] = buy_sell_function(data)[1]
            fresh_buy = data.iloc[-1]['Buy']
            fresh_sell = data.iloc[-1]['Sell']
            fresh_buy_1 = data.iloc[-2]['Buy']
            fresh_sell_1 = data.iloc[-2]['Sell']
            print("fresh_buy : ",fresh_buy)
            print("fresh_sell : ",fresh_sell)

            ou = pd.DataFrame(data)
            ou.to_csv(out_file_name1,encoding='utf-8')
            if not np.isnan(fresh_buy) and np.isnan(fresh_buy_1) :  
                with open("Buy_file.csv", "a") as f:
                    f.write(stock + " : " + str(fresh_buy) + "\n")
            if not np.isnan(fresh_sell) and np.isnan(fresh_sell_1) :
                print("check signals for sell #####")
                print("Write into Sell file")    
                with open("Sell_file.csv", "a") as f:
                    f.write(stock + " : " + str(fresh_sell)  +  "\n")
           
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

        close = data.iloc[i]['Close']
        open_price = data.iloc[i]['Open']
        high = data.iloc[i]['High']
        low = data.iloc[i]['Low']
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

        if SC_Candle and (EMAALrangeB or EMAALrangeB1) and flag_short == False and flag_long == False :
        # if  (EMAALrangeB or EMAALrangeB1) :
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
            fresh_long = True
        elif SC_Candle and (EMAALrangeS or EMAALrangeS1) and flag_long == False and flag_short == False :
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = True
            fresh_short = True
        elif flag_short == True and ((data['ema5'][i] > data['ema21'][i]) or data['cci34_1D'][i] >= 0 ):
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False
        elif flag_long == True and ((data['ema5'][i] < data['ema21'][i]) or data['cci34_1D'][i] <= 0 ):
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
    
    return (buy_list, sell_list)



if __name__ == "__main__":
    # Replace with the desired stock symbols followed by ".NS" for NSE stocks
    # stock_symbols = ['ADANIENT.NS',	'TCS.NS',	'RELIANCE.NS',	'AXISBANK.NS',	'INDUSINDBK.NS',	'ULTRACEMCO.NS',	'ICICIBANK.NS',	'NESTLEIND.NS',	'WIPRO.NS',	'SBIN.NS',	'ONGC.NS',	'DIVISLAB.NS',	'HCLTECH.NS',	'INFY.NS',	'TATACONSUM.NS',	'ASIANPAINT.NS',	'SUNPHARMA.NS',	'ITC.NS',	'BAJAJFINSV.NS', 'APOLLOHOSP.NS',	'CIPLA.NS',	'BAJAJ-AUTO.NS',	'JSWSTEEL.NS',	'KOTAKBANK.NS',	'TITAN.NS',	'COALINDIA.NS',	'GRASIM.NS',	'BPCL.NS',	'HINDALCO.NS',	'HDFCBANK.NS',	'HEROMOTOCO.NS',	'DRREDDY.NS',	'BAJFINANCE.NS',	'TATASTEEL.NS',	'TECHM.NS',	'POWERGRID.NS',	'HDFCLIFE.NS',	'ADANIPORTS.NS',	'NTPC.NS',	'BRITANNIA.NS',	'MARUTI.NS',	'LT.NS',	'M&M.NS',	'BHARTIARTL.NS',	'HINDUNILVR.NS',	'TATAMOTORS.NS',	'UPL.NS',	'EICHERMOT.NS',	'SBILIFE.NS',] 
    #stock_symbols = ['3MINDIA.NS',	'ABB.NS',	'ACC.NS',	'AIAENG.NS',	'APLAPOLLO.NS',	'AUBANK.NS',	'AARTIDRUGS.NS',	'AAVAS.NS',	'ABBOTINDIA.NS',	'ADANIENT.NS',	'ADANIGREEN.NS',	'ADANIPORTS.NS',	'ATGL.NS',	'ADANITRANS.NS',	'AWL.NS',	'ABCAPITAL.NS',	'ABFRL.NS',	'ABSLAMC.NS',	'AEGISCHEM.NS',	'AETHER.NS',	'AFFLE.NS',	'AJANTPHARM.NS',	'APLLTD.NS',	'ALKEM.NS',	'ALKYLAMINE.NS',	'ALLCARGO.NS',	'ALOKINDS.NS',	'AMARAJABAT.NS',	'AMBER.NS',	'AMBUJACEM.NS',	'ANGELONE.NS',	'ANURAS.NS',	'APOLLOHOSP.NS',	'APOLLOTYRE.NS',	'APTUS.NS',	'ASAHIINDIA.NS',	'ASHOKLEY.NS',	'ASIANPAINT.NS',	'ASTERDM.NS',	'ASTRAZEN.NS',	'ASTRAL.NS',	'ATUL.NS',	'AUROPHARMA.NS',	'AVANTIFEED.NS',	'DMART.NS',	'AXISBANK.NS',	'BASF.NS',	'BSE.NS',	'BAJAJ-AUTO.NS',	'BAJAJELEC.NS',	'BAJFINANCE.NS',	'BAJAJFINSV.NS',	'BAJAJHLDNG.NS',	'BALAMINES.NS',	'BALKRISIND.NS',	'BALRAMCHIN.NS',	'BANDHANBNK.NS',	'BANKBARODA.NS',	'BANKINDIA.NS',	'MAHABANK.NS',	'BATAINDIA.NS',	'BAYERCROP.NS',	'BERGEPAINT.NS',	'BDL.NS',	'BEL.NS',	'BHARATFORG.NS',	'BHEL.NS',	'BPCL.NS',	'BHARATRAS.NS',	'BHARTIARTL.NS',	'BIOCON.NS',	'BIRLACORPN.NS',	'BSOFT.NS',	'BLUEDART.NS',	'BLUESTARCO.NS',	'BBTC.NS',	'BORORENEW.NS',	'BOSCHLTD.NS',	'BRIGADE.NS',	'BCG.NS',	'BRITANNIA.NS',	'MAPMYINDIA.NS',	'CCL.NS',	'CESC.NS',	'CGPOWER.NS',	'CRISIL.NS',	'CSBBANK.NS',	'CAMPUS.NS',	'CANFINHOME.NS',	'CANBK.NS',	'CAPLIPOINT.NS',	'CGCL.NS',	'CARBORUNIV.NS',	'CASTROLIND.NS',	'CEATLTD.NS',	'CENTRALBK.NS',	'CDSL.NS',	'CENTURYPLY.NS',	'CENTURYTEX.NS',	'CERA.NS',	'CHALET.NS',	'CHAMBLFERT.NS',	'CHEMPLASTS.NS',	'CHOLAHLDNG.NS',	'CHOLAFIN.NS',	'CIPLA.NS',	'CUB.NS',	'CLEAN.NS',	'COALINDIA.NS',	'COCHINSHIP.NS',	'COFORGE.NS',	'COLPAL.NS',	'CAMS.NS',	'CONCOR.NS',	'COROMANDEL.NS',	'CREDITACC.NS',	'CROMPTON.NS',	'CUMMINSIND.NS',	'CYIENT.NS',	'DCMSHRIRAM.NS',	'DLF.NS',	'DABUR.NS',	'DALBHARAT.NS',	'DEEPAKFERT.NS',	'DEEPAKNTR.NS',	'DELHIVERY.NS',	'DELTACORP.NS',	'DEVYANI.NS',	'DHANI.NS',	'DBL.NS',	'DIVISLAB.NS',	'DIXON.NS',	'LALPATHLAB.NS',	'DRREDDY.NS',	'EIDPARRY.NS',	'EIHOTEL.NS',	'EPL.NS',	'EASEMYTRIP.NS',	'EDELWEISS.NS',	'EICHERMOT.NS',	'ELGIEQUIP.NS',	'EMAMILTD.NS',	'ENDURANCE.NS',	'ENGINERSIN.NS',	'EQUITASBNK.NS',	'ESCORTS.NS',	'EXIDEIND.NS',	'FDC.NS',	'NYKAA.NS',	'FEDERALBNK.NS',	'FACT.NS',	'FINEORG.NS',	'FINCABLES.NS',	'FINPIPE.NS',	'FSL.NS',	'FORTIS.NS',	'GRINFRA.NS',	'GAIL.NS',	'GMMPFAUDLR.NS',	'GMRINFRA.NS',	'GALAXYSURF.NS',	'GARFIBRES.NS',	'GICRE.NS',	'GLAND.NS',	'GLAXO.NS',	'GLENMARK.NS',	'GOCOLORS.NS',	'GODFRYPHLP.NS',	'GODREJAGRO.NS',	'GODREJCP.NS',	'GODREJIND.NS',	'GODREJPROP.NS',	'GRANULES.NS',	'GRAPHITE.NS',	'GRASIM.NS',	'GESHIP.NS',	'GREENPANEL.NS',	'GRINDWELL.NS',	'GUJALKALI.NS',	'GAEL.NS',	'FLUOROCHEM.NS',	'GUJGASLTD.NS',	'GNFC.NS',	'GPPL.NS',	'GSFC.NS',	'GSPL.NS',	'HEG.NS',	'HCLTECH.NS',	'HDFCAMC.NS',	'HDFCBANK.NS',	'HDFCLIFE.NS',	'HFCL.NS',	'HLEGLAS.NS',	'HAPPSTMNDS.NS',	'HATSUN.NS',	'HAVELLS.NS',	'HEROMOTOCO.NS',	'HIKAL.NS',	'HINDALCO.NS',	'HGS.NS',	'HAL.NS',	'HINDCOPPER.NS',	'HINDPETRO.NS',	'HINDUNILVR.NS',	'HINDZINC.NS',	'POWERINDIA.NS',	'HOMEFIRST.NS',	'HONAUT.NS',	'HUDCO.NS',	'ICICIBANK.NS',	'ICICIGI.NS',	'ICICIPRULI.NS',	'ISEC.NS',	'IDBI.NS',	'IDFCFIRSTB.NS',	'IDFC.NS',	'IFBIND.NS',	'IIFL.NS',	'IRB.NS',	'ITC.NS',	'ITI.NS',	'INDIACEM.NS',	'IBULHSGFIN.NS',	'IBREALEST.NS',	'INDIAMART.NS',	'INDIANB.NS',	'IEX.NS',	'INDHOTEL.NS',	'IOC.NS',	'IOB.NS',	'IRCTC.NS',	'IRFC.NS',	'INDIGOPNTS.NS',	'INDOCO.NS',	'IGL.NS',	'INDUSTOWER.NS',	'INDUSINDBK.NS',	'INFIBEAM.NS',	'NAUKRI.NS',	'INFY.NS',	'INOXLEISUR.NS',	'INTELLECT.NS',	'INDIGO.NS',	'IPCALAB.NS',	'JBCHEPHARM.NS',	'JKCEMENT.NS',	'JBMA.NS',	'JKLAKSHMI.NS',	'JKPAPER.NS',	'JMFINANCIL.NS',	'JSWENERGY.NS',	'JSWSTEEL.NS',	'JAMNAAUTO.NS',	'JSL.NS',	'JINDALSTEL.NS',	'JUBLFOOD.NS',	'JUBLINGREA.NS',	'JUBLPHARMA.NS',	'JUSTDIAL.NS',	'JYOTHYLAB.NS',	'KPRMILL.NS',	'KEI.NS',	'KNRCON.NS',	'KPITTECH.NS',	'KRBL.NS',	'KAJARIACER.NS',	'KALPATPOWR.NS',	'KALYANKJIL.NS',	'KANSAINER.NS',	'KARURVYSYA.NS',	'KEC.NS',	'KOTAKBANK.NS',	'KIMS.NS',	'L&TFH.NS',	'LTTS.NS',	'LICHSGFIN.NS',	'LTIM.NS',	'LAXMIMACH.NS',	'LT.NS',	'LATENTVIEW.NS',	'LAURUSLABS.NS',	'LXCHEM.NS',	'LICI.NS',	'LINDEINDIA.NS',	'LUPIN.NS',	'LUXIND.NS',	'MMTC.NS',	'MOIL.NS',	'MRF.NS',	'MTARTECH.NS',	'LODHA.NS',	'MGL.NS',	'M&MFIN.NS',	'M&M.NS',	'MAHINDCIE.NS',	'MHRIL.NS',	'MAHLIFE.NS',	'MAHLOG.NS',	'MANAPPURAM.NS',	'MRPL.NS',	'MARICO.NS',	'MARUTI.NS',	'MASTEK.NS',	'MFSL.NS',	'MAXHEALTH.NS',	'MAZDOCK.NS',	'MEDPLUS.NS',	'METROBRAND.NS',	'METROPOLIS.NS',	'MSUMI.NS',	'MOTILALOFS.NS',	'MPHASIS.NS',	'MCX.NS',	'MUTHOOTFIN.NS',	'NATCOPHARM.NS',	'NBCC.NS',	'NCC.NS',	'NHPC.NS',	'NIITLTD.NS',	'NLCINDIA.NS',	'NOCIL.NS',	'NTPC.NS',	'NH.NS',	'NATIONALUM.NS',	'NAVINFLUOR.NS',	'NAZARA.NS',	'NESTLEIND.NS',	'NETWORK18.NS',	'NAM-INDIA.NS',	'NUVOCO.NS',	'OBEROIRLTY.NS',	'ONGC.NS',	'OIL.NS',	'OLECTRA.NS',	'PAYTM.NS',	'OFSS.NS',	'ORIENTELEC.NS',	'POLICYBZR.NS',	'PCBL.NS',	'PIIND.NS',	'PNBHOUSING.NS',	'PNCINFRA.NS',	'PAGEIND.NS',	'PATANJALI.NS',	'PERSISTENT.NS',	'PETRONET.NS',	'PFIZER.NS',	'PHOENIXLTD.NS',	'PIDILITIND.NS',	'POLYMED.NS',	'POLYCAB.NS',	'POLYPLEX.NS',	'POONAWALLA.NS',	'PFC.NS',	'POWERGRID.NS',	'PRAJIND.NS',	'PRESTIGE.NS',	'PRINCEPIPE.NS',	'PRSMJOHNSN.NS',	'PRIVISCL.NS',	'PGHL.NS',	'PGHH.NS',	'PNB.NS',	'QUESS.NS',	'RBLBANK.NS',	'RECLTD.NS',	'RHIM.NS',	'RITES.NS',	'RADICO.NS',	'RVNL.NS',	'RAIN.NS',	'RAJESHEXPO.NS',	'RALLIS.NS',	'RCF.NS',	'RATNAMANI.NS',	'RTNINDIA.NS',	'RAYMOND.NS',	'REDINGTON.NS',	'RELAXO.NS',	'RELIANCE.NS',	'RBA.NS',	'ROSSARI.NS',	'ROUTE.NS',	 'SBILIFE.NS',	'SIS.NS',	'SJVN.NS',	'SKFINDIA.NS',	'SRF.NS',	'MOTHERSON.NS',	'SANOFI.NS',	'SAPPHIRE.NS',	'SAREGAMA.NS',	'SCHAEFFLER.NS',	'SHARDACROP.NS',	'SFL.NS',	'SHILPAMED.NS',	'SCI.NS',	'SHOPERSTOP.NS',	'SHREECEM.NS',	'RENUKA.NS',	'SHRIRAMFIN.NS',	'SHYAMMETL.NS',	'SIEMENS.NS',	'SOBHA.NS',	'SOLARINDS.NS',	'SONACOMS.NS',	'SONATSOFTW.NS',	'STARHEALTH.NS',	'SBIN.NS',	'SAIL.NS',	'SWSOLAR.NS',	'STLTECH.NS',	'SUDARSCHEM.NS',	'SUMICHEM.NS',	'SPARC.NS',	'SUNPHARMA.NS',	'SUNTV.NS',	'SUNDARMFIN.NS',	'SUNDRMFAST.NS',	'SUNTECK.NS',	'SUPRAJIT.NS',	'SUPREMEIND.NS',	'SUVENPHAR.NS',	'SUZLON.NS',	'SWANENERGY.NS',	'SYMPHONY.NS',	'SYNGENE.NS',	'TCIEXP.NS',	'TCNSBRANDS.NS',	'TTKPRESTIG.NS',	'TV18BRDCST.NS',	'TVSMOTOR.NS',	'TANLA.NS',	'TATACHEM.NS',	'TATACOFFEE.NS',	'TATACOMM.NS',	'TCS.NS',	'TATACONSUM.NS',	'TATAELXSI.NS',	'TATAINVEST.NS',	'TATAMTRDVR.NS',	'TATAMOTORS.NS',	'TATAPOWER.NS',	'TATASTEEL.NS',	'TTML.NS',	'TEAMLEASE.NS',	'TECHM.NS',	'TEJASNET.NS',	'NIACL.NS',	'RAMCOCEM.NS',	'THERMAX.NS',	'THYROCARE.NS',	'TIMKEN.NS',	'TITAN.NS',	'TORNTPHARM.NS',	'TORNTPOWER.NS',	'TCI.NS',	'TRENT.NS',	'TRIDENT.NS',	'TRIVENI.NS',	'TRITURBINE.NS',	'TIINDIA.NS',	'UFLEX.NS',	'UNOMINDA.NS',	'UPL.NS',	'UTIAMC.NS',	'ULTRACEMCO.NS',	'UNIONBANK.NS',	'UBL.NS',	'MCDOWELL-N.NS',	'VGUARD.NS',	'VMART.NS',	'VIPIND.NS',	'VAIBHAVGBL.NS',	'VTL.NS',	'VARROC.NS',	'VBL.NS',	'MANYAVAR.NS',	'VEDL.NS',	'VIJAYA.NS',	'VINATIORGA.NS',	'IDEA.NS',	'VOLTAS.NS',	'WELCORP.NS',	'WELSPUNIND.NS',	'WESTLIFE.NS',	'WHIRLPOOL.NS',	'WIPRO.NS',	'WOCKPHARMA.NS',	'YESBANK.NS',	'ZFCVINDIA.NS',	'ZEEL.NS',	'ZENSARTECH.NS',	'ZOMATO.NS',	'ZYDUSLIFE.NS',	'ZYDUSWELL.NS',	'ECLERX.NS']
    stock_symbols = ['ZOMATO.NS']
    start_date = "2023-01-01"  # Replace with the desired start date
    # end_date = "2023-08-02"    # Replace with the desired end date
    end_date = date.today()
    print("script starting")
    #Importdata()   
    Loaddata()