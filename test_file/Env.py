from typing import Any, Optional, Tuple, Union

import numpy as np
import gym
from gym import spaces
import pandas as pd
from sklearn import preprocessing
import random

class CIPairWiseEnv(gym.Env):
    def __init__(self, excel):
        super(CIPairWiseEnv, self).__init__()
        
        self.excel = excel
        
        
        self.reward_range = (0,1)
        
        min = excel.min(axis = 0).to_numpy()
        min2 = np.concatenate((min, min))
        max = excel.max(axis = 0).to_numpy()
        max2 = np.concatenate((max, max))
        
        self.observation_space = spaces.Box(low=min2, high=max2)
        self.action_space = spaces.Discrete(2)
        
        
    def reset(self):
        
        self.dict_excel = self.excel.to_dict(orient='records')
        self.arr = self.dict_excel
        
        self.arr = self.arr[:5606]
        self.arr = random.sample(self.arr, 500)
        
        
        
        self.low = 0
        self.high = len(self.arr) - 1
        self.top = -1
        # self.quicksort_stack = []
        
        # print(self.arr)

        
        
        
        # print(self.arr)
        
        size = self.high - self.low + 1
        self.quicksort_stack = [0] * (size)
    
        
        self.top = self.top + 1
        self.quicksort_stack[self.top] = self.low
        self.top = self.top + 1
        self.quicksort_stack[self.top] = self.high
        
        self.smallest_index = ( self.low - 1 )
        
        self.pivot = self.arr[self.high]
        self.pivot_index = self.high
        self.list_counter = self.low
        
        self.done = False
        
        self.observation = self.arr[self.list_counter],  self.pivot
        
<<<<<<< HEAD
        print("loop complete\n")
        
=======
>>>>>>> 2707b6bc818cfaa81c18adc17a9ae50f32620324
        return list(self.arr[self.list_counter].values()) + list(self.pivot.values())
        
        
    def render(self, mode='human'):
        pass
        
        
    def calculate_reward(self):
        ob1 = self.observation[0]
        ob2 = self.observation[1]
        
        if ob1 is None:
            return 0
        
        
        
        if ob1["Verdict"] == ob2["Verdict"]:
            if ob1["Duration"] > ob2["Duration"]:
                return 0.5
            else:
                return 0
        elif ob1["Verdict"] < ob2["Verdict"]:
            return 1
        else:
            return 0
        
        
        
    
        
        
        
    def step(self, action):
        
        done = False
        reward = self.calculate_reward()
                
        if action:
            self.smallest_index = self.smallest_index+1
            self.arr[self.smallest_index],self.arr[self.list_counter] = self.arr[self.list_counter],self.arr[self.smallest_index]
        
        self.list_counter = self.list_counter + 1
        
        if self.list_counter >= self.high:
            self.arr[self.smallest_index+1],self.arr[self.high] = self.arr[self.high],self.arr[self.smallest_index+1]
            self.pivot_index = self.smallest_index + 1
            
            
            if self.pivot_index-1 > self.low:
                self.top = self.top + 1
                self.quicksort_stack[self.top] = self.low
                self.top = self.top + 1
                self.quicksort_stack[self.top] = self.pivot_index - 1
    
            # # If there are elements on right side of pivot,
            # # then push right side to stack
            if self.pivot_index+1 < self.high:
                self.top = self.top + 1
                self.quicksort_stack[self.top] = self.pivot_index + 1
                self.top = self.top + 1
                self.quicksort_stack[self.top] = self.high
                
            if self.top < 0:
                done = True
            
            else:
                self.high = self.quicksort_stack[self.top]
                self.top = self.top - 1
                self.low = self.quicksort_stack[self.top]
                self.top = self.top - 1
                
                self.smallest_index = ( self.low - 1 )
                self.pivot = self.arr[self.high]
                self.list_counter = self.low
                
        # print(self.arr)
        
        
        self.observation = (self.arr[self.list_counter], self.pivot)
        
        # print(list(self.arr[self.list_counter].values()) + list(self.pivot.values()))
        
        return list(self.arr[self.list_counter].values()) + list(self.pivot.values()), reward, done, {}

