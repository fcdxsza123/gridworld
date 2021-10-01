# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:13:22 2021

@author: vaheg
"""

import numpy as np
import pandas as pd

def init():
    df = pd.read_csv('input.csv')
    
    action = df.action.dropna()
    state = df.state.dropna()
    obs = df.observation.dropna()
    obs_prob = df.observation_probability.dropna()
    tran_prob = df.transition_probability.dropna()
    return state, action, obs, obs_prob, tran_prob
