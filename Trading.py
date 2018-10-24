# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:30:30 2018

@author: Raphael Loo
"""

import numpy as np
import pandas as pd
import MatMath as mm
import Summarystatsv2 as ss
import MaxSharpe as ms

class Portfolio():
    def __init__(self, *, stock_data, datapoints=10, intervals, rf):
        self.numtrades=len(intervals)
        for i in range(self.numtrades):
            
    
    





#def trade(capital, strategy, tickers, **kwargs)