# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 19:23:56 2021

@author: vaheg
"""
import numpy as np
import matplotlib.pyplot as plt

class gridworld_value_iteration:
    def __init__(self,policy,value,action,q_fn,prob_mx,rows,cols,gamma):
        self.gamma = gamma
        self.value = value
        self.action = action
        self.prob_mx = prob_mx
        self.rows = rows
        self.cols = cols
        self.reward = q_fn
        self.policy = np.zeros(np.shape(policy))
        
    def iteration(self):
        self.policy = np.zeros(np.shape(self.policy))
        helper = np.copy(self.value)
        for s in range(len(self.policy)):
            potential_values = np.zeros((len(self.action),1))
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
                potential_values[a] = self.reward[reward_offset]+self.gamma*future_state_sum
            helper[s] = np.max(potential_values)
            index = np.argmax(potential_values)
            if(potential_values[4]==helper[s]):
                index = 4
            self.policy[s][index]=1
        self.value = helper
    def full(self,epsilon):
        old_value = np.copy(self.value)
        self.iteration()
        new_value = np.copy(self.value)
        counter = 1
        delta = np.inf
        delta = np.min([delta,np.max(np.abs(old_value-new_value))])
        while(delta>=epsilon):
            old_value = np.copy(self.value)
            self.iteration()
            new_value = np.copy(self.value)
            counter+=1
            delta = np.min([delta,np.max(np.abs(old_value-new_value))])
        self.plot()
        return counter

    def plot(self):
        value_fn = np.reshape(self.value,(self.rows,self.cols))
        fig, ax = plt.subplots()
        plt.imshow(value_fn,cmap='Spectral')
        plt.colorbar(label = 'Value at State', orientation = 'vertical')
        ax.set_xticks(list(range(self.cols)))
        ax.set_yticks(list(range(self.rows)))
        counter = 0
        for i in range(self.rows):
            for j in range(self.cols):
               ax.text(j,i,str(round(self.value[counter], 2)), ha='center', va='center')
               counter+=1
        
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