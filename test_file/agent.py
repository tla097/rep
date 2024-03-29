
import time
from stable_baselines3.dqn.policies import MlpPolicy
from stable_baselines3 import DQN
from Env import CIPairWiseEnv
import pandas as pd
import numpy as np

path_to_save = "models/new_model5"

class TPPairWiseDQNAgent:

    def train_agent(self, env: CIPairWiseEnv, steps: int, path_to_save_agent: None, base_model=None,
                    callback_class=None, device = 'cpu'):
        env.reset()
        path_to_save = path_to_save_agent
        print("running")
        if not base_model:
            # base_model = DQN(MlpPolicy, env, device='cpu')
            base_model = DQN.load("models/new_model4")
            base_model.set_env(env)
        # check_env(env)
        base_model = base_model.learn(total_timesteps=steps, reset_num_timesteps=False, callback=callback_class)
        if path_to_save:
            base_model.save(path_to_save)
        return base_model
    
    def test_agent(self, env: CIPairWiseEnv, model_path: str, model):
        agent_actions = []
        total_rewards = 0
        num = 0
        path_to_save = model_path
        print("Evaluation of an agent from " + path_to_save)
        model = DQN.load(model_path)
        print("Agent is loaded")
        done = False
        obs = env.reset()
        obs = np.array(obs)
        while True:
            action, _states = model.predict(obs, deterministic=False, device= 'cpu')
            # print(action)
            obs, rewards, done, info = env.step(action)
            obs = np.array(obs)
            total_rewards += rewards
            num +=1 

            if done:
                break
            
        return total_rewards/num

from stable_baselines3.common.callbacks import BaseCallback

class SaveOnBestTrainingRewardCallback(BaseCallback):
    def __init__(self, check_freq: int):
        super(SaveOnBestTrainingRewardCallback, self).__init__(self)
        self.check_freq = check_freq
        self.best_mean_reward = -float("inf")

    def _on_step(self) -> bool:
        curr = time.time() - start_time
        if self.n_calls % self.check_freq == 0:
            
            print("SAVED")
            
            self.model.save(f"{path_to_save}")
            with open(f"models/new_model_time2", "w") as f:
                f.write(f"current modeltime = {curr}\n")
                
        if self.n_calls % (self.check_freq * 10) == 0:
            
            excel = pd.read_csv("my_data_mutual_info3P3.csv")
            column_names = ['last_run', 'my_maturity', 'Cycle', 'GapInRun', 'last_result', 'Month', 'Failure_Percentage', 'times_ran',
                                    'Verdict', 'Duration']
            excel = excel[column_names]
            e = CIPairWiseEnv(excel)
            ag = TPPairWiseDQNAgent()
            
            res = ag.test_agent(e, path_to_save)
            with open("NEW_MODEL_5", "a") as f:
                f.write(f" calls - {self.n_calls} score = {res}\n ")
                
            

        
excel = pd.read_csv("my_data_mutual_info3P3.csv")


column_names = ['last_run', 'my_maturity', 'Cycle', 'GapInRun', 'last_result', 'Month', 'Failure_Percentage', 'times_ran',
                        'Verdict', 'Duration']

excel = excel[column_names]


env = CIPairWiseEnv(excel)
ag = TPPairWiseDQNAgent()

callback = SaveOnBestTrainingRewardCallback(1000)

start_time = time.time()

ag.train_agent(env, 50000000000, path_to_save, callback_class= callback)

# print(ag.test_agent(env, "models/new_model", 0))

# ag.train_agent(env, 500, "models/agent_500_runs")

# better_agent = ""
# better_agent_num = 0
# worse_agent = ""
# worse_agent_num = 0

# for i in range(10):
#     worse_agent = (ag.test_agent(env, "models/agent_500_runs", 0))
#     better_agent = (ag.test_agent(env, "models/agent", 0))
    
#     better_agent_num += better_agent
#     worse_agent_num += worse_agent
    
#     with open("results/worse_agent", "a") as f:
#         f.write(f"{worse_agent}\n")
        
    
#     with open("results/better_agent", "a") as f:
#         f.write(f"{better_agent}\n")

    
    
# with open("results/worse_agent", "a") as f:
#     f.write(worse_agent_num/10)
    
    
# with open("results/better_agent", "a") as f:
#     f.write(f"\n average = {better_agent_num/10}")

    
    


