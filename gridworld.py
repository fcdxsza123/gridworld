# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:32:51 2021

@author: vaheg
"""

import numpy as np
import matplotlib.pyplot as plt
import math

def init():
    rows = input("Enter number of rows:")
    rows = int(rows)
    while(rows<1):
        rows = input("Enter number of rows:")
        rows = int(rows)
        
    cols = input("Enter number of columns:")
    cols = int(cols)
    while(cols<1):
        cols = input("Enter number of columns:")
        cols = int(cols)
        
    while(cols*rows<3):
        print("You need at least 3 spaces!")
        rows = input("Enter number of rows:")
        rows = int(rows)
        while(rows<1):
            rows = input("Enter number of rows:")
            rows = int(rows)
            
        cols = input("Enter number of columns:")
        cols = int(cols)
        while(cols<1):
            cols = input("Enter number of columns:")
            cols = int(cols)
            
    grid = np.zeros((rows,cols))
    print("Starting at (0,0) going upwards to (num rows,num_cols) with columns increasing first, input your map.")
    print("0 represents empty space")
    print("1 represents the player")
    print("2 the ice cream shops")
    print("3 the obstacles")
    print("4 the roads")
    print("You must have 1 player and 2 ice cream shops")
    for i in range(rows):
        for j in range(cols):
            print("0 represents empty space")
            print("1 represents the player")
            print("2 the ice cream shops")
            print("3 the obstacles")
            print("4 the roads")
            print("You must have 1 player and 2 ice cream shops")
            print("Location is (",i,",",j,")")
            grid[i][j] = int(input("Value:"))
            while(grid[i][j]!=0 and grid[i][j]!=1 and grid[i][j]!=2 and grid[i][j]!=3 and grid[i][j]!=4):
                print("invalid input, try again")
                grid[i][j] = int(input("Value:"))
    player_arr = np.where(grid==1)
    shops_arr = np.where(grid==2)
    while(np.size(player_arr)!=2 or np.size(shops_arr)!=4):
        print("Mistake on number of players or ice cream shops, try again!")
        print("Starting at (0,0) going upwards to (num rows,num_cols) with columns increasing first, input your map.")
        print("0 represents empty space")
        print("1 represents the player")
        print("2 the ice cream shops")
        print("3 the obstacles")
        print("4 the roads")
        print("You must have 1 player and 2 ice cream shops")
        for i in range(rows):
            for j in range(cols):
                print("0 represents empty space")
                print("1 represents the player")
                print("2 the ice cream shops")
                print("3 the obstacles")
                print("4 the roads")
                print("You must have 1 player and 2 ice cream shops")
                print("Location is (",i,",",j,")")
                grid[i][j] = int(input("Value:"))
                while(grid[i][j]!=0 and grid[i][j]!=1 and grid[i][j]!=2 and grid[i][j]!=3 and grid[i][j]!=4):
                    print("invalid input, try again")
                    grid[i][j] = int(input("Value:"))
        player_arr = np.where(grid==1)
        shops_arr = np.where(grid==2)
    return grid
    
def getdirection(grid,player_coord,direction,prob_wind):
    val = np.random.random()
    true_dir = direction
    if(val>1-prob_wind):
        print("Heck, the wind got you!")
        val = np.random.random()
        if(direction[0]==0 and direction[1]==0):
            if(val<.25):
                true_dir[0] = 0
                true_dir[1] = 1
            elif (val<.5):
                true_dir[0] = 0
                true_dir[1] = -1
            elif (val<.75):
                true_dir[0] = 1
                true_dir[1] = 0
            else:
                true_dir[0] = -1
                true_dir[1] = 0
        elif(direction[0]==0 and direction[1]==1):
            if(val<.25):
                true_dir[0] = 0
                true_dir[1] = 0
            elif (val<.5):
                true_dir[0] = 0
                true_dir[1] = -1
            elif (val<.75):
                true_dir[0] = 1
                true_dir[1] = 0
            else:
                true_dir[0] = -1
                true_dir[1] = 0
        elif(direction[0]==1 and direction[1]==0):
            if(val<.25):
                true_dir[0] = 0
                true_dir[1] = 0
            elif (val<.5):
                true_dir[0] = 0
                true_dir[1] = -1
            elif (val<.75):
                true_dir[0] = 0
                true_dir[1] = 0
            else:
                true_dir[0] = -1
                true_dir[1] = 0
        elif(direction[0]==0 and direction[1]==-1):
            if(val<.25):
                true_dir[0] = 0
                true_dir[1] = 0
            elif (val<.5):
                true_dir[0] = 0
                true_dir[1] = 0
            elif (val<.75):
                true_dir[0] = 1
                true_dir[1] = 0
            else:
                true_dir[0] = -1
                true_dir[1] = 0
        elif(direction[0]==-1 and direction[1]==0):
            if(val<.25):
                true_dir[0] = 0
                true_dir[1] = 0
            elif (val<.5):
                true_dir[0] = 0
                true_dir[1] = -1
            elif (val<.75):
                true_dir[0] = 1
                true_dir[1] = 0
            else:
                true_dir[0] = 0
                true_dir[1] = 0
    newCoords = [player_coord[0]+true_dir[0],player_coord[1]+true_dir[1]]
    helper = grid.shape
    if(newCoords[0][0]<0 or newCoords[0][0]>=helper[0] or newCoords[1][0]<0 or newCoords[1][0]>=helper[1]):
        true_dir = [0,0]
    return true_dir

def calcH(grid,player_coord):
    shops_arr = np.where(grid==2)
    row_p = player_coord[0][0]
    col_p = player_coord[1][0]
    row_s_1 = shops_arr[0][0]
    col_s_1 = shops_arr[0][1]
    row_s_2 = shops_arr[1][0]
    col_s_2 = shops_arr[1][1]
    sum1 = (row_p-row_s_1)**2
    sum2 = (col_p-col_s_1)**2
    sum3 = (row_p-row_s_2)**2
    sum4 = (col_p-col_s_2)**2
    d1 = math.sqrt(sum1+sum2)
    d2 = math.sqrt(sum3+sum4)
    h = 2/(1/d1+1/d2)
    return h

def calcO(h):
    val = np.random.random()
    h_up = int(h+1)
    h_down = int(h)
    if(val>(h_up-h)):
        return h_up
    else:
        return h_down
def world_update(grid,player_coord,direction,prob_wind):
    direction_true = getdirection(grid,player_coord,direction,prob_wind)
    newSpot = grid[player_coord[0][0]+direction_true[0]][player_coord[1][0]+direction_true[1]]
    new_coord = player_coord
    if(newSpot != 3):
        new_coord[0][0] += direction_true[0]
        new_coord[1][0] += direction_true[1]
    else:
        print("You hit an obstacle! No change in position")
    h = calcH(grid,new_coord)
    o = calcO(h)
    return grid, new_coord, o

grid = init()
player_coord = np.where(grid==1)
grid[player_coord] = 0
gridDisplay = np.copy(grid)
gridDisplay[player_coord] += 10
print(np.flipud(gridDisplay))
print("(",player_coord[0][0],",",player_coord[1][0],")")
while(True):
    row_del = int(input("Direction for rows:"))
    col_del = int(input("Direction for cols:"))
    while(row_del!=0 and col_del!=0 and row_del==col_del):
        row_del = int(input("Direction for rows:"))
        col_del = int(input("Direction for cols:"))
    direction = [row_del,col_del]
    grid, player_coord, obs = world_update(grid,player_coord,direction,0)
    gridDisplay = np.copy(grid)
    gridDisplay[player_coord] += 10
    print(np.flipud(gridDisplay))
    print("(",player_coord[0][0],",",player_coord[1][0],")")
    print("Sensor Observation: ",obs)
