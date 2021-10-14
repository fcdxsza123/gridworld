# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:39:34 2021

@author: vaheg
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import itertools

class gridworld_generator_multiagent:
    def __init__(self,numAgents,ice_cream_1,ice_cream_2, rows, cols, wind,obstacles,rewards):
        self.numAgents = numAgents
        self.ice_cream_1 = ice_cream_1
        self.ice_cream_2 = ice_cream_2
        self.obstacle_locations = obstacles
        self.rows = rows
        self.cols = cols
        self.observations = []
        self.observations_probability = []
        self.transition_probability = []
        self.wind = wind
        self.rewards = rewards
        actions_list = [*range(0,5)]
        self.actions = list(itertools.product(actions_list,repeat=self.numAgents))
        rows_list = [*range(0,self.rows)]
        cols_list = [*range(0,self.cols)]
        pos_list = list(itertools.product(rows_list,cols_list))
        self.states = list(itertools.product(pos_list,repeat=self.numAgents))
        policy = np.zeros((len(rewards),5))
        for i in range(len(rewards)):
            # r = [.2,.2,.2,.2,.2]
            r = [0,0,0,0,1]
            policy[i] = r
        self.init_policy = policy
        
    def plotreward(self):
        fig, ax = plt.subplots()
        ax.imshow(np.zeros((self.rows,self.cols)), cmap='binary')
        ax.set_xticks(list(range(self.cols)))
        ax.set_yticks(list(range(self.rows)))
        counter = 0
        for i in range(self.rows):
            for j in range(self.cols):
                ax.text(j,i,self.rewards[counter], ha='center', va='center')
                counter+=1
        plt.gca().invert_yaxis()
        plt.show()
        
    def plotworld(self):
        fig, ax = plt.subplots()
        ax.imshow(np.zeros((self.rows,self.cols)), cmap='binary')
        ax.set_xticks(list(range(self.cols)))
        ax.set_yticks(list(range(self.rows)))
        counter = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if(counter in self.obstacle_locations):
                    ax.text(j,i,'O', ha='center', va='center')
                elif(counter == self.ice_cream_1 or counter == self.ice_cream_2):
                    ax.text(j,i,'I', ha='center', va='center')
                elif(self.rewards[counter]<0):
                    ax.text(j,i,'R', ha='center', va='center')
                else:
                    ax.text(j,i,'', ha='center', va='center')
                counter+=1
        plt.gca().invert_yaxis()
        plt.show()
        
    def transition_calculator_multiagent(self):
        biggerboy2 = []
        rawpos_list = [*range((self.rows*self.cols))]
        raw_states = list(itertools.product(rawpos_list,repeat=self.numAgents))
        
        for i in range(len(self.actions)):
            for j in range(len(raw_states)):
                stayProbs = []
                upProbs = []
                leftProbs = []
                rightProbs = []
                downProbs = []
                for k in range(self.numAgents):
                    if self.actions[i][k]==0: #up
                        stayProbs.append(self.wind/4)
                        upProbs.append(1-self.wind)
                        rightProbs.append(self.wind/4)
                        downProbs.append(self.wind/4)
                        leftProbs.append(self.wind/4)
                    elif(self.actions[i][k]==1): #right
                        stayProbs.append(self.wind/4)
                        upProbs.append(self.wind/4)
                        rightProbs.append(1-self.wind)
                        downProbs.append(self.wind/4)
                        leftProbs.append(self.wind/4)
                    elif(self.actions[i][k]==2): #down
                        stayProbs.append(self.wind/4)
                        upProbs.append(self.wind/4)
                        rightProbs.append(self.wind/4)
                        downProbs.append(1-self.wind)
                        leftProbs.append(self.wind/4)
                    elif(self.actions[i][k]==3): #left
                        stayProbs.append(self.wind/4)
                        upProbs.append(self.wind/4)
                        rightProbs.append(self.wind/4)
                        downProbs.append(self.wind/4)
                        leftProbs.append(1-self.wind)
                    else:       #stay
                        stayProbs.append(1-self.wind)
                        upProbs.append(self.wind/4)
                        rightProbs.append(self.wind/4)
                        downProbs.append(self.wind/4)
                        leftProbs.append(self.wind/4)
                    if(raw_states[j][k]+self.cols>=self.cols*self.rows or ((raw_states[j][k]+self.cols) in self.obstacle_locations)):
                        stayProbs[k] += upProbs[k]
                        upProbs[k] = 0
                    if(raw_states[j][k]-self.cols<0 or ((raw_states[j][k]-self.cols) in self.obstacle_locations)):
                        stayProbs[k] += downProbs[k]
                        downProbs[k] = 0
                    if((raw_states[j][k]%self.cols==(self.cols-1)) or ((raw_states[j][k]+1) in self.obstacle_locations)):
                        stayProbs[k] += rightProbs[k]
                        rightProbs[k] = 0
                    if(raw_states[j][k]%self.cols==0 or ((raw_states[j][k]-1) in self.obstacle_locations)):
                        stayProbs[k] += leftProbs[k]
                        leftProbs[k] = 0
                for m in range(len(raw_states)):
                    nextProb = 1
                    for n in range(self.numAgents):
                        if(not(raw_states[j][n] in self.obstacle_locations)):
                            if(raw_states[m][n]==raw_states[j][n]+self.cols):
                                nextProb *= upProbs[n]
                            elif(raw_states[m][n]==raw_states[j][n]+1):
                                nextProb *= rightProbs[n]
                            elif(raw_states[m][n]==raw_states[j][n]-self.cols):
                                nextProb *= downProbs[n]
                            elif(raw_states[m][n]==raw_states[j][n]-1):
                                nextProb *= leftProbs[n]
                            elif(raw_states[m][n]==raw_states[j][n]):
                                nextProb *= stayProbs[n]
                            else:
                                nextProb = 0
                        else:
                            if(self.actions[i][n]==4 and raw_states[j][n]==raw_states[m][n]):
                                nextProb *= 1
                            else:
                                nextProb = 0
                    biggerboy2.append(nextProb)
                    
        self.transition_probability = biggerboy2
        
        
        
    def transition_calculator(self):
        bigboy = []
        for i in range(5):      #num of actions in order: up right down left stay
            for j in range(self.rows*self.cols): #num of states in order (0,0) (0,1) ... (4,4)
                if(i==0): #up
                    stayval = self.wind/4
                    upval = 1-self.wind
                    rightval = self.wind/4
                    downval = self.wind/4
                    leftval = self.wind/4
                elif(i==1): #right
                    stayval = self.wind/4
                    upval = self.wind/4
                    rightval = 1-self.wind
                    downval = self.wind/4
                    leftval = self.wind/4
                elif(i==2): #down
                    stayval = self.wind/4
                    upval = self.wind/4
                    rightval = self.wind/4
                    downval = 1-self.wind
                    leftval = self.wind/4
                elif(i==3): #left
                    stayval = self.wind/4
                    upval = self.wind/4
                    rightval = self.wind/4
                    downval = self.wind/4
                    leftval = 1-self.wind
                else:       #stay
                    stayval = 1-self.wind
                    upval = self.wind/4
                    rightval = self.wind/4
                    downval = self.wind/4
                    leftval = self.wind/4
                if(j+self.cols>=self.cols*self.rows or ((j+self.cols) in self.obstacle_locations)):
                    stayval +=upval
                    upval = 0
                if(j-self.cols<0 or ((j-self.cols) in self.obstacle_locations)):
                    stayval +=downval
                    downval = 0
                if((j%self.cols==(self.cols-1)) or ((j+1) in self.obstacle_locations)):
                    stayval +=rightval
                    rightval = 0
                if(j%self.cols==0 or ((j-1) in self.obstacle_locations)):
                    stayval +=leftval
                    leftval = 0
                for k in range(self.rows*self.cols):
                    if(not(j in self.obstacle_locations)):
                        if(k==j+self.cols):
                            bigboy.append(upval)
                        elif(k==j+1):
                            bigboy.append(rightval)
                        elif(k==j-self.cols):
                            bigboy.append(downval)
                        elif(k==j-1):
                            bigboy.append(leftval)
                        elif(k==j):
                            bigboy.append(stayval)
                        else:
                            bigboy.append(0)
                    else:
                        if(i==4 and j==k):
                            bigboy.append(1)
                        else:
                            bigboy.append(0)
        
    def observation_calculator(self):
        x_1 = self.ice_cream_1%self.cols
        y_1 = int(self.ice_cream_1/self.cols)
        x_2 = self.ice_cream_2%self.cols
        y_2 = int(self.ice_cream_2)/self.cols
        
        obs_1 = []
        obs_2 = []
        
        probs_1 = []
        probs_2 = []
        for i in range(self.rows):
            for j in range(self.cols):
                d_1 = math.sqrt((x_1-j)**2+(y_1-i)**2)
                d_2 = math.sqrt((x_2-j)**2+(y_2-i)**2)
                if(d_1!=0 and d_2!=0):
                    h = 2/((1/d_1)+(1/d_2))
                else:
                    h = 0    
                h1 = int(h+1)
                h2 = int(h)
                prob_1 = 1-(h1-h)
                prob_2 = h1-h
                probs_1.append(prob_1)
                probs_2.append(prob_2)
                obs_1.append(h1)
                obs_2.append(h2)
        self.observations = np.unique([obs_1,obs_2])
        
        final_list = []
        for i in range(len(probs_1)):
            for value in self.observations:
                if(obs_1[i]==value and obs_2[i]==value):
                    final_list.append(1)
                elif(obs_1[i]==value):
                    final_list.append(probs_1[i])
                elif(obs_2[i]==value):
                    final_list.append(probs_2[i])
                else:
                    final_list.append(0)
           
        self.observations_probability = final_list
   
    def create(self):
        columns = ['state','action','observation','observation_probability','transition_probability']
        df1 = pd.DataFrame(columns = [columns[0]])
        df2 = pd.DataFrame(columns = [columns[1]])
        df3 = pd.DataFrame(columns = [columns[2]])
        df4 = pd.DataFrame(columns = [columns[3]])
        df5 = pd.DataFrame(columns = [columns[4]])
        df1.state = self.states
        df2.action = self.actions
        df3.observation = self.observations
        df4.observation_probability=self.observations_probability
        df5.transition_probability = self.transition_probability
        df = pd.concat([df1, df2, df3, df4, df5],axis=1)
        #df.to_csv('input.csv',index=False)
        return df
    
    def q_calculator_multiagent(self):
        #num of actions in order: up right down left stay
        rewards_at_transition = np.zeros(len(self.rewards)*5)
        counter = 0
        for s in range(len(self.rewards)):
            for a in range(5):
                if(not(s in self.obstacle_locations)):
                    if(a == 0):
                        if(s+self.cols>=self.cols*self.rows or ((s+self.cols) in self.obstacle_locations)):
                             rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s+self.cols]
                    elif(a==1):
                        if(s%self.cols==(self.cols-1) or ((s+1) in self.obstacle_locations)):
                            rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s+1]
                    elif(a==2):
                        if(s-self.cols<0 or ((s-self.cols) in self.obstacle_locations)):
                             rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s-self.cols]
                    elif(a==3):
                        if(s%self.cols==0  or ((s-1) in self.obstacle_locations)):
                            rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s-1]
                    elif(a==4):
                        rewards_at_transition[counter] = self.rewards[s]
                else:
                    rewards_at_transition[counter] = 0
                counter+=1
        dfsave = pd.DataFrame(rewards_at_transition)
        dfsave.columns = ['transition rewards']
        filepath = 'rewards_at_transition.csv'
        dfsave.to_csv(filepath, index=False)     
        return rewards_at_transition
    
    def q_calculator(self):
        #num of actions in order: up right down left stay
        rewards_at_transition = np.zeros(len(self.rewards)*5)
        counter = 0
        for s in range(len(self.rewards)):
            for a in range(5):
                if(not(s in self.obstacle_locations)):
                    if(a == 0):
                        if(s+self.cols>=self.cols*self.rows or ((s+self.cols) in self.obstacle_locations)):
                             rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s+self.cols]
                    elif(a==1):
                        if(s%self.cols==(self.cols-1) or ((s+1) in self.obstacle_locations)):
                            rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s+1]
                    elif(a==2):
                        if(s-self.cols<0 or ((s-self.cols) in self.obstacle_locations)):
                             rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s-self.cols]
                    elif(a==3):
                        if(s%self.cols==0  or ((s-1) in self.obstacle_locations)):
                            rewards_at_transition[counter] = 0
                        else:
                             rewards_at_transition[counter] = self.rewards[s-1]
                    elif(a==4):
                        rewards_at_transition[counter] = self.rewards[s]
                else:
                    rewards_at_transition[counter] = 0
                counter+=1
        dfsave = pd.DataFrame(rewards_at_transition)
        dfsave.columns = ['transition rewards']
        filepath = 'rewards_at_transition.csv'
        dfsave.to_csv(filepath, index=False)     
        return rewards_at_transition
    
    def generate(self):
        self.transition_calculator_multiagent()
        self.observation_calculator()
        MDP = self.create()
        Q_fn = self.q_calculator()
        return MDP, Q_fn