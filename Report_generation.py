from datetime import date, datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as talib
import subprocess
import os

def ReportGen(stock_symbols):
    report_data = []
    
    for stock in stock_symbols:
        try:
            data = pd.read_csv('C:/Users/muniv/Desktop/Market/Signals/{}.csv'.format(stock))
            print(stock)
            for index, row in data.iterrows():
                # print('in entry buy loop@@@@@')
                if row['Buy_Entry'] == 'freshe buy':
                    date_trig = row['Date_new']
                    # date_trig = datetime.strptime(date_trig, '%d-%m-%Y')
                    # print('buy entry date :',date_trig)
                                       
                    for idx, sell_row in data.iterrows():
                        selldate = sell_row.at['Date']
                        # selldate = datetime.strptime(selldate, '%d-%m-%Y')
                        exit_found = False  # Flag to exit the loop
                        # print('in exit buy loop')
                        if selldate > date_trig and sell_row['exit_buy'] == 'Exit buy':
                            # print("sell date  :", selldate  )
                            # print("date_trig  :", date_trig  )
                            # print("Buy ext data :",sell_row['Date'])
                            if row['Close'] > sell_row['Close']:
                            
                                new_record = {
                                    'Stock Name': stock,
                                    'Entry price': row['Close'],
                                    'Entry Date': row['Date'],
                                    'Exit Price': sell_row['Close'],
                                    # 'Exit Date': selldate.strftime('%Y-%m-%d'),
                                    'Exit Date': sell_row['Date'],
                                    'Loss': sell_row['Close'] - row['Close']
                                }
                            else:    
                                 new_record = {
                                    'Stock Name': stock,
                                    'Entry price': row['Close'],
                                    'Entry Date': row['Date'],
                                    'Exit Price': sell_row['Close'],
                                    # 'Exit Date': selldate.strftime('%Y-%m-%d'),
                                    'Exit Date': sell_row['Date'],
                                    'Profit':  sell_row['Close'] - row['Close'] 
                                }
                            # print("'new record : ",new_record)
                            report_data.append(new_record)
                            exit_found = True  
                            break  
        except KeyError as e:
            print(f"Exception: {e}")

    report_gen = 'C:/Users/muniv/Desktop/Market/marketdata_analysis/Reports.csv'
    report_df = pd.DataFrame(report_data)
    report_df.to_csv(report_gen, encoding='utf-8', index=False)

