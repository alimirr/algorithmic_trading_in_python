# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 15:14:55 2021

@author: LK
"""

import bt
import pandas as pd

# Buy and Hodl
def hodl_backtest(name='HODL'):
    # Define Strategy
    s = bt.Strategy('HODL',[bt.algos.RunOnce(),
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
    return bt.Backtest(s,pd.DataFrame(indicators[asset]))

