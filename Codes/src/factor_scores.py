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

lag = 18

def PPP(df):
    us = US_CPI.copy()
    us['Currency'] = df.index[0][0]
    us = us.set_index(['Currency','Date'])
    return df.SPOT*df.CPI/us.US_CPI


foreign_CPI['PPP'] = foreign_CPI.groupby(level='Currency').apply(PPP).values
foreign = foreign.join(foreign_CPI.PPP)
foreign.PPP = foreign.PPP.groupby(level = 'Currency').transform(lambda x: -(x/x[0]))
foreign.PPP = foreign.PPP.groupby(level = 'Currency').shift(periods = lag)
PPP_betas = foreign[['PPP','rets']].groupby(level = 1).apply(monthly_reg)
eval_factor(PPP_betas)

# Z=scoring the factor scores
foreign['carry_z'] = foreign.carry.groupby(level = 1).transform(z_score)
foreign['mom26_z'] = foreign.mom_26.groupby(level = 1).transform(z_score)
foreign['PPP_z'] = foreign.PPP.groupby(level = 1).transform(z_score)

month = foreign[['rets','carry_z', 'PPP_z', 'mom26_z']].dropna()
month = month.reset_index()
month.columns = ['Currency', 'Date'] + list(month.columns[2:])
dates = np.unique(month.Date.values)
month = month.set_index(['Date', 'Currency'])
month['forecast'] = np.NaN


#===============================================================================
# 3 factor model
#===============================================================================
rolling_multi = pd.DataFrame()
for date in dates:
    window = month.ix[date]
    Y = window.ix[:,0]
    X = window[['carry_z', 'PPP_z', 'mom26_z']]
    X = sm.add_constant(X)
    reg = sm.OLS(Y, X)
    results = reg.fit().params
    day_reg = pd.DataFrame({'carry':results.ix['carry_z'],
                      'PPP':results.ix['PPP_z'],
                      'mom': results.ix['mom26_z']},
                           columns = ['carry','PPP', 'mom'], index = [date])
    if len(rolling_multi) == 0: 
        rolling_multi = day_reg.copy()
    else:
        rolling_multi = rolling_multi.append(day_reg)

rolling_multi = pd.expanding_mean(rolling_multi)
for date in dates:
    month.ix[date,'forecast'] = month.ix[date,1:-1].apply(lambda x: sum(x*rolling_multi.ix[date].values), axis = 1).values
month.forecast = month.forecast.shift()
month = month.dropna()
        
# Raw
strat_rets = month.groupby(level = 0).apply(strat)
eval_factor(strat_rets)

# Continuous condition
Turbulence = fd.get_TI()
TI = Turbulence.cont
condition = rolling_multi.copy()
condition = condition.ix['1996':]
TI.index = condition.index
condition.carry = condition.carry * TI
month2 = month.copy()
for date in dates:
    if date in condition.index:
        month2.ix[date,'forecast'] = month2.ix[date,1:-1].apply(lambda x: sum(x*condition.ix[date].values), axis = 1).values
    else:
        month2.ix[date,'forecast'] = np.NaN
month2 = month2.dropna()
month2.forecast = month2.forecast.shift()
month2 = month2.dropna()
strat2_rets = month2.groupby(level = 0).apply(strat)
eval_factor(strat2_rets)

# Discrete condition
TI = Turbulence.discrete
condition = rolling_multi.copy()
condition = condition.ix['1996':]
TI.index = condition.index
condition.carry = condition.carry * TI
month2 = month.copy()
for date in dates:
    if date in condition.index:
        month2.ix[date,'forecast'] = month2.ix[date,1:-1].apply(lambda x: sum(x*condition.ix[date].values), axis = 1).values
    else:
        month2.ix[date,'forecast'] = np.NaN
month2 = month2.dropna()
month2.forecast = month2.forecast.shift()
month2 = month2.dropna()
strat2_rets = month2.groupby(level = 0).apply(strat)
eval_factor(strat2_rets)




#===============================================================================
# 2 factor model
#===============================================================================
rolling_multi = pd.DataFrame()
for date in dates:
    window = month.ix[date]
    Y = window.ix[:,0]
    X = window[['carry_z', 'PPP_z']]
    X = sm.add_constant(X)
    reg = sm.OLS(Y, X)
    results = reg.fit().params
    day_reg = pd.DataFrame({'carry':results.ix['carry_z'],
                      'PPP':results.ix['PPP_z']},
                           columns = ['carry','PPP'], index = [date])
    if len(rolling_multi) == 0: 
        rolling_multi = day_reg.copy()
    else:
        rolling_multi = rolling_multi.append(day_reg)
rolling_multi = pd.expanding_mean(rolling_multi)
for date in dates:
    month.ix[date,'forecast'] = month.ix[date,1:-2].apply(lambda x: sum(x*rolling_multi.ix[date].values), axis = 1).values
month.forecast = month.forecast.shift()
month = month.dropna()
        
# Raw
strat_rets = month.groupby(level = 0).apply(strat)
eval_factor(strat_rets)

# Continuous condition
Turbulence = fd.get_TI()
TI = Turbulence.cont
condition = rolling_multi.copy()
condition = condition.ix['1996':]
TI.index = condition.index
condition.carry = condition.carry * TI
month2 = month.copy()
for date in dates:
    if date in condition.index:
        month2.ix[date,'forecast'] = month2.ix[date,1:-2].apply(lambda x: sum(x*condition.ix[date].values), axis = 1).values
    else:
        month2.ix[date,'forecast'] = np.NaN
month2 = month2.dropna()
month2.forecast = month2.forecast.shift()
month2 = month2.dropna()
strat2_rets = month2.groupby(level = 0).apply(strat)
eval_factor(strat2_rets)

# Discrete condition
TI = Turbulence.discrete
condition = rolling_multi.copy()
condition = condition.ix['1996':]
TI.index = condition.index
condition.carry = condition.carry * TI
month2 = month.copy()
for date in dates:
    if date in condition.index:
        month2.ix[date,'forecast'] = month2.ix[date,1:-2].apply(lambda x: sum(x*condition.ix[date].values), axis = 1).values
    else:
        month2.ix[date,'forecast'] = np.NaN
month2 = month2.dropna()
month2.forecast = month2.forecast.shift()
month2 = month2.dropna()
strat2_rets = month2.groupby(level = 0).apply(strat)
eval_factor(strat2_rets)





plotPanel(carry_betas)
plotPanel(mom26_betas)
plotPanel(PPP_betas)

