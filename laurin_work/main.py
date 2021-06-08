# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:59:44 2021

@author: LK
"""

import bt
import talib
import numpy as np
import pandas as pd

#import Strategies
import Strategies
""" 

Test Several Strategies



# Specify which data to import

assets = ['BTC-USD', 'MIOTA-USD', 'ADA-USD', 'ETH-USD']
beginning = '01-01-2020'
ending = '06-01-2021'

# Import Data
data = bt.get(assets,start=beginning,end=ending)

# Define Weights
#weights = {'BTC-USD':0.5, 'MIOTA-USD':0.2,'ADA-USD':0.1,'ETH-USD':0.2}

benchmark = Strategies.hodl(assets)
sma_10 = Strategies.above_sma(assets, sma_per=10, name='sma10')
sma_25 = Strategies.above_sma(assets, sma_per=25, name='sma25')
sma_50 = Strategies.above_sma(assets, sma_per=50, name='sma50')

run_bt = bt.run(benchmark,sma_10,sma_25,sma_50)

# Display results
run_bt.plot()
run_bt.display()
run_bt.plot_security_weights()
"""

"""

Strategy based on own Signals

"""

from methods import get_indicator_signal, plot_bband_dema

#Methods work currently only for one asset at a time
asset = 'BTC-USD'

# Specify
start = '01-01-2019'
end = '31-12-2021'

# BBands
t_bbands = 80
nbdevup = 1
nbdevdn = 1

# DEMA
t_fast = 20
t_slow = 100

# Get Indicators and Signals 
indicators,signals = get_indicator_signal(asset=asset,start=start,end=end,t_fast=t_fast,t_slow=t_slow,t_bbands=t_bbands, nbdevup=nbdevup, nbdevdn=nbdevdn)

# Plot the data
bband_dema_fig = plot_bband_dema(asset=asset,indicators=indicators,signals=signals)

""" 

Buy and Hold

"""

hodl = Strategies.hodl(asset)


""" 

DEMA-Strategy
- Go long if Fast DEMA > Slow DEMA
- Go short if Fast DEMA < Slow DEMA

"""

# Get the target weights of the DEMA Strategy

target_weight = pd.DataFrame(signals['DEMA'])
target_weight.columns = [asset]

# Create DEMA Strategy

dema_crossover = bt.Strategy('DEMA_Crossover', 
                           [bt.algos.WeighTarget(target_weight),
                            bt.algos.Rebalance()],
                           )

#Create and run Backtest

backtest_dema = bt.Backtest(dema_crossover, pd.DataFrame(indicators[asset]))


"""

BBANDS Strategy
- Go long if price goes below Upperband

"""


# Get the target weights of the DEMA Strategy

target_weight = pd.DataFrame(signals['BBAND'])
target_weight.columns = [asset]


bbands = bt.Strategy('BDands_Crossover_Up', 
                           [bt.algos.WeighTarget(target_weight),
                            bt.algos.Rebalance()],
                           )

backtest_bbands = bt.Backtest(bbands, pd.DataFrame(indicators[asset]))



run = bt.run(hodl, backtest_dema,backtest_bbands)
run.plot()
run.display()
run.plot_security_weights()


