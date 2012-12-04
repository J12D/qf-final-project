import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

    fig = plt.figure()

    ax1 = fig.add_subplot(311)
    ax1.set_title('Cumulative Betas')
    cumBetas.plot(style='r',label='Original Beta')
    cumConBetas.plot(style='b', label='Discrete Weights')
    cumDisBetas.plot(style='g', label='Digital Weights')
    plt.legend(loc=2)

    ax2 = fig.add_subplot(312)
    ax2.set_title('Discrete Weights')
    getTIresult.ix[:,1].plot(style='b')
    plt.ylim([0, 1.2])
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])

    ax3 = fig.add_subplot(313)
    ax3.set_title('Digital Weights')
    getTIresult.ix[:,2].plot(style='g')
    plt.ylim([-0.1, 1.1])
    plt.yticks([-0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1])

    fig.tight_layout()
    plt.show()

