# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:39:34 2021

@author: vaheg
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

class gridworld_generator:
    def __init__(self, ice_cream_1,ice_cream_2, rows, cols, wind,obstacles,rewards):
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
        policy = np.zeros((len(rewards),5))
        for i in range(len(rewards)):
            # r = [.2,.2,.2,.2,.2]
            r = [1,0,0,0,0]
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
        self.transition_probability = bigboy
        
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
        states = []
        for i in range(self.rows):
            for j in range(self.cols):
                val = '('+str(i)+','+str(j)+')'
                states.append(val)
        df1.state = states
        df2.action = ['up','right','down','left','stay']
        df3.observation = self.observations
        df4.observation_probability=self.observations_probability
        df5.transition_probability = self.transition_probability
        df = pd.concat([df1, df2, df3, df4, df5],axis=1)
        df.to_csv('input.csv',index=False)
        return df
    
    def reward_calculator(self):
        #num of actions in order: up right down left stay
        rewards_at_transition = np.zeros(len(self.rewards)**2*5)
        counter = 0
        for a in range(5):
            for s in range(len(self.rewards)):
                # top = s+self.cols>=self.cols*self.rows or ((s+self.cols) in self.obstacle_locations)
                # rightside = s%self.cols==(self.cols-1) or ((s+1) in self.obstacle_locations)
                # leftside = s%self.cols==0  or ((s-1) in self.obstacle_locations)
                # bottom = s-self.cols<0 or ((s-self.cols) in self.obstacle_locations)
                for s_prime in range(len(self.rewards)):
                    if(not(s in self.obstacle_locations)): # check if current state is an obstacle, if so fill with zeros
                        if(s_prime==s+self.cols):
                            rewards_at_transition[counter] = self.rewards[s+self.cols]
                        elif(s_prime==s+1):
                            rewards_at_transition[counter] = self.rewards[s+1]
                        elif(s_prime==s-self.cols):
                            rewards_at_transition[counter] = self.rewards[s-self.cols]
                        elif(s_prime==s-1):
                            rewards_at_transition[counter] = self.rewards[s-1]
                        elif(s_prime==s):
                            rewards_at_transition[counter] = self.rewards[s]
                        else:
                            rewards_at_transition[counter] = 0
                        # if(a==0 and top):
                        #     rewards_at_transition[counter] = self.rewards[s]
                        # if(a==1 and rightside):
                        #     rewards_at_transition[counter] = self.rewards[s]
                        # if(a==2 and bottom):
                        #     rewards_at_transition[counter] = self.rewards[s]
                        # if(a==3 and leftside):
                        #     rewards_at_transition[counter] = self.rewards[s]
                        if(s_prime in self.obstacle_locations):
                            rewards_at_transition[counter] = 0
                    else:
                        rewards_at_transition[counter] = 0
                    counter+=1
        dfsave = pd.DataFrame(rewards_at_transition)
        dfsave.columns = ['transition rewards']
        filepath = 'rewards_at_transition.csv'
        dfsave.to_csv(filepath, index=False)     
        return rewards_at_transition
    
    def generate(self):
        self.transition_calculator()
        self.observation_calculator()
        MDP = self.create()
        rew = self.reward_calculator()
        return MDP, rew