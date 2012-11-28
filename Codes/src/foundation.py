import pandas as pd
import os
from datetime import datetime as dt
import numpy as np

# Assuming our code is in /Codes/src (or another 2-dir deep structure). 
# Should only be called once
def getRootDir():
    upone = os.path.dirname(os.getcwd())
    root = os.path.dirname(upone)
    return root

def getFxRatesOLD():
    #import fxSpotRates
    fxfile=os.path.join(getRootDir(),'data/qf-fxSpotRates.csv')
    data=pd.read_csv(fxfile)
    #convert index into date object
    for i in range(len(data.Index)):
        data.Index[i]=dt.datetime.strptime(data.Index[i],"%Y-%m-%d")
    return data

# Should only be called once in the beginning
def getFxRates():
    os.chdir(getRootDir())
    fx_data = pd.read_csv('data/full.csv')
    fx_data.ix[:,2:] = fx_data.ix[:,2:].replace('\\N', np.NaN).apply(np.float64)
    fx_data.Date = fx_data.Date.map(lambda x: x[:10])
    fx_data.Date = fx_data.Date.map(lambda x: dt.strptime(x, '%Y-%m-%d'))
    fx_data = fx_data.set_index('Date')
    return fx_data

#uncomment this to test wether the code is working correctly
#print "The root of the project is: "+getRootDir()
#print "FXRates start at date: "+str(getFxRates().Index[0])
