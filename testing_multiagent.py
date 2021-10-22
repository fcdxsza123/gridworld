# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:23:28 2021

@author: vaheg
"""

from gridworld_generator_multiagent import gridworld_generator_multiagent
import numpy as np
from gridworld_value_iteration import gridworld_value_iteration

epsilon = 0.01
rows = 3
cols = 3
numAgents = 2
ice_cream_loc_1 = 6 # zero indexed
ice_cream_loc_2 = 12 # zero indexed
wind = 0.1
obstacles = [] # zero indexed
starting_state = 0
gamma = .4
rewards = np.zeros((rows*cols)**numAgents)
counter = 0
for i in range(rows):
    for j in range(cols):
        if(j==cols-1):
            rewards[counter] = -10
        counter+=1
        
rewards[ice_cream_loc_1] = 10
rewards[ice_cream_loc_2] = 1
rewards[obstacles] = 0
values = np.zeros((rows*cols)**numAgents)

generator = gridworld_generator_multiagent(numAgents,ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind,obstacles,rewards)
generator.plotreward()
generator.plotworld()
MDP, R = generator.generate()

v_iterator = gridworld_value_iteration(generator.init_policy,values,MDP.action.dropna(), R, MDP.transition_probability.dropna(),rows,cols,gamma)
print(v_iterator.full(epsilon))              
                    

        
            
                
    
            
