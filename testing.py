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
rewards = [0,0,1,0,-1,0,0,0,0,-1,0,0,10,0,-1,0,0,0,0,-1,0,0,0,0,-1]
generator = gridworld_generator(2,12,5,5,.1,[6,7,16,17],rewards)
MDP, Q = generator.generate()
simulator = MDP_sim(MDP,0)
values = np.zeros(len(rewards))
iterator = gridworld_policy_iteration(generator.init_policy,values,MDP.action.dropna(),Q,MDP.transition_probability.dropna(),5,5,1)
old_value = iterator.value
iterator.evaluation()
new_value = iterator.value
counter = 0
print(counter)
for i in range(10):
    old_value = new_value
    iterator.iterate()
    iterator.evaluation()
    new_value = iterator.value
    counter+=1
    print(counter)

iterator.plot()