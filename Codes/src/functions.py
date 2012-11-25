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
