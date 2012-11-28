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

emafxData = fxData.groupby(level = 0).SPOT.apply(lambda x: efa(x,0.97,300))
