#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:57:18 2021

@author: andyhsu
"""

from gridworld_generator import gridworld_generator
from MDP_sim import MDP_sim
import numpy as np
rows = 5
cols = 5
ice_cream_loc_1 = 2 # zero indexed
ice_cream_loc_2 = 12 # zero indexed
wind_prob = 0.0
obstacles = [6,7,16,17] # zero indexed
starting_state = 0
gamma = .4
rewards = np.zeros(rows*cols)
counter = 0
# for i in range(rows):
#     for j in range(cols):
#         if(j==cols-1):
#             rewards[counter] = -1
#         counter+=1
        
rewards[ice_cream_loc_1] = 1
rewards[ice_cream_loc_2] = 10
rewards[obstacles] = 0

generator = gridworld_generator(ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind_prob,obstacles,rewards)
generator.plotreward()
generator.plotworld()
MDP, rewards = generator.generate()
simulator = MDP_sim(MDP,starting_state)

belief = np.ones(rows*cols)
for i in range(len(belief)):
    belief[i] = 1/((rows*cols)-len(obstacles))
    
belief[obstacles] = 0
trajectory = [1,1,4]
trueStates = [starting_state,0,0,0]
obs = np.copy(trueStates)
priori = np.zeros(rows*cols)
posteriori = belief

# i is trajectory iterator
# j is belief state iterator
# k is iterator to update each element in belief state (by finding correct transition probability)

for i in range(len(trajectory)):
    
    for j in range(rows*cols):
        sumVal = 0
        for k in range(rows*cols):
            sumVal += generator.transition_probability[(trajectory[i]*rows*cols*rows*cols)+(k*rows*cols)+j]*posteriori[k]
        priori[j] = sumVal
        
    trueStates[i+1] = simulator.world_update(trajectory[i])
    obs[i] = simulator.observe()
    
    eta = 0
    for x in range(rows*cols):
        
        posteriori[x] = generator.observations_probability[(x*len(generator.observations))+obs[i]]*priori[x]
        eta += generator.observations_probability[(x*len(generator.observations))+obs[i]]*priori[x]
    posteriori = posteriori/eta
    belief = posteriori
            
print(belief)
        
    