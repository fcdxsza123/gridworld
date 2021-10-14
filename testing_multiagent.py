# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:23:28 2021

@author: vaheg
"""

from gridworld_generator_multiagent import gridworld_generator_multiagent
import numpy as np
import itertools
epsilon = 0.01
rows = 5
cols = 5
numAgents = 3
ice_cream_loc_1 = 2 # zero indexed
ice_cream_loc_2 = 3 # zero indexed
wind = 0.1
obstacles = [] # zero indexed
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

generator = gridworld_generator_multiagent(numAgents,ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind,obstacles,rewards)
generator.plotreward()
generator.plotworld()
MDP, Q = generator.generate()

biggerboy = []
rawpos_list = [*range((rows*cols))]
raw_states = list(itertools.product(rawpos_list,repeat=numAgents))

for i in range(len(generator.actions)):
    for j in range(len(raw_states)):
        stayProbs = []
        upProbs = []
        leftProbs = []
        rightProbs = []
        downProbs = []
        for k in range(numAgents):
            if generator.actions[i][k]==0: #up
                stayProbs.append(wind/4)
                upProbs.append(1-wind)
                rightProbs.append(wind/4)
                downProbs.append(wind/4)
                leftProbs.append(wind/4)
            elif(generator.actions[i][k]==1): #right
                stayProbs.append(wind/4)
                upProbs.append(wind/4)
                rightProbs.append(1-wind)
                downProbs.append(wind/4)
                leftProbs.append(wind/4)
            elif(generator.actions[i][k]==2): #down
                stayProbs.append(wind/4)
                upProbs.append(wind/4)
                rightProbs.append(wind/4)
                downProbs.append(1-wind)
                leftProbs.append(wind/4)
            elif(generator.actions[i][k]==3): #left
                stayProbs.append(wind/4)
                upProbs.append(wind/4)
                rightProbs.append(wind/4)
                downProbs.append(wind/4)
                leftProbs.append(1-wind)
            else:       #stay
                stayProbs.append(1-wind)
                upProbs.append(wind/4)
                rightProbs.append(wind/4)
                downProbs.append(wind/4)
                leftProbs.append(wind/4)
            if(raw_states[j][k]+cols>=cols*rows or ((raw_states[j][k]+cols) in obstacles)):
                stayProbs[k] += upProbs[k]
                upProbs[k] = 0
            if(raw_states[j][k]-cols<0 or ((raw_states[j][k]-cols) in obstacles)):
                stayProbs[k] += downProbs[k]
                downProbs[k] = 0
            if((raw_states[j][k]%cols==(cols-1)) or ((raw_states[j][k]+1) in obstacles)):
                stayProbs[k] += rightProbs[k]
                rightProbs[k] = 0
            if(raw_states[j][k]%cols==0 or ((raw_states[j][k]-1) in obstacles)):
                stayProbs[k] += leftProbs[k]
                leftProbs[k] = 0
        for m in range(len(raw_states)):
            nextProb = 1
            for n in range(numAgents):
                if(not(raw_states[j][n] in obstacles)):
                    if(raw_states[m][n]==raw_states[j][n]+cols):
                        nextProb *= upProbs[n]
                    elif(raw_states[m][n]==raw_states[j][n]+1):
                        nextProb *= rightProbs[n]
                    elif(raw_states[m][n]==raw_states[j][n]-cols):
                        nextProb *= downProbs[n]
                    elif(raw_states[m][n]==raw_states[j][n]-1):
                        nextProb *= leftProbs[n]
                    elif(raw_states[m][n]==raw_states[j][n]):
                        nextProb *= stayProbs[n]
                    else:
                        nextProb = 0
                else:
                    if(generator.actions[i][n]==4 and raw_states[j][n]==raw_states[m][n]):
                        nextProb *= 1
                    else:
                        nextProb = 0
            biggerboy.append(nextProb)
                        
                    

        
            
                
    
            
