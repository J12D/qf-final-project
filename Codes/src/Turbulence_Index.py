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
from functions import efa

# Clean up data
import foundation as fd
fx_data = fd.getFxRates()
fx_data = fx_data[['Currency', 'SPOT']]

# Subsetting data into foreign currencies
foreign = fx_data.ix[fx_data.Currency != 'USD',:]
foreign = foreign.set_index('Currency', append = True)
foreign = foreign.groupby(level = 1).apply(lambda x: x.fillna(method = 'ffill',limit = 30 ))
foreign['spot_rets'] = foreign.groupby(level = 1).SPOT.pct_change()
TI = pd.DataFrame()
for name, rets in foreign.groupby(level = 1).spot_rets:
    if TI.empty:
        TI = pd.DataFrame(index = [i[0] for i in rets.index])
        TI[name] = rets.values
    else:
        TI = TI.join(pd.Series(rets.values, index = [i[0] for i in rets.index], name = name))

TI = TI.dropna()
index = TI.index
TI.index = range(len(TI))
Turbulence = pd.DataFrame(index = TI.index)
Turbulence['TI'] = np.NaN

for i in xrange(20,len(TI)):
    mean = TI.ix[:i-1].mean().values
    cov = np.matrix(np.cov(TI.ix[:i-1].T))
    rets = TI.ix[i].values
    d = rets - mean 
    Turbulence.ix[i,'TI'] = d.dot(cov.I).dot(d.T)
    
Turbulence.index = index
Turbulence = Turbulence.dropna()

Turbulence['MA'] = efa(Turbulence.TI,1,30)
Turbulence.MA.ix[:29] = np.NaN

def get_weight(interval, q, method = 'continuous'):
    if not q:
        return np.NaN
    pc = sum(interval <= q)/np.float64(len(interval))
    if method == 'continuous':
        if pc <= 0.2:
            return 1.0
        elif pc <= 0.4:
            return 0.8
        elif pc <= 0.6:
            return 0.6
        elif pc <= 0.8:
            return 0.4
        else:
            return 0.2
    elif method == 'discrete':
        if pc <= 0.8:
            return 1
        else:
            return 0
    else:
        raise ValueError('Unrecognized method')


Turbulence['cont_weight'] = np.NaN
Turbulence['discrete_weight'] = np.NaN
for i in xrange(3*365+1,len(Turbulence)):
    Turbulence.ix[i,'cont_weight'] =\
    get_weight(Turbulence.TI[(i-3*365+1):(i-1)], Turbulence.TI[i-1])
    Turbulence.ix[i,'discrete_weight'] =\
    get_weight(Turbulence.TI[(i-3*365+1):(i-1)], Turbulence.TI[i-1], method = 'discrete')

Turbulence = Turbulence.reset_index()
Turbulence.columns = ['Date', 'TI', 'MA', 'cont', 'discrete']
Turbulence.to_csv('data/TI')         
    
    