if __name__ == "__main__":
    # stock_symbols = ['3MINDIA.NS'] #, 'AARTIDRUGS.NS', 'AAVAS.NS']
    stock_symbols = [	'AARTIDRUGS.NS',	'AAVAS.NS',	'ABB.NS',	'ABBOTINDIA.NS',	'ABCAPITAL.NS',	'ABFRL.NS',	'ABSLAMC.NS',	'ACC.NS',	'ADANIENT.NS',	'ADANIGREEN.NS',	'ADANIPORTS.NS',	'ADANITRANS.NS',	'AEGISCHEM.NS',	'AETHER.NS',	'AFFLE.NS',	'AIAENG.NS',	'AJANTPHARM.NS',	'ALKEM.NS',	'ALKYLAMINE.NS',	'ALLCARGO.NS',	'ALOKINDS.NS',	'AMARAJABAT.NS',	'AMBER.NS',	'AMBUJACEM.NS',	'ANGELONE.NS',	'ANURAS.NS',	'APLAPOLLO.NS',	'APLLTD.NS',	'APOLLOHOSP.NS',	'APOLLOTYRE.NS',	'APTUS.NS',	'ASAHIINDIA.NS',	'ASHOKLEY.NS',	'ASIANPAINT.NS',	'ASTERDM.NS',	'ASTRAL.NS',	'ASTRAZEN.NS',	'ATGL.NS',	'ATUL.NS',	'AUBANK.NS',	'AUROPHARMA.NS',	'AVANTIFEED.NS',	'AWL.NS',	'AXISBANK.NS',	'BAJAJ-AUTO.NS',	'BAJAJELEC.NS',	'BAJAJFINSV.NS',	'BAJAJHLDNG.NS',	'BAJFINANCE.NS',	'BALAMINES.NS',	'BALKRISIND.NS',	'BALRAMCHIN.NS',	'BANDHANBNK.NS',	'BANKBARODA.NS',	'BANKINDIA.NS',	'BASF.NS',	'BATAINDIA.NS',	'BAYERCROP.NS',	'BBTC.NS',	'BCG.NS',	'BDL.NS',	'BEL.NS',	'BERGEPAINT.NS',	'BHARATFORG.NS',	'BHARATRAS.NS',	'BHARTIARTL.NS',	'BHEL.NS',	'BIOCON.NS',	'BIRLACORPN.NS',	'BLUEDART.NS',	'BLUESTARCO.NS',	'BORORENEW.NS',	'BOSCHLTD.NS',	'BPCL.NS',	'BRIGADE.NS',	'BRITANNIA.NS',	'BSE.NS',	'BSOFT.NS',	'CAMPUS.NS',	'CAMS.NS',	'CANBK.NS',	'CANFINHOME.NS',	'CAPLIPOINT.NS',	'CARBORUNIV.NS',	'CASTROLIND.NS',	'CCL.NS',	'CDSL.NS',	'CEATLTD.NS',	'CENTRALBK.NS',	'CENTURYPLY.NS',	'CENTURYTEX.NS',	'CERA.NS',	'CESC.NS',	'CGCL.NS',	'CGPOWER.NS',	'CHALET.NS',	'CHAMBLFERT.NS',	'CHEMPLASTS.NS',	'CHOLAFIN.NS',	'CHOLAHLDNG.NS',	'CIPLA.NS',	'CLEAN.NS',	'COALINDIA.NS',	'COCHINSHIP.NS',	'COFORGE.NS',	'COLPAL.NS',	'CONCOR.NS',	'COROMANDEL.NS',	'CREDITACC.NS',	'CRISIL.NS',	'CROMPTON.NS',	'CSBBANK.NS',	'CUB.NS',	'CUMMINSIND.NS',	'CYIENT.NS',	'DABUR.NS',	'DALBHARAT.NS',	'DBL.NS',	'DCMSHRIRAM.NS',	'DEEPAKFERT.NS',	'DEEPAKNTR.NS',	'DELHIVERY.NS',	'DELTACORP.NS',	'DEVYANI.NS',	'DHANI.NS',	'DIVISLAB.NS',	'DIXON.NS',	'DLF.NS',	'DMART.NS',	'DRREDDY.NS',	'EASEMYTRIP.NS',	'ECLERX.NS',	'EDELWEISS.NS',	'EICHERMOT.NS',	'EIDPARRY.NS',	'EIHOTEL.NS',	'ELGIEQUIP.NS',	'EMAMILTD.NS',	'ENDURANCE.NS',	'ENGINERSIN.NS',	'EPL.NS',	'EQUITASBNK.NS',	'ESCORTS.NS',	'EXIDEIND.NS',	'FACT.NS',	'FDC.NS',	'FEDERALBNK.NS',	'FINCABLES.NS',	'FINEORG.NS',	'FINPIPE.NS',	'FLUOROCHEM.NS',	'FORTIS.NS',	'FSL.NS',	'GAEL.NS',	'GAIL.NS',	'GALAXYSURF.NS',	'GARFIBRES.NS',	'GESHIP.NS',	'GICRE.NS',	'GLAND.NS',	'GLAXO.NS',	'GLENMARK.NS',	'GMMPFAUDLR.NS',	'GMRINFRA.NS',	'GNFC.NS',	'GOCOLORS.NS',	'GODFRYPHLP.NS',	'GODREJAGRO.NS',	'GODREJCP.NS',	'GODREJIND.NS',	'GODREJPROP.NS',	'GPPL.NS',	'GRANULES.NS',	'GRAPHITE.NS',	'GRASIM.NS',	'GREENPANEL.NS',	'GRINDWELL.NS',	'GRINFRA.NS',	'GSFC.NS',	'GSPL.NS',	'GUJALKALI.NS',	'GUJGASLTD.NS',	'HAL.NS',	'HAPPSTMNDS.NS',	'HATSUN.NS',	'HAVELLS.NS',	'HCLTECH.NS',	'HDFCAMC.NS',	'HDFCBANK.NS',	'HDFCLIFE.NS',	'HEG.NS',	'HEROMOTOCO.NS',	'HFCL.NS',	'HGS.NS',	'HIKAL.NS',	'HINDALCO.NS',	'HINDCOPPER.NS',	'HINDPETRO.NS',	'HINDUNILVR.NS',	'HINDZINC.NS',	'HLEGLAS.NS',	'HOMEFIRST.NS',	'HONAUT.NS',	'HUDCO.NS',	'IBREALEST.NS',	'IBULHSGFIN.NS',	'ICICIBANK.NS',	'ICICIGI.NS',	'ICICIPRULI.NS',	'IDBI.NS',	'IDEA.NS',	'IDFC.NS',	'IDFCFIRSTB.NS',	'IEX.NS',	'IFBIND.NS',	'IGL.NS',	'IIFL.NS',	'INDHOTEL.NS',	'INDIACEM.NS',	'INDIAMART.NS',	'INDIANB.NS',	'INDIGO.NS',	'INDIGOPNTS.NS',	'INDOCO.NS',	'INDUSINDBK.NS',	'INDUSTOWER.NS',	'INFIBEAM.NS',	'INFY.NS',	'INOXLEISUR.NS',	'INTELLECT.NS',	'IOB.NS',	'IOC.NS',	'IPCALAB.NS',	'IRB.NS',	'IRCTC.NS',	'IRFC.NS',	'ISEC.NS',	'ITC.NS',	'ITI.NS',	'JAMNAAUTO.NS',	'JBCHEPHARM.NS',	'JBMA.NS',	'JINDALSTEL.NS',	'JKCEMENT.NS',	'JKLAKSHMI.NS',	'JKPAPER.NS',	'JMFINANCIL.NS',	'JSL.NS',	'JSWENERGY.NS',	'JSWSTEEL.NS',	'JUBLFOOD.NS',	'JUBLINGREA.NS',	'JUBLPHARMA.NS',	'JUSTDIAL.NS',	'JYOTHYLAB.NS',	'KAJARIACER.NS', 'KALYANKJIL.NS',	'KANSAINER.NS',	'KARURVYSYA.NS',	'KEC.NS',	'KEI.NS',	'KIMS.NS',	'KNRCON.NS',	'KOTAKBANK.NS',	'KPITTECH.NS',	'KPRMILL.NS',	'KRBL.NS',	'L&TFH.NS',	'LALPATHLAB.NS',	'LATENTVIEW.NS',	'LAURUSLABS.NS',	'LAXMIMACH.NS',	'LICHSGFIN.NS',	'LICI.NS',	'LINDEINDIA.NS',	'LODHA.NS',	'LT.NS',	'LTIM.NS',	'LTTS.NS',	'LUPIN.NS',	'LUXIND.NS',	'LXCHEM.NS',	'M&M.NS',	'M&MFIN.NS',	'MAHABANK.NS',	'MAHINDCIE.NS',	'MAHLIFE.NS',	'MAHLOG.NS',	'MANAPPURAM.NS',	'MANYAVAR.NS',	'MAPMYINDIA.NS',	'MARICO.NS',	'MARUTI.NS',	'MASTEK.NS',	'MAXHEALTH.NS',	'MAZDOCK.NS',	'MCDOWELL-N.NS',	'MCX.NS',	'MEDPLUS.NS',	'METROBRAND.NS',	'METROPOLIS.NS',	'MFSL.NS',	'MGL.NS',	'MHRIL.NS',	'MMTC.NS',	'MOIL.NS',	'MOTHERSON.NS',	'MOTILALOFS.NS',	'MPHASIS.NS',	'MRF.NS',	'MRPL.NS',	'MSUMI.NS',	'MTARTECH.NS',	'MUTHOOTFIN.NS',	'NAM-INDIA.NS',	'NATCOPHARM.NS',	'NATIONALUM.NS',	'NAUKRI.NS',	'NAVINFLUOR.NS',	'NAZARA.NS',	'NBCC.NS',	'NCC.NS',	'NESTLEIND.NS',	'NETWORK18.NS',	'NH.NS',	'NHPC.NS',	'NIACL.NS',	'NIITLTD.NS',	'NLCINDIA.NS',	'NOCIL.NS',	'NTPC.NS',	'NUVOCO.NS',	'NYKAA.NS',	'OBEROIRLTY.NS',	'OFSS.NS',	'OIL.NS',	'OLECTRA.NS',	'ONGC.NS',	'ORIENTELEC.NS',	'PAGEIND.NS',	'PATANJALI.NS',	'PAYTM.NS',	'PCBL.NS',	'PERSISTENT.NS',	'PETRONET.NS',	'PFC.NS',	'PFIZER.NS',	'PGHH.NS',	'PGHL.NS',	'PHOENIXLTD.NS',	'PIDILITIND.NS',	'PIIND.NS',	'PNB.NS',	'PNBHOUSING.NS',	'PNCINFRA.NS',	'POLICYBZR.NS',	'POLYCAB.NS',	'POLYMED.NS',	'POLYPLEX.NS',	'POONAWALLA.NS',	'POWERGRID.NS',	'POWERINDIA.NS',	'PRAJIND.NS',	'PRESTIGE.NS',	'PRINCEPIPE.NS',	'PRIVISCL.NS',	'PRSMJOHNSN.NS',	'QUESS.NS',	'RADICO.NS',	'RAIN.NS',	'RAJESHEXPO.NS',	'RALLIS.NS',	'RAMCOCEM.NS',	'RATNAMANI.NS',	'RAYMOND.NS',	'RBA.NS',	'RBLBANK.NS',	'RCF.NS',	'RECLTD.NS',	'REDINGTON.NS',	'RELAXO.NS',	'RELIANCE.NS',	'RENUKA.NS',	'RHIM.NS',	'RITES.NS',	'ROSSARI.NS',	'ROUTE.NS',	'RTNINDIA.NS',	'RVNL.NS',	'SAIL.NS',	'SANOFI.NS',	'SAPPHIRE.NS',	'SAREGAMA.NS',	'SBILIFE.NS',	'SBIN.NS',	'SCHAEFFLER.NS',	'SCI.NS',	'SFL.NS',	'SHARDACROP.NS',	'SHILPAMED.NS',	'SHOPERSTOP.NS',	'SHREECEM.NS',	'SHRIRAMFIN.NS',	'SHYAMMETL.NS',	'SIEMENS.NS',	'SIS.NS',	'SJVN.NS',	'SKFINDIA.NS',	'SOBHA.NS',	'SOLARINDS.NS',	'SONACOMS.NS',	'SONATSOFTW.NS',	'SPARC.NS',	'SRF.NS',	'STARHEALTH.NS',	'STLTECH.NS',	'SUDARSCHEM.NS',	'SUMICHEM.NS',	'SUNDARMFIN.NS',	'SUNDRMFAST.NS',	'SUNPHARMA.NS',	'SUNTECK.NS',	'SUNTV.NS',	'SUPRAJIT.NS',	'SUPREMEIND.NS',	'SUVENPHAR.NS',	'SUZLON.NS',	'SWANENERGY.NS',	'SWSOLAR.NS',	'SYMPHONY.NS',	'SYNGENE.NS',	'TANLA.NS',	'TATACHEM.NS',	'TATACOFFEE.NS',	'TATACOMM.NS',	'TATACONSUM.NS',	'TATAELXSI.NS',	'TATAINVEST.NS',	'TATAMOTORS.NS',	'TATAMTRDVR.NS',	'TATAPOWER.NS',	'TATASTEEL.NS',	'TCI.NS',	'TCIEXP.NS',	'TCNSBRANDS.NS',	'TCS.NS',	'TEAMLEASE.NS',	'TECHM.NS',	'TEJASNET.NS',	'THERMAX.NS',	'THYROCARE.NS',	'TIINDIA.NS',	'TIMKEN.NS',	'TITAN.NS',	'TORNTPHARM.NS',	'TORNTPOWER.NS',	'TRENT.NS',	'TRIDENT.NS',	'TRITURBINE.NS',	'TRIVENI.NS',	'TTKPRESTIG.NS',	'TTML.NS',	'TV18BRDCST.NS',	'TVSMOTOR.NS',	'UBL.NS',	'UFLEX.NS',	'ULTRACEMCO.NS',	'UNIONBANK.NS',	'UNOMINDA.NS',	'UPL.NS',	'UTIAMC.NS',	'VAIBHAVGBL.NS',	'VARROC.NS',	'VBL.NS',	'VEDL.NS',	'VGUARD.NS',	'VIJAYA.NS',	'VINATIORGA.NS',	'VIPIND.NS',	'VMART.NS',	'VOLTAS.NS',	'VTL.NS',	'WELCORP.NS',	'WELSPUNIND.NS',	'WESTLIFE.NS',	'WHIRLPOOL.NS',	'WIPRO.NS',	'WOCKPHARMA.NS',	'YESBANK.NS',	'ZEEL.NS',	'ZENSARTECH.NS',	'ZFCVINDIA.NS',	'ZOMATO.NS',	'ZYDUSLIFE.NS',	'ZYDUSWELL.NS']

    print("Script starting...")
    ReportGen(stock_symbols)
    print("Report generation complete.")
