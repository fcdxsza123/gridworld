# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:20:25 2021

@author: vaheg
"""
import numpy as np

def evaluation(policy, value_old, action, reward, prob_mx):
    value_new = np.copy(value_old)
    for s in range(len(policy)):
        value_new_current_state = 0
        prob_action = policy(s) #policy contains quadruples
        for a in range(len(action)):
            reward_offset = s*len(action)+a
            offset_index = int(len(prob_mx)/len(action))
            start_index = int(a*offset_index)
            start_index+=int(s)*len(policy)
            prob_mx = np.copy(prob_mx[start_index:start_index+len(policy)])
            possible_state = np.where(prob_mx>0)
            future_state_sum = 0
            for i in range(len(possible_state[0])):
                prob = prob_mx[possible_state[0][i]]
                future_state_sum+=prob*value_old(possible_state[0][i])
            value_new_current_state+=prob_action[a]*(reward(reward_offset)+future_state_sum)
        value_new[s] = value_new_current_state