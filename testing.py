# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:23:28 2021

@author: vaheg
"""

from gridworld_generator import gridworld_generator
from MDP_sim import MDP_sim
from gridworld_policy_iteration import gridworld_policy_iteration
from gridworld_value_iteration import gridworld_value_iteration
import numpy as np
epsilon = 0.01
rows = 5
cols = 5
ice_cream_loc_1 = 2 # zero indexed
ice_cream_loc_2 = 12 # zero indexed
wind_prob = 0.1
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

generator = gridworld_generator(ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind_prob,obstacles,rewards)
generator.plotreward()
generator.plotworld()
MDP, Q = generator.generate()
simulator = MDP_sim(MDP,starting_state)
values = np.zeros(len(rewards))
p_iterator = gridworld_policy_iteration(generator.init_policy,values,MDP.action.dropna(),Q,MDP.transition_probability.dropna(),rows,cols,gamma)
print(p_iterator.full(epsilon))
v_iterator = gridworld_value_iteration(generator.init_policy,values,MDP.action.dropna(),Q,MDP.transition_probability.dropna(),rows,cols,gamma)
print(v_iterator.full(epsilon))