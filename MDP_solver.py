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
    current_state = input("Current State of Actor:")
    return state, action, obs, obs_prob, tran_prob, current_state

def get_action(actions):
    print("List of possible actions:")
    print(actions)
    act = input("Action to take:")
    return act

def world_update(state,action,obs,obs_prob,tran_prob,current_state,act):
    randVal = np.random.random()
    #offsets for tran_prob are as follows: biggest chunks are based on actions, subchunk on starting state, thats the matrix of interest
    offset = np.where(action==int(act)) #gives index of action, i.e. desired big chunk
    offset_index = len(tran_prob)/len(action)
    start_index = int(offset[0]*offset_index)
    #okay we have where to start, next we need to go the point for the current state
    start_index+=int(current_state)*len(state)
    prob_mx = np.copy(tran_prob[start_index:start_index+len(state)])
    possible_state = np.where(prob_mx>0)
    newState = 100
    for i in range(len(possible_state[0])):
        prob = prob_mx[possible_state[0][i]]
        if(randVal<prob):
            newState = possible_state[0][i]
            break
        else:
            randVal-=prob_mx[possible_state[0][i]]
    # observation = 
    return newState
state,action,obs,obs_prob,tran_prob,current_state = init()
while(True):
    act = get_action(action)
    current_state = world_update(state,action,obs,obs_prob,tran_prob,current_state,act)
    print(current_state)