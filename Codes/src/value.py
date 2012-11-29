import numpy as np
import pandas as pd
import scipy as stats
import foundation as fd

cpiData = fd.get_monthly_CPI();
foreign = cpiData[cpiData.Currency != 'USD']

realFx = lambda x: x.SPOT/x.CPI*cpiData.CPI['USD'].values
foreign['RealFx'] = foreign[['SPOT','CPI']].groupby(level='Currency').apply(realFx).values
foreign['normRealFx'] = foreign['RealFx'].groupby(level='Currency').apply(lambda x: x/x.values[0]).values


