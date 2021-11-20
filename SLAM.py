import numpy as np
import cvxpy as cp
from MDP_sim import MDP_sim
from gridworld_generator import gridworld_generator


class SLAM:
    def __init__(self,ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind_prob,obstacles,rewards,starting_state):
        self.icecream = [0,1]
        self.generator = gridworld_generator(ice_cream_loc_1,ice_cream_loc_2,rows,cols,wind_prob,obstacles,rewards)
        self.MDP, self.rewards = self.generator.generate()
        self.rows = rows
        self.cols = cols
        self.belief = np.ones(rows*cols)
        for i in range(len(self.belief)):
            self.belief[i] = 1/((rows*cols)-len(obstacles))
        self.belief[obstacles] = 0
        self.simulator = MDP_sim(self.MDP,starting_state)
        self.priori = np.zeros(rows*cols)
        self.posteriori = self.belief
        self.actions_taken = []
        self.observations = [self.simulator.observe()]
        
        self.trueState = starting_state
        
        self.fakegenerator = gridworld_generator(self.icecream[0], self.icecream[1], self.rows, self.cols, self.generator.wind, self.generator.obstacle_locations, self.generator.rewards)
        self.fakeMDP, self.fakerewards = self.fakegenerator.generate()
        self.fakesimulator = MDP_sim(self.fakeMDP,self.trueState)
        
    def regenerate(self):
        self.fakegenerator = gridworld_generator(self.icecream[0], self.icecream[1], self.rows, self.cols, self.generator.wind, self.generator.obstacle_locations, self.generator.rewards)
        self.fakeMDP, self.fakerewards = self.fakegenerator.generate()
        self.fakesimulator = MDP_sim(self.fakeMDP,self.trueState)
        
    def localization(self,action):
        
        
        for j in range(self.rows*self.cols):
            sumVal = 0
            for k in range(self.rows*self.cols):
                sumVal += self.generator.transition_probability[(action*self.rows*self.cols*self.rows*self.cols)+(k*self.rows*self.cols)+j]*self.posteriori[k]
            self.priori[j] = sumVal
        
        self.trueState = self.simulator.world_update(action)
        obs = self.fakesimulator.observe()
        self.observations.append(obs)
        eta = 0
        for x in range(self.rows*self.cols):
            
            self.posteriori[x] = self.fakegenerator.observations_probability[(x*len(self.fakegenerator.observations))+obs]*self.priori[x]
            eta += self.fakegenerator.observations_probability[(x*len(self.fakegenerator.observations))+obs]*self.priori[x]
        self.posteriori = self.posteriori/eta
        self.belief = self.posteriori
        
        self.actions_taken.append(action)
    def mapping(self):
        tran_prob = self.generator.transition_probability
        obs_prob = self.generator.observations_probability
        states = cp.Variable(len(self.observations))
        ice_creams = cp.Variable(2)
        objective = cp.Maximize(1)
        for i in range(len(self.observations)-1):
            objective += cp.Maximize(np.log(tran_prob(self.actions_taken[i]*self.rows*self.rows*self.cols*self.cols+states[i]+states[i+1])))
        # for i in len(self.observations):
        #     fake
        constraints = [ice_creams >=0, ice_creams <=self.rows*self.cols-1, states>=0, states <=self.rows*self.cols-1]
        problem =  cp.Problem(objective, constraints)
        problem.solve()
        # self.icecream = ice_creams.value
        print(states.value)
        