# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 14:37:16 2021

@author: LK
"""

import bt
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def get_indicator_signal(asset,start='01-01-2020',end='31.12.2020',t_fast=20,t_slow=45,t_bbands=60,nbdevup=1,nbdevdn=1):
    #Get data
    data = bt.get(asset,start=start,end=end)
    data.columns = [asset]
    
    # Copy Price Data
    indicators = pd.DataFrame(data.loc[:,asset].copy())
    
    # DEMA - Double Exponential Moving Average 
    indicators['Fast_DEMA'] = talib.DEMA(data.loc[:,asset],t_fast)
    indicators['Slow_DEMA'] = talib.DEMA(data.loc[:,asset],t_slow)
    
    #Copy Price Data
    signals = pd.DataFrame(data.loc[:,asset].copy()) 
    
    # Create DEMA Signal
    signals['DEMA'] = 0
    signals.loc[indicators['Fast_DEMA']>indicators['Slow_DEMA'],'DEMA'] = 1   
    signals.loc[indicators['Fast_DEMA']<indicators['Slow_DEMA'],'DEMA'] = -1      
    
    # RSI
    indicators['RSI'] = talib.RSI(data[asset], timeperiod=14)
    
    signals['RSI'] = 0
    signals.loc[indicators['RSI']>70,'RSI'] = 1
    signals.loc[indicators['RSI']<30,'RSI'] = -1    
    
    # BBANDS
    indicators['Upperband'], indicators['Middleband'], indicators['Lowerband'] = talib.BBANDS(data[asset], timeperiod=t_bbands, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=0)
    
    signals['BBAND'] = 0
    signals.loc[data[asset]>indicators['Upperband'],'BBAND'] = 1
    #signals.loc[data[asset]<indicators['Lowerband'],'BBAND'] = 1  
    
    return indicators, signals


def plot_bband_dema(asset,indicators,signals):
    

    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(16,8), dpi=400, gridspec_kw={'height_ratios':[20,2,8,2]})
    fig.subplots_adjust(hspace=0.8)

    ax1.plot(indicators[asset], linewidth=3, label='Price',color='black')
    #ax1.set_yscale('log')
    ax1.title.set_text('Price with Bollinger Bands')
    # Add BBANDS to subplot
    ax1.plot(indicators['Lowerband'],label='Lowerband',color='green')
    ax1.plot(indicators['Middleband'],label='Middleband')
    ax1.plot(indicators['Upperband'],label='Upperband',color='red')
    ax1.legend()

    ax2.plot(signals['BBAND'],color='midnightblue',linewidth=2)
    ax2.title.set_text('BBAND Signal')

    ax3.plot(indicators['Fast_DEMA'],label='Fast DEMA')
    ax3.plot(indicators['Slow_DEMA'],label='Slow DEMA')
    #ax3.set_yscale('log')
    ax3.title.set_text('Double Exponential Moving Average - DEMA')
    ax3.legend()

    ax4.plot(signals['DEMA'],color='midnightblue',linewidth=2)
    ax4.set_xlim(left=signals.index[0])
    ax4.title.set_text('DEMA Signal')
    
    return fig











