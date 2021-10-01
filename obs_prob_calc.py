# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 23:59:47 2021

@author: vaheg
"""
import math

x_1 = 2
y_1 = 0
x_2 = 2
y_2 = 2

obs_1 = []
obs_2 = []

probs_1 = []
probs_2 = []
for i in range(5):
    for j in range(5):
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
final_list = []
for i in range(len(probs_1)):
    if(obs_1[i]==0 and obs_2[i]==0):
        final_list.append(1)
    elif(obs_1[i]==0):
        final_list.append(probs_1[i])
    elif(obs_2[i]==0):
        final_list.append(probs_2[i])
    else:
        final_list.append(0)
        
    if(obs_1[i]==1 and obs_2[i]==1):
        final_list.append(1)
    elif(obs_1[i]==1):
        final_list.append(probs_1[i])
    elif(obs_2[i]==1):
        final_list.append(probs_2[i])
    else:
        final_list.append(0)
        
    if(obs_1[i]==2 and obs_2[i]==2):
        final_list.append(1)
    elif(obs_1[i]==2):
        final_list.append(probs_1[i])
    elif(obs_2[i]==2):
        final_list.append(probs_2[i])
    else:
        final_list.append(0)
        
    if(obs_1[i]==3 and obs_2[i]==3):
        final_list.append(1)
    elif(obs_1[i]==3):
        final_list.append(probs_1[i])
    elif(obs_2[i]==3):
        final_list.append(probs_2[i])
    else:
        final_list.append(0)
        
    if(obs_1[i]==4 and obs_2[i]==4):
        final_list.append(1)
    elif(obs_1[i]==4):
        final_list.append(probs_1[i])
    elif(obs_2[i]==4):
        final_list.append(probs_2[i])
    else:
        final_list.append(0)