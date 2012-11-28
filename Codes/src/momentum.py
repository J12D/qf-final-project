from numpy import *
# import numpy as np is a better practice - avoid import *
import pandas as pd
import scipy as stats
import foundation as fd
from functions import efa

# will change implementation later -> getFxRates()
#fxData=fd.getFxRatesOLD()

fxData=fd.getFxRates()
fxData.set_index('Date')
fxData=fxData[fxData.Currency!='USD']
fxData=fxData.groupby('Currency').apply(lambda x: x.ix[:,1:].fillna(method = 'ffill',limit = 30 ))
#This breaks
#fxData.groupby('Currency').SPOT.apply(lambda x: efa(x,0.97,260))

#This works
efa(fxData[fxData.Currency=='AUD']['SPOT'],0.97,300)

#This doesn't
efa(fxData[fxData.Currency=='CAD']['SPOT'],0.97,300)
#ema = data.copy()
# You can' use print for this
#data.apply(lambda x:print x,axis=0)
#emadata=data.apply(lambda x:efa(x,0.97,260),axis=0)
