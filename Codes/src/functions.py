'''
Created on Nov 24, 2012

@author: alex
'''
import pandas as pd
from scipy import stats
import numpy as np

def monthly_reg(month):
    if all(month.ix[:,0].map(np.isnan)): 
        return np.NaN
    else:
        month = month.dropna()
        X = month.ix[:,0] * 100.0
        Y = month.ix[:,1] * 100.0
        return stats.linregress(X,Y)[0]

def eval_factor(betas):    
    alpha = betas.mean()*12
    sigma = betas.std()*np.sqrt(12)
    sharpe = alpha/sigma
    t_stat = betas.mean()/betas.std()*np.sqrt(len(betas))
    return {'alpha':alpha,
            'sigma':sigma,
            'sharpe':sharpe,
            't-stat':t_stat}

#return the exponentially weighted moving average
def efa(x,p,wlen):
    wlen=int(wlen)
    weighting=np.arange(float(wlen))
    for i in range(wlen):
        weighting[i]=pow(p,i+1)
    sums=sum(weighting)
    weighting/=sums
    data=np.zeros(len(x))
    for i in range(wlen-1,len(x)):
        for j in range(wlen):
            data[i]+=float(weighting[j]*x[i-wlen+1+j])
    return data

