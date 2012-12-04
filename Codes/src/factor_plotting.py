#plotting logic
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')
fn.plotPanel(carry_betas,'Carry Betas')
pp.savefig()
fn.plotPanel(mom26_betas,'Momentum Betas')
pp.savefig()

def PPP(df):
    us = US_CPI.copy()
    us['Currency'] = df.index[0][0]
    us = us.set_index(['Currency','Date'])
    return df.SPOT*df.CPI/us.US_CPI

for i in range(6,25,6):
    # Subsetting data into foreign currencies
    foreign = fx_data.ix[fx_data.Currency != 'USD',:]
    foreign = foreign.groupby('Currency').apply(lambda x: x.ix[:,1:].fillna(method = 'ffill',limit = 30 ).asfreq('BM'))
    # Compute monthly returns for each currency
    monthly_rets = lambda x: x.SPOT/x.FRWD_1M.shift() - 1
    foreign['rets'] = foreign[['SPOT','FRWD_1M']].groupby(level='Currency').apply(monthly_rets).values
    # Compute PPP factors
    cpi = fd.get_monthly_CPI()
    foreign_CPI = cpi.ix['AUD' : 'SEK']
    US_CPI = cpi.ix['USD'].CPI
    US_CPI.name = 'US_CPI'
    US_CPI = US_CPI.reset_index() 
    US_CPI = US_CPI.rename(columns = {'index': 'Date'})
    lag = i
    print lag
    foreign_CPI['PPP'] = foreign_CPI.groupby(level='Currency').apply(PPP).values
    foreign = foreign.join(foreign_CPI.PPP)
    foreign.PPP = foreign.PPP.groupby(level = 'Currency').transform(lambda x: -(x/x[0]))
    foreign.PPP = foreign.PPP.groupby(level = 'Currency').shift(periods = lag)
    PPP_betas = foreign[['PPP','rets']].groupby(level = 1).apply(monthly_reg)
    fn.plotPanel(PPP_betas,'PPP '+str(i))
    pp.savefig()
    print eval_factor(PPP_betas)
    
pp.close()


#############


#plotting logic
#from matplotlib.backends.backend_pdf import PdfPages
#pp = PdfPages('multipage.pdf')
#fn.plotPanel(carry_betas,'Carry Betas')
#pp.savefig()
#fn.plotPanel(mom26_betas,'Momentum Betas')
#pp.savefig()

def PPP(df):
    us = US_CPI.copy()
    us['Currency'] = df.index[0][0]
    us = us.set_index(['Currency','Date'])
    return df.SPOT*df.CPI/us.US_CPI

x=[]

for i in range(1,25,1):
    # Subsetting data into foreign currencies
    foreign = fx_data.ix[fx_data.Currency != 'USD',:]
    foreign = foreign.groupby('Currency').apply(lambda x: x.ix[:,1:].fillna(method = 'ffill',limit = 30 ).asfreq('BM'))
    # Compute monthly returns for each currency
    monthly_rets = lambda x: x.SPOT/x.FRWD_1M.shift() - 1
    foreign['rets'] = foreign[['SPOT','FRWD_1M']].groupby(level='Currency').apply(monthly_rets).values
    # Compute PPP factors
    cpi = fd.get_monthly_CPI()
    foreign_CPI = cpi.ix['AUD' : 'SEK']
    US_CPI = cpi.ix['USD'].CPI
    US_CPI.name = 'US_CPI'
    US_CPI = US_CPI.reset_index() 
    US_CPI = US_CPI.rename(columns = {'index': 'Date'})
    lag = i
    print lag
    foreign_CPI['PPP'] = foreign_CPI.groupby(level='Currency').apply(PPP).values
    foreign = foreign.join(foreign_CPI.PPP)
    foreign.PPP = foreign.PPP.groupby(level = 'Currency').transform(lambda x: -(x/x[0]))
    foreign.PPP = foreign.PPP.groupby(level = 'Currency').shift(periods = lag)
    PPP_betas = foreign[['PPP','rets']].groupby(level = 1).apply(monthly_reg)
    x.append(eval_factor(PPP_betas)['t-stat'])
    print eval_factor(PPP_betas)
    
print x

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('t-statistic.pdf')
plt.plot(x)
plt.title('Lagged PPP (months): t-statistic')
pp.savefig()
pp.close()

