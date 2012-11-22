'''
Created on Nov 20, 2012

@author: vu
'''
import pandas as pd
import matplotlib.pylab as plt
import statsmodels.api as sm
import numpy as np
from datetime import datetime as dt
import os
ws = os.path.expanduser('~/Documents/workspace/qf-final-project/')
os.chdir(ws)

# Clean up data
fx_data = pd.read_csv('data/full.csv')
fx_data.ix[:,2:] = fx_data.ix[:,2:].replace('\\N', np.NaN).apply(np.float64)
fx_data.Date = fx_data.Date.map(lambda x: x[:10])
fx_data.Date = fx_data.Date.map(lambda x: dt.strptime(x, '%Y-%m-%d'))
fx_data = fx_data.set_index('Date')

# Subsetting data into foreign currencies
foreign = fx_data.ix[fx_data.Currency != 'USD',:]
foreign = foreign.groupby('Currency').apply(lambda x: x.ix[:,1:].fillna(method = 'ffill',limit = 30 ).asfreq('BM'))

# Compute monthly returns for each currency
monthly_rets = lambda x: x.SPOT/x.FRWD_1M.shift() - 1
foreign['rets'] = foreign[['SPOT','FRWD_1M']].groupby(level='Currency').apply(monthly_rets).values