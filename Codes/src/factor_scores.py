'''
Created on Nov 20, 2012

@author: vu
'''
import pandas as pd
import matplotlib.pylab as plt
import statsmodels.api as sm
import numpy as np
import os
ws = os.path.expanduser('~/qf-final-project/')
os.chdir(ws)

#===============================================================================
# Clean up data
#===============================================================================
fx_data = pd.read_csv('data/full.csv', sep = '\t')
fx_data.GOVT_YIELD_10YR = fx_data.GOVT_YIELD_10YR.apply(lambda x: x[:-2])
fx_data.ix[:,2:6] = fx_data.ix[:,2:6].replace('\\N', np.NaN).apply(np.float64)
 