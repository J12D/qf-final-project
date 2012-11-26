import pandas as pd
import os
import datetime as dt

#assuming our code is in /Codes/src (or another 2-dir deep structure)
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

def getFxRates():
	fx_data = pd.read_csv('data/full.csv')
	fx_data = fx_data[['Date', 'Currency', 'SPOT']]
	fx_data.SPOT = fx_data.SPOT.replace('\\N', np.NaN).apply(np.float64)
	fx_data.Date = fx_data.Date.map(lambda x: x[:10])
	fx_data.Date = fx_data.Date.map(lambda x: dt.strptime(x, '%Y-%m-%d'))
	return fx_data

#uncomment this to test wether the code is working correctly
#print "The root of the project is: "+getRootDir()
#print "FXRates start at date: "+str(getFxRates().Index[0])
