# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:17:19 2021

@author: LK
"""

import bt
import talib
import numpy as np
import pandas as pd

from methods import get_indicator_signal

# Buy and Hodl Strategy
def hodl(tickers, start='01.01.2018', name='HODL'):
    s = bt.Strategy('HODL',[bt.algos.RunOnce(),
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
    data = bt.get(tickers,start=start)
    return bt.Backtest(s,data)


def above_sma(tickers, sma_per=50, start='01.01.2018', name='above_sma'):
    """
    Long securities that are above their n period
    Simple Moving Averages with equal weights.
    """
    # download data
    data = bt.get(tickers, start=start)
    # calc sma
    sma = data.rolling(sma_per).mean()

    # create strategy
    s = bt.Strategy(name, [bt.algos.RunWeekly(),
                           bt.algos.SelectWhere(data > sma),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])

    # now we create the backtest
    return bt.Backtest(s, data)








