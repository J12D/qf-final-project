import numpy as np
import pandas as pd
import scipy as stats
import foundation as fd
from functions import efa

# will change implementation later -> getFxRates()
#fxData=fd.getFxRatesOLD()

fxData=fd.getFxRates()
fxData = fxData[fxData.Currency!='USD']
fxData = fxData.reset_index()
fxData = fxData[['Date','Currency', 'SPOT']].set_index(['Currency','Date'])
fxData = fxData.groupby(level = 0).apply(lambda x: x.fillna(method = 'ffill',limit = 30 ))
#This breaks
#fxData.groupby('Currency').SPOT.apply(lambda x: efa(x,0.97,260))

#This works
#print efa(foreign.ix['AUD'].SPOT.values,0.97,300)
print fxData.groupby(level = 0).sum()
print fxData[0:20].SPOT.values
fxData = fxData.groupby(level = 0).SPOT.values.apply(lambda x: efa(x,0.97,300))
print fxData[0:20].SPOT.values
#This doesn't
#efa(fxData.ix['CAD'].values,0.97,300)
#ema = data.copy()
# You can' use print for this
#data.apply(lambda x:print x,axis=0)
#emadata=data.apply(lambda x:efa(x,0.97,260),axis=0)
