import numpy as np
import pandas as pd
import scipy as stats
import foundation as fd
from functions import efa

# will change implementation later -> getFxRates()
#fxData=fd.getFxRatesOLD()

fxData=fd.getFxRates()
foreign = fxData[fxData.Currency!='USD']
foreign = fxData.reset_index()
foreign = foreign[['Date','Currency', 'SPOT']].set_index(['Currency','Date'])
foreign = foreign.groupby(level = 0).apply(lambda x: x.fillna(method = 'ffill',limit = 30 ))
#This breaks
#fxData.groupby('Currency').SPOT.apply(lambda x: efa(x,0.97,260))

#This works
efa(foreign.ix['AUD'].values,0.97,300)

#This doesn't
efa(fxData.ix['CAD'].values,0.97,300)
#ema = data.copy()
# You can' use print for this
#data.apply(lambda x:print x,axis=0)
#emadata=data.apply(lambda x:efa(x,0.97,260),axis=0)
