# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:23:28 2021

@author: vaheg
"""

from gridworld_generator import gridworld_generator
from MDP_sim import MDP_sim
import matplotlib.pyplot as plt
from gridworld_policy_iteration import gridworld_policy_iteration
import numpy as np
import pandas as pd

rows = 10
cols = 10
ice_cream_loc_1 = 2 # zero indexed
ice_cream_loc_2 = 12 # zero indexed
wind_prob = .5
obstacles = [6,7,16,17] # zero indexed
# rewards = [0,0,10,0,-1,0,0,0,0,-1,0,0,10,0,-1,0,0,0,0,-1,0,0,0,0,-1]
gamma = .9
rewards = np.zeros(rows*cols)
counter = 0
for i in range(rows):
    for j in range(cols):
        if(j==cols-1):
            rewards[counter] = -10
        counter+=1
        
rewards[ice_cream_loc_1] = 1
rewards[ice_cream_loc_2] = 10        
rewards[obstacles] = 0

generator = gridworld_generator(ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind_prob,obstacles,rewards)
generator.plotreward()
generator.plotworld()
MDP, Q = generator.generate()
simulator = MDP_sim(MDP,0)
values = np.zeros(len(rewards))
iterator = gridworld_policy_iteration(generator.init_policy,values,MDP.action.dropna(),Q,MDP.transition_probability.dropna(),rows,cols,gamma)
old_value = iterator.value
iterator.evaluation()
new_value = iterator.value
counter = 0
print(counter)
for i in range(200):
    old_value = new_value
    iterator.iterate()
    iterator.evaluation()
    new_value = iterator.value
    counter+=1
    print(counter)

iterator.plot()