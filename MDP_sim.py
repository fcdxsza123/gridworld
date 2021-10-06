# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:13:22 2021

@author: vaheg
"""

import numpy as np
import pandas as pd

class MDP_sim:
    def __init__(self):
        df = pd.read_csv('input.csv')
        
        self.action = df.action.dropna()
        self.state = df.state.dropna()
        self.obs = df.observation.dropna()
        self.obs_prob = df.observation_probability.dropna()
        self.tran_prob = df.transition_probability.dropna()
        self.current_state = input("Current State of Actor:")
        
    def get_action(self):
        print("List of possible actions:")
        print(self.action)
        act = input("Index of Action to take:")
        return act
    
    def world_update(self,act):
        randVal = np.random.random()
        #offsets for tran_prob are as follows: biggest chunks are based on actions, subchunk on starting state, thats the matrix of interest
        offset = int(act) #gives index of action, i.e. desired big chunk
        offset_index = int(len(self.tran_prob)/len(self.action))
        start_index = int(offset*offset_index)
        #okay we have where to start, next we need to go the point for the current state
        start_index+=int(self.current_state)*len(self.state)
        prob_mx = np.copy(self.tran_prob[start_index:start_index+len(self.state)])
        possible_state = np.where(prob_mx>0)
        newState = 100
        for i in range(len(possible_state[0])):
            prob = prob_mx[possible_state[0][i]]
            if(randVal<prob):
                newState = possible_state[0][i]
                break
            else:
                randVal-=prob_mx[possible_state[0][i]]
        #calculate observation
        obs_index =  len(self.obs)*newState
        obs_prob_mx = np.copy(self.obs_prob[obs_index:obs_index+len(self.obs)])
        randVal = np.random.random()
        possible_obs = np.where(obs_prob_mx>0)
        for i in range(len(possible_obs[0])):
            prob = obs_prob_mx[possible_obs[0][i]]
            if(randVal<prob):
                observation = possible_obs[0][i]
                break
            else:
                randVal-=obs_prob_mx[possible_obs[0][i]]        
        self.current_state = newState
        return newState, observation
    
# sim = MDP_sim()
# while(True):
#     act = sim.get_action()
#     current_state, observation = sim.world_update(act)
#     print("New State:")
#     print(sim.state[current_state])
#     print("Observation there:")
#     print(observation)