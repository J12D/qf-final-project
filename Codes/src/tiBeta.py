import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def corrMatrix(carry, mom, value):
    dict = {'Carry' : carry, 'Mom' : mom, 'PPP' : value }
    df = pd.DataFrame(dict)
    return df.corr()

def tiCarryPlot(getTIresult):
    conCarry = getTIresult.ix[:,0]*getTIresult.ix[:,1]
    disCarry = getTIresult.ix[:,0]*getTIresult.ix[:,2]
    cumBetas = np.cumprod(getTIresult.ix[:,0]/100+1)-1
    cumConBetas = np.cumprod(conCarry/100+1)-1
    cumDisBetas = np.cumprod(disCarry/100+1)-1

    pp = PdfPages('ticompare.pdf')
    fig = plt.figure()

    ax1 = fig.add_subplot(211)
    ax1.set_title('Cumulative Betas')
    cumBetas.plot(style='r',label='Original Beta')
    cumConBetas.plot(style='b', label='Continuous Weights')
    cumDisBetas.plot(style='g', label='Digital Weights')
    plt.legend(loc=2)

    ax2 = fig.add_subplot(212)
    ax2.set_title('Weights')
    getTIresult.ix[:,1].plot(style='b', label='Continuous')
    getTIresult.ix[:,2].plot(style='g', label='Digital')
    plt.legend(loc=2)

    fig.tight_layout()
    pp.savefig()
    pp.close()
