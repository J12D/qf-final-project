import pandas as pd
import os
import datetime as dt

#assuming our code is in /Codes/src (or another 2-dir deep structure)
def getRootDir():
    upone = os.path.dirname(os.getcwd())
    root = os.path.dirname(upone)
    return root

def getFxRates():
    os.chdir(getRootDir())
    #import fxSpotRates
    data=pd.read_csv('data/qf-fxSpotRates.csv')
    #convert index into date object
    for i in range(len(data.Index)):
        data.Index[i]=dt.datetime.strptime(data.Index[i],"%Y-%m-%d")
    return data

#uncomment this to test wether the code is working correctly
#print "The root of the project is: "+getRootDir()
#print "FXRates start at date: "+str(getFxRates().Index[0])
