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

#===============================================================================
# Clean up data
#===============================================================================
fx_data = pd.read_csv('data/full.csv')
fx_data.ix[:,2:] = fx_data.ix[:,2:].replace('\\N', np.NaN).apply(np.float64)
fx_data.Date = fx_data.Date.map(lambda x: x[:10])
fx_data.Date = fx_data.Date.map(lambda x: dt.strptime(x, '%Y-%m-%d'))
fx_data.index = fx_data.Date
currency = fx_data.groupby('Currency')