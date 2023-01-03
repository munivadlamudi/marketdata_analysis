from nsetools import Nse 
import pandas as pd, numpy as np

nse = Nse()

print(nse)

q = pd.Series(nse.get_stock_codes())

print(q)