# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 13:30:33 2021

@author: vaheg
"""

import pandas as pd
import numpy as np
#num of actions in order: up right down left stay
df = pd.read_csv('rewards.csv')
rewards = df['reward at state']
rewards_at_transition = np.zeros(len(rewards)*5)
counter = 0
for s in range(len(rewards)):
    for a in range(5):
        if(not(s==6 or s ==7 or s ==16 or s==17)):
            if(a == 0):
                if(s+5>=25):
                     rewards_at_transition[counter] = rewards[s]
                else:
                     rewards_at_transition[counter] = rewards[s+5]
            elif(a==1):
                if(s%5==4):
                    rewards_at_transition[counter] = rewards[s]
                else:
                     rewards_at_transition[counter] = rewards[s+1]
            elif(a==2):
                if(s-5<0):
                     rewards_at_transition[counter] = rewards[s]
                else:
                     rewards_at_transition[counter] = rewards[s-5]
            elif(a==3):
                if(s%5==0):
                    rewards_at_transition[counter] = rewards[s]
                else:
                     rewards_at_transition[counter] = rewards[s-1]
            elif(a==4):
                rewards_at_transition[counter] = rewards[s]
        else:
            rewards_at_transition[counter] = 0
        counter+=1
dfsave = pd.DataFrame(rewards_at_transition)
dfsave.columns = ['transition rewards']
filepath = 'rewards_at_transition.csv'
dfsave.to_csv(filepath, index=False)     

