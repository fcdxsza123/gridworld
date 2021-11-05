#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:57:18 2021

@author: andyhsu
"""

from gridworld_generator import gridworld_generator
from MDP_sim import MDP_sim
import numpy as np
rows = 3
cols = 3
ice_cream_loc_1 = 4 # zero indexed
ice_cream_loc_2 = 6 # zero indexed
wind_prob = 0.1
obstacles = [] # zero indexed
starting_state = 0
gamma = .4
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
MDP, rewards = generator.generate()
simulator = MDP_sim(MDP,starting_state)

belief = np.ones(rows*cols)
for i in range(len(belief)):
    belief[i] = 1/(rows*cols)
    
trajectory = [0,0,0,0,0,0,0,0,0,0]
obs = [1,1,2,2,2,2,2,2,2,2]

priori = np.zeros(rows*cols)
posteriori = belief

# i is trajectory iterator
# j is belief state iterator
# k is iterator to update each element in belief state (by finding correct transition probability)

for i in range(len(trajectory)):
    for j in range(rows*cols):
        sum = 0
        for k in range(rows*cols):
            sum += generator.transition_probability[(trajectory[i]*rows*cols*rows*cols)+(k*rows*cols)+j]*posteriori[k]
        priori[j] = sum
    eta = 0
    for x in range(rows*cols):
        posteriori[x] = generator.observations_probability[(x*len(generator.observations))+obs[i]]*priori[x]
        eta += generator.observations_probability[(x*len(generator.observations))+obs[i]]*priori[x]
    posteriori = posteriori/eta
    belief = posteriori
    
            
        
        
    