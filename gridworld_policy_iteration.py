# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:20:25 2021

@author: vaheg
"""
import numpy as np
import matplotlib.pyplot as plt
class gridworld_policy_iteration:
    def __init__(self,policy,value,action,q_fn,prob_mx,rows,cols,gamma):
        self.policy = policy 
        self.value = value
        self.action = action
        self.reward = q_fn
        self.prob_mx = prob_mx
        self.rows = rows
        self.cols = cols
        self.gamma = gamma
    def evaluation(self):
        value_new = np.copy(self.value)
        for s in range(len(self.policy)):
            value_new_current_state = 0
            prob_action = self.policy[s] #policy contains quints (each entree is a state)
            for a in range(len(self.action)):
                reward_offset = s*len(self.action)+a #rewards are based on transitions so each state has its own chunk based on actions
                offset_index = int(len(self.prob_mx)/len(self.action))
                start_index = int(a*offset_index)
                start_index+=int(s)*len(self.policy)
                prob_mx_work = np.copy(self.prob_mx[start_index:start_index+len(self.policy)])
                possible_state = np.where(prob_mx_work>0)
                future_state_sum = 0
                for i in range(len(possible_state[0])):
                    prob = prob_mx_work[possible_state[0][i]]
                    future_state_sum+=prob*self.value[possible_state[0][i]]
                value_new_current_state+=prob_action[a]*(self.reward[reward_offset]+self.gamma*future_state_sum)
            value_new[s] = value_new_current_state
        self.value = value_new
    
    def iterate(self):
        policy_new = np.copy(self.policy)
        for s in range(len(self.policy)):
            state_policy = []
            max_val = -1000
            old_index = 0
            for a in range(len(self.action)):
                #num of actions in order: up right down left stay
                state_policy.append(0)
                if(a == 0):
                    if(s+self.cols>=self.rows*self.cols):
                        if(max_val <= self.value[s]):
                            max_val = self.value[s]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                    else:
                        if(max_val <= self.value[s+5]):
                            max_val = self.value[s+5]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                elif(a==1):
                    if(s%self.cols==(self.cols-1)):
                        if(max_val <= self.value[s]):
                            max_val = self.value[s]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                    else:
                        if(max_val <= self.value[s+1]):
                            max_val = self.value[s+1]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                elif(a==2):
                    if(s-self.cols<0):
                        if(max_val <= self.value[s]):
                            max_val = self.value[s]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                    else:
                        if(max_val <= self.value[s-5]):
                            max_val = self.value[s-5]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                elif(a==3):
                    if(s%self.cols==0):
                        if(max_val <= self.value[s]):
                            max_val = self.value[s]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                    else:
                        if(max_val <= self.value[s-1]):
                            max_val = self.value[s-1]
                            state_policy[old_index] = 0
                            state_policy[a] = 1
                            old_index = a
                elif(a==4):
                    if(max_val <= self.value[s]):
                         max_val = self.value[s]
                         state_policy[old_index] = 0
                         state_policy[a] = 1
                         old_index = a
                         
            policy_new[s] = state_policy
        self.policy = policy_new
        
    def plot(self):
        value_fn = np.reshape(self.value,(self.rows,self.cols))
        fig, ax = plt.subplots()
        plt.imshow(value_fn,cmap='Spectral')
        plt.colorbar(label = 'Value at State', orientation = 'vertical')
        ax.set_xticks(list(range(self.cols)))
        ax.set_yticks(list(range(self.rows)))
        plt.gca().invert_yaxis()
        plt.show()

        fig, ax = plt.subplots()
        ax.imshow(np.zeros((self.rows,self.cols)), cmap='binary')
        ax.set_xticks(list(range(self.cols)))
        ax.set_yticks(list(range(self.rows)))
        p = np.chararray((self.rows,self.cols),unicode=True)
        counter = 0
        for i in range(self.rows):
            for j in range(self.cols):
                index = np.where(self.policy[counter]==1)
                index = index[0][0]
                if(index==0):
                    p[i][j] ='\u2191'
                if(index==1):
                    p[i][j] = '\u2192'
                if(index==2):
                    p[i][j] = '\u2193'
                if(index==3):
                    p[i][j] = '\u2190'
                if(index==4):
                    p[i][j] = 'x'
                ax.text(j,i,p[i][j], ha='center', va='center')
                counter+=1
        plt.gca().invert_yaxis()
        plt.show()