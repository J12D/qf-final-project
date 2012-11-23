'''
Created on Nov 22, 2012

@author: alex
'''

import pandas as pd
import matplotlib.pylab as plt
import statsmodels.api as sm
from scipy import stats
import numpy as np
from datetime import datetime as dt
import os
ws = os.path.expanduser('~/Documents/workspace/qf-final-project/')
os.chdir(ws)

# Clean up data
fx_data = pd.read_csv('data/full.csv')
fx_data = fx_data[['Date', 'Currency', 'SPOT']]
fx_data.SPOT = fx_data.SPOT.replace('\\N', np.NaN).apply(np.float64)
fx_data.Date = fx_data.Date.map(lambda x: x[:10])
fx_data.Date = fx_data.Date.map(lambda x: dt.strptime(x, '%Y-%m-%d'))

# Subsetting data into foreign currencies
foreign = fx_data.ix[fx_data.Currency != 'USD',:]
foreign = foreign.set_index(['Currency', 'Date'])
foreign = foreign.groupby(level = 0).apply(lambda x: x.fillna(method = 'ffill',limit = 30 ))
foreign['spot_rets'] = foreign.groupby(level = 0).SPOT.pct_change()
TI = pd.DataFrame()
for name, rets in foreign.groupby(level = 0).spot_rets:
    if TI.empty:
        TI = pd.DataFrame(index = [i[1] for i in rets.index])
        TI[name] = rets.values
    else:
        TI = TI.join(pd.Series(rets.values, index = [i[1] for i in rets.index], name = name))

TI = TI.dropna()
index = TI.index
TI.index = range(len(TI))
Turbulence = pd.DataFrame(index = TI.index)
Turbulence['values'] = np.NaN

for i in xrange(20,len(TI)):
    mean = TI.ix[:i-1].mean().values
    cov = np.matrix(np.cov(TI.ix[:i-1].T))
    rets = TI.ix[i].values
    d = rets - mean 
    Turbulence.ix[i,'values'] = d.dot(cov.I).dot(d.T)
    
Turbulence.index = index
     
    
    
