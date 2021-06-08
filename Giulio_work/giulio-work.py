# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 17:33:31 2021

@author: Giulio Cesare
"""

#Riskfree rate
riskfree =  bt.get('^IRX', start='2018-01-01', end= '2021-06-01')
riskfree_rate = riskfree.mean() / 100
print(riskfree_rate)
type(riskfree_rate)

riskfree_rate = float(riskfree_rate)
type(riskfree_rate)

#Benchmark
btc_data=bt.get('btc-usd ', start='2019-01-01')
long_only_ew = bt.Strategy('Benchmark spy', [bt.algos.RunOnce(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])
test_benchmark = bt.Backtest(long_only_ew, btc_data)
res_benchmark = bt.run(test_benchmark)

#strategies' results and benchmark
res_both=bt.run(test_MA,test_MA2,test_benchmark)
res_both.set_riskfree_rate(riskfree_rate)


res_both.plot()
plt.xlabel('Date')
plt.ylabel('Value')