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
	data=np.copy(x)
	for i in range(wlen-1,len(x)):
		data[i]=np.vdot(weighting,x[i-(wlen-1):i+1])
	return data

def rolling_tstat(x):
    emean=pd.expanding_mean(x)
    estd=pd.expanding_std(x)
    t=np.arange(1,len(x)+1)
    esqr=np.sqrt(t)
    rtstat=(emean/estd)*esqr
    return rtstat

def plotPanel(betaSeries):
    cumbetas=np.cumprod(carry_betas/100+1)-1
    fig=plt.figure()
    ax1 = fig.add_subplot(411)
    ax1.set_title('Carry betas')
    ax1.yaxis.set_major_locator(MaxNLocator(3))
    carry_betas.plot()
    ax2 = fig.add_subplot(412)
    ax2.set_title('Cumulative Carry betas')
    ax2.yaxis.set_major_locator(MaxNLocator(3))
    cumbetas.plot()
    ax3 = fig.add_subplot(413)
    ax3.set_title('Rolling Mean: Carry betas')
    ax3.yaxis.set_major_locator(MaxNLocator(3))
    pd.expanding_mean(carry_betas).plot()
    ax4 = fig.add_subplot(414)
    ax4.set_title('Rolling t-stat: Carry betas')
    ax4.yaxis.set_major_locator(MaxNLocator(3))
    rolling_tstat(carry_betas).plot()
    fig.tight_layout(pad = 1.1)
