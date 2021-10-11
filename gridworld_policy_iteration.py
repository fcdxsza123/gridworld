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
    
    def full(self,epsilon):
        old_policy = np.copy(self.policy)
        self.evaluation(epsilon)
        self.iterate()
        new_policy = np.copy(self.policy)
        counter = 1
        # print(counter)
        policy_stable = np.array_equal(old_policy,new_policy)
        while(not policy_stable):
            old_policy = np.copy(self.policy)
            self.evaluation(epsilon)
            self.iterate()
            new_policy = np.copy(self.policy)
            counter+=1
            policy_stable = np.array_equal(old_policy,new_policy)
            # print(counter)
        self.plot()
        return counter
    
    def evaluation(self,epsilon):
        old_value = np.copy(self.value)
        self.evaluate()
        new_value = np.copy(self.value)
        counter = 1
        delta = np.inf
        delta = np.min([delta,np.max(np.abs(old_value-new_value))])
        while(delta>=epsilon):
            old_value = np.copy(self.value)
            self.evaluate()
            new_value = np.copy(self.value)
            counter+=1
            delta = np.min([delta,np.max(np.abs(old_value-new_value))])
        return counter
    
    def evaluate(self):
        helper = np.copy(self.value)
        for s in range(len(self.policy)):
            potential_values = np.zeros((len(self.action),1))
            # if(s==6):
            #     print(s)
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
                potential_values[a] = self.policy[s][a]*(self.reward[reward_offset]+self.gamma*future_state_sum)
            helper[s] = sum(potential_values)
        self.value = helper
        
    def iterate(self):
        policy_new = np.zeros(np.shape(self.policy))
        for s in range(len(policy_new)):
            if(s==3):
                print("wtf")
            store = []
            if(s+self.cols<self.rows*self.cols):
                store.append(self.value[s+self.cols])
            else:
                store.append(np.NINF)
            if(s%self.cols!=(self.cols-1)):
                store.append(self.value[s+1])
            else:
                store.append(np.NINF)
            if(s-self.cols>=0):
                store.append(self.value[s-self.cols])
            else:
                store.append(np.NINF)
            if(s%self.cols!=0):
                store.append(self.value[s-1])
            else:
                store.append(np.NINF)
            store.append(self.value[s])
            policy_value = np.max(store)
            policy_index = np.argmax(store)
            if(store[4] == policy_value):
                policy_index = 4
            policy_new[s][policy_index] = 1
        self.policy = policy_new

        
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