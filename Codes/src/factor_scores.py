from functions import *
import matplotlib.pylab as plt
import statsmodels.api as sm
from datetime import datetime as dt
import scipy.stats.stats as st
import pandas as pd

# Clean up data
import foundation as fd
fx_data = fd.getFxRates()

# Subsetting data into foreign currencies
foreign = fx_data.ix[fx_data.Currency != 'USD',:]
foreign = foreign.groupby('Currency').apply(lambda x: x.ix[:,1:].fillna(method = 'ffill',limit = 30 ).asfreq('BM'))

# Compute monthly returns for each currency
monthly_rets = lambda x: x.SPOT/x.FRWD_1M.shift() - 1
foreign['rets'] = foreign[['SPOT','FRWD_1M']].groupby(level='Currency').apply(monthly_rets).values

# Compute mom factors
foreign['mom_12'] = foreign.SPOT.groupby(level='Currency').pct_change().values 
foreign['mom_26'] = foreign.SPOT.groupby(level='Currency').pct_change(periods = 4).values

# Compute and test carry and mom factor
foreign['carry'] = -(foreign.FRWD_1M/foreign.SPOT - 1)
foreign.carry = foreign.carry.groupby(level = 'Currency').shift()
foreign.mom_12 = foreign.mom_12.groupby(level = 'Currency').shift()
foreign.mom_26 = foreign.mom_26.groupby(level = 'Currency').shift(periods = 2)

# All nan approaches have resulted in unwanted behavior/way too many deleted entries:
# This code should ignore all nan-values (just return them unmodified) and transform only
# non-nan values
# zscore = lambda x: (x-st.nanmean(x))/st.nanstd(x)
# Wraper for the zscore lambda
# def smart_zscore(x):
#     if(pd.isnull(x).all()):
#         return x
#     else:
#         return zscore(x)
#
# # This seems to work (very weird)
# foreign = foreign.groupby(level = 1).dropna()
# print foreign.groupby(level = 1).carry.transform(zscore)

carry_betas = foreign[['carry','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(carry_betas)
mom12_betas = foreign[['mom_12','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(mom12_betas)
mom26_betas = foreign[['mom_26','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(mom26_betas)

# Compute PPP factors
cpi = fd.get_monthly_CPI()
foreign_CPI = cpi.ix['AUD' : 'SEK']
US_CPI = cpi.ix['USD'].CPI
US_CPI.name = 'US_CPI'
US_CPI = US_CPI.reset_index() 
US_CPI = US_CPI.rename(columns = {'index': 'Date'})

lag = 3

def PPP(df):
    us = US_CPI.copy()
    us['Currency'] = df.index[0][0]
    us = us.set_index(['Currency','Date'])
    return df.SPOT*df.CPI/us.US_CPI

foreign_CPI['PPP'] = foreign_CPI.groupby(level='Currency').apply(PPP).values
foreign = foreign.join(foreign_CPI.PPP)
foreign.PPP = foreign.PPP.groupby(level = 'Currency').shift(periods = lag)
PPP_betas = foreign[['PPP','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(PPP_betas)

((1+carry_betas/100).cumprod()-1).plot()
plt.show()
