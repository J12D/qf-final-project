from numpy import *
import pandas as pd
import scipy as stats

#return the exponentially weighted moving average
def efa(x,p,wlen):
    wlen=int(wlen)
    weighting=arange(float(wlen))
    for i in range(wlen):
        weighting[i]=pow(p,i+1)
    sums=sum(weighting)
    weighting/=sums
    data=zeros(len(x))
    for i in range(wlen-1,len(x)):
        for j in range(wlen):
            data[i]+=float(weighting[j]*x[i-wlen+1+j])
    return data

efa(arange(1000.0),0.97,260)
