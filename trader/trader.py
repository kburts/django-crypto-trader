import time
import numpy as np
#numpy doesn't really want to work on windows + virtualenv

from ticker.models import Pair, Ticker

'''

def movingAverage(data, window):
    """
    Simple moving average algorithm
    Params: data, window
        data format: [(time, price)...]
    """
    out =  []
    data = ([x[1] for x in data]) ## Discard timestamps
    for i in xrange(len(data) - 1):
        v = (sum(data[max(0, i-window):i]))
        v = v / min(window, i+1)
        out.append(v)
    return out
'''
def EMA(values, window):
    """
    Sentdex.com
    Exponential moving average algorithm.
    """
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def movingaverage(values,window):
    """
    Sentdex.com
    moving average algorithm.
    """
    weigths = np.repeat(1.0, window)/window
    #including valid will REQUIRE there to be enough datapoints.
    #for example, if you take out valid, it will start @ point one,
    #not having any prior points, so itll be 1+0+0 = 1 /3 = .3333
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

class SMATrader(object):
    """
    Simple moving average trader class.
    Param: pairPK (eg. 2)
    """
    def __init__(self, pair, timeframe, ema1, ema2):
        self.data = self.getData(pair, timeframe)
        self.indicator1, self.indicator2 = self.analyzePreviousDay(ema1, ema2)
        print self.data
        print self.indicator1
        print self.indicator2
        print len(self.data), len(self.indicator1), len(self.indicator2)


    def getData(self, pair, timeframe):
        timePeriod = time.time() - timeframe
        data = Ticker.objects.filter(pair=pair, timestamp__gt=timePeriod)

        times = []
        prices = []
        for item in data:
            times.append(int(float(item.timestamp))) # times now in integer format.
            prices.append(float(item.price))
        return zip(times, prices)

    def analyzePreviousDay(self, ema1, ema2):
        averagedData1 = EMA(([item[1] for item in self.data]), ema1)
        averagedData2 = EMA(([item[1] for item in self.data]), ema2)
        return averagedData1, averagedData2