'''
Created on Nov 20, 2012

@author: vu
'''
from functions import *
import matplotlib.pylab as plt
import statsmodels.api as sm
from datetime import datetime as dt

# Clean up data
import foundation as fd
fx_data = fd.getFxRates()

# Subsetting data into foreign currencies
foreign = fx_data.ix[fx_data.Currency != 'USD',:]
foreign = foreign.groupby('Currency').apply(lambda x: x.ix[:,1:].fillna(method = 'ffill',limit = 30 ).asfreq('BM'))

# Compute monthly returns for each currency
monthly_rets = lambda x: x.SPOT/x.FRWD_1M.shift() - 1
foreign['rets'] = foreign[['SPOT','FRWD_1M']].groupby(level='Currency').apply(monthly_rets).values
foreign['mom_12'] = foreign.SPOT.groupby(level='Currency').pct_change().values 
foreign['mom_26'] = foreign.SPOT.groupby(level='Currency').pct_change(periods = 4).values

# Compute and test carry factor
foreign['carry'] = -(foreign.FRWD_1M/foreign.SPOT - 1)
foreign.carry = foreign.carry.groupby(level = 'Currency').shift()
foreign.mom_12 = foreign.mom_12.groupby(level = 'Currency').shift()
foreign.mom_26 = foreign.mom_26.groupby(level = 'Currency').shift(periods = 2)

carry_betas = foreign[['carry','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(carry_betas)
mom12_betas = foreign[['mom_12','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(mom12_betas)
mom26_betas = foreign[['mom_26','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(mom26_betas)