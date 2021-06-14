# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:59:44 2021

@author: LK
"""

import bt
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import Strategies

from methods import get_indicator_signal, plot_bband_dema

#Methods work currently only for one asset at a time
asset = 'BTC-USD'

# Specify
training_start = '01-01-2014'
training_end = '31-12-2018'
test_start = '01-01-2019'
test_end = '06-01-2021'

# BBands
t_bbands = 80
nbdevup = 1
nbdevdn = 1


""" 

Buy and Hold

"""

hodl = Strategies.hodl(asset)


""" 

DEMA-Strategy
- Go long if Fast DEMA > Slow DEMA
- Go short if Fast DEMA < Slow DEMA

"""


"""

Optimization of the DEMA Strategy based on Training Data

"""

# Create placeholder for SMAs, CAGR, & Daily Sharpe
results_df = pd.DataFrame(columns = ['t_fast', 't_slow', 
                                     'CAGR', 'Daily_Sharpe','Max_Drawdown'])

# Loop over t_fast and t_slow
for t_fast in np.arange(20,30,5):
    for t_slow in np.arange(110,130,10):
        
        # Get Indicators and Signals 
        indicators,signals = get_indicator_signal(asset=asset,start=training_start,end=training_end,t_fast=t_fast,t_slow=t_slow,t_bbands=t_bbands, nbdevup=nbdevup, nbdevdn=nbdevdn)
        
        # Set Target Weights
        target_weight = pd.DataFrame(signals['DEMA'])
        target_weight.columns = [asset]
        
        # Name Strategy      
        strategy = f'Long_DEMA:{t_fast}_Slow_DEMA:{t_slow}'
        
        # Define Strategy
        dema_crossover = bt.Strategy(strategy, 
                               [bt.algos.WeighTarget(target_weight),
                                bt.algos.Rebalance()],
                               )
        
        
        # Create and run Backtest
        backtest_dema = bt.Backtest(dema_crossover, pd.DataFrame(indicators[asset]))
        result = bt.run(backtest_dema)
        

        # Save some figures into variable for easy access
        CAGR = result.stats.at['cagr', strategy]
        Daily_Sharpe = result.stats.at['daily_sharpe', strategy]
        Max_Drawdown = result.stats.at['max_drawdown', strategy]
        
        # Append the figures we're interested in to our result dataframe
        results_df = results_df.append({'t_fast'    : t_fast.astype(int),
                                       't_slow'     : t_slow.astype(int),
                                       'CAGR'         : CAGR,
                                       'Daily_Sharpe' : Daily_Sharpe,
                                       'Max_Drawdown':Max_Drawdown}, 
                                      ignore_index=True)


# Prepare data for CAGR Heatmap
CAGR = results_df.pivot(index='t_fast', columns='t_slow', values = 'CAGR')

# Plot heatmap of CAGR


# Set figure size
fig, ax = plt.subplots(figsize=(15, 8))

# Plot the heatmap
ax = sns.heatmap(data       = CAGR,            # Data for plot (3 dimensional)
                 annot      = True,            # Annotate with values
                 annot_kws  = {"fontsize":15}, # Size of annotation
                 linewidths = 0.5,             # Size of gridlines
                 cmap       = "inferno")       # Style (viridis, plasma, inferno, magma, cividis)


# Change size of x-axis & y-axis tickmarks
ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize = 16)
ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize = 15)


# Customize labels
ax.set_xlabel("t_slow", fontsize = 20)
ax.set_ylabel("t_fast", fontsize = 20)
ax.set_title("CAGR per DEMA Combination",fontsize = 23)


# Show plot
plt.show()


""" 

Test the optimal parameters with Test Data

"""


# Best strategy in terms of CAGR
index_highest_cagr = results_df['CAGR'].idxmax(5)
print(results_df.loc[[index_highest_cagr]])

# Best strategy in terms of Daily Sharpe
index_highest_sharpe = results_df['Daily_Sharpe'].idxmax(5)
print(results_df.loc[[index_highest_sharpe]])

# Best strategy in terms of Daily Sharpe
index_highest_drawdown = results_df['Max_Drawdown'].idxmax(5)
print(results_df.loc[[index_highest_drawdown]])



# Optimal Parameters
t_fast = int(results_df.loc[[index_highest_cagr],'t_fast'])
t_slow = int(results_df.loc[[index_highest_cagr],'t_slow'])

t_fast = 28
t_slow = 126
t_bbands = 80
nbdevup = 0.8
nbdevdn = 1


training_start = '01-01-2014'
training_end = '31-12-2018'

test_start = '01-01-2018'
test_end = '06-01-2021'

# Get Indicators and Signals 
indicators,signals = get_indicator_signal(asset=asset,start=training_start,end=training_end,t_fast=t_fast,t_slow=t_slow,t_bbands=t_bbands, nbdevup=nbdevup, nbdevdn=nbdevdn)

# Plot the data
bband_dema_fig = plot_bband_dema(asset=asset,indicators=indicators,signals=signals)

# Get the target weights of the DEMA Strategy

target_weight = pd.DataFrame(signals['DEMA'])
target_weight.columns = [asset]

# Create DEMA Strategy

dema_crossover = bt.Strategy('Optimized_DEMA_Crossover', 
                           [bt.algos.WeighTarget(target_weight),
                            bt.algos.Rebalance()],
                           )

#Create and run Backtest

backtest_dema = bt.Backtest(dema_crossover, pd.DataFrame(indicators[asset]))

run = bt.run(backtest_dema)
run.plot()
run.display()
run.plot_security_weights()



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



run = bt.run(hodl,backtest_dema,backtest_bbands)
run.plot()
run.display()
run.plot_security_weights()

run.stats.loc['total_return']










