# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:23:28 2021

@author: vaheg
"""

# from gridworld_generator import gridworld_generator
# from MDP_sim import MDP_sim
from SLAM import SLAM
import numpy as np
epsilon = 0.01
rows = 5
cols = 5
ice_cream_loc_1 = 2 # zero indexed
ice_cream_loc_2 = 12 # zero indexed
wind_prob = 0.0
obstacles = [6,7,16,17] # zero indexed
starting_state = 0
gamma = .9
rewards = np.zeros(rows*cols)
counter = 0
for i in range(rows):
    for j in range(cols):
        if(j==cols-1):
            rewards[counter] = -10
        counter+=1
        
rewards[ice_cream_loc_1] = 10
rewards[ice_cream_loc_2] = 1
rewards[obstacles] = 0

slam = SLAM(ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind_prob,obstacles,rewards,starting_state)