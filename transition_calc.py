# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 01:48:31 2021

@author: vaheg
"""
import pandas as pd
#bad coords are 6,7,16,17

p_e = .1
bigboy = []
for i in range(5):      #num of actions in order: up right down left stay
    for j in range(25): #num of states in order (0,0) (0,1) ... (4,4)
        for k in range(25):
            if(i==0): #up
                stayval = p_e/4
                upval = 1-p_e
                rightval = p_e/4
                downval = p_e/4
                leftval = p_e/4
                if(j+5>=25 or j+5==6 or j+5 ==7 or j+5 ==16 or j+5==17):
                    stayval +=1-p_e
                    upval = 0
                if(j-5<=0 or j-5==6 or j-5 ==7 or j-5 ==16 or j-5==17):
                    stayval +=p_e/4
                    downval = 0
                if(j%5==4 or j+1==6 or j+1 ==7 or j+1 ==16 or j+1==17):
                    stayval +=p_e/4
                    rightval = 0
                if(j%5==0 or j-1==6 or j-1 ==7 or j-1 ==16 or j-1==17):
                    stayval +=p_e/4
                    leftval = 0
                if(k==j+5):
                    bigboy.append(upval)
                elif(k==j+1):
                    bigboy.append(rightval)
                elif(k==j-5):
                    bigboy.append(downval)
                elif(k==j-1):
                    bigboy.append(leftval)
                elif(k==j):
                    bigboy.append(stayval)
                else:
                    bigboy.append(0)
            elif(i==1): #right
                stayval = p_e/4
                upval = p_e/4
                rightval = 1-p_e
                downval = p_e/4
                leftval = p_e/4
                if(j+5>=25 or j+5==6 or j+5 ==7 or j+5 ==16 or j+5==17):
                    stayval +=p_e/4
                    upval = 0
                if(j-5<=0 or j-5==6 or j-5 ==7 or j-5 ==16 or j-5==17):
                    stayval +=p_e/4
                    downval = 0
                if(j%5==4 or j+1==6 or j+1 ==7 or j+1 ==16 or j+1==17):
                    stayval +=1-p_e
                    rightval = 0
                if(j%5==0 or j-1==6 or j-1 ==7 or j-1 ==16 or j-1==17):
                    stayval +=p_e/4
                    leftval = 0
                if(k==j+5):
                    bigboy.append(upval)
                elif(k==j+1):
                    bigboy.append(rightval)
                elif(k==j-5):
                    bigboy.append(downval)
                elif(k==j-1):
                    bigboy.append(leftval)
                elif(k==j):
                    bigboy.append(stayval)
                else:
                    bigboy.append(0)
            elif(i==2): #down
                stayval = p_e/4
                upval = p_e/4
                rightval = p_e/4
                downval = 1-p_e
                leftval = p_e/4
                if(j+5>=25 or j+5==6 or j+5 ==7 or j+5 ==16 or j+5==17):
                    stayval +=p_e/4
                    upval = 0
                if(j-5<=0 or j-5==6 or j-5 ==7 or j-5 ==16 or j-5==17):
                    stayval +=1-p_e
                    downval = 0
                if(j%5==4 or j+1==6 or j+1 ==7 or j+1 ==16 or j+1==17):
                    stayval +=p_e/4
                    rightval = 0
                if(j%5==0 or j-1==6 or j-1 ==7 or j-1 ==16 or j-1==17):
                    stayval +=p_e/4
                    leftval = 0
                if(k==j+5):
                    bigboy.append(upval)
                elif(k==j+1):
                    bigboy.append(rightval)
                elif(k==j-5):
                    bigboy.append(downval)
                elif(k==j-1):
                    bigboy.append(leftval)
                elif(k==j):
                    bigboy.append(stayval)
                else:
                    bigboy.append(0)
            elif(i==3): #left
                stayval = p_e/4
                upval = p_e/4
                rightval = p_e/4
                downval = p_e/4
                leftval = 1-p_e
                if(j+5>=25 or j+5==6 or j+5 ==7 or j+5 ==16 or j+5==17):
                    stayval +=p_e/4
                    upval = 0
                if(j-5<=0 or j-5==6 or j-5 ==7 or j-5 ==16 or j-5==17):
                    stayval +=p_e/4
                    downval = 0
                if(j%5==4 or j+1==6 or j+1 ==7 or j+1 ==16 or j+1==17):
                    stayval +=p_e/4
                    rightval = 0
                if(j%5==0 or j-1==6 or j-1 ==7 or j-1 ==16 or j-1==17):
                    stayval +=1-p_e
                    leftval = 0
                if(k==j+5):
                    bigboy.append(upval)
                elif(k==j+1):
                    bigboy.append(rightval)
                elif(k==j-5):
                    bigboy.append(downval)
                elif(k==j-1):
                    bigboy.append(leftval)
                elif(k==j):
                    bigboy.append(stayval)
                else:
                    bigboy.append(0)
            else:       #stay
                stayval = 1-p_e
                upval = p_e/4
                rightval = p_e/4
                downval = p_e/4
                leftval = p_e/4
                if(j+5>=25 or j+5==6 or j+5 ==7 or j+5 ==16 or j+5==17):
                    stayval +=p_e/4
                    upval = 0
                if(j-5<=0 or j-5==6 or j-5 ==7 or j-5 ==16 or j-5==17):
                    stayval +=p_e/4
                    downval = 0
                if(j%5==4 or j+1==6 or j+1 ==7 or j+1 ==16 or j+1==17):
                    stayval +=p_e/4
                    rightval = 0
                if(j%5==0 or j-1==6 or j-1 ==7 or j-1 ==16 or j-1==17):
                    stayval +=p_e/4
                    leftval = 0
                if(k==j+5):
                    bigboy.append(upval)
                elif(k==j+1):
                    bigboy.append(rightval)
                elif(k==j-5):
                    bigboy.append(downval)
                elif(k==j-1):
                    bigboy.append(leftval)
                elif(k==j):
                    bigboy.append(stayval)
                else:
                    bigboy.append(0)
df = pd.DataFrame(bigboy)
filepath = 'transition_probability_monster.xlsx'
df.to_excel(filepath, index=False)