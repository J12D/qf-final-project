from numpy import *
# import numpy as np is a better practice - avoid import *
import pandas as pd
import scipy as stats
import foundation as fd
from functions import efa

# will change implementation later -> getFxRates()
fxData=fd.getFxRatesOLD()


efa(fxData,0.97,260)

ema = data.copy()
# You can' use print for this
data.apply(lambda x:print x,axis=0)
emadata=data.apply(lambda x:efa(x,0.97,260),axis=0)
