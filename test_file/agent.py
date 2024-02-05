from stable_baselines3.dqn.policies import MlpPolicy
from stable_baselines3 import DQN
from Env import CIPairWiseEnv
import pandas as pd
import numpy as np


class TPPairWiseDQNAgent:

    def train_agent(self, env: CIPairWiseEnv, steps: int, path_to_save_agent: None, base_model=None,
                    callback_class=None):
        env.reset()
        print("running")
        if not base_model:
            base_model = DQN(MlpPolicy, env)
            base_model.set_env(env)
        # check_env(env)
        base_model = base_model.learn(total_timesteps=steps, reset_num_timesteps=False, callback=callback_class)
        if path_to_save_agent:
            base_model.save(path_to_save_agent)
        return base_model
    
    def test_agent(self, env: CIPairWiseEnv, model_path: str, model):
        agent_actions = []
        total_rewards = 0
        num = 0
        print("Evaluation of an agent from " + model_path)
        model = DQN.load(model_path)
        print("Agent is loaded")
        done = False
        obs = env.reset()
        obs = np.array(obs)
        while True:
            action, _states = model.predict(obs, deterministic=False)
            # print(action)
            obs, rewards, done, info = env.step(action)
            obs = np.array(obs)
            total_rewards += rewards
            num +=1 
            
            if done:
                break
            
        return total_rewards/num
        
excel = pd.read_csv("my_data_mutual_info3P3.csv")


column_names = ['last_run', 'my_maturity', 'Cycle', 'GapInRun', 'last_result', 'Month', 'Failure_Percentage', 'times_ran',
                        'Verdict', 'Duration']

excel = excel[column_names]


env = CIPairWiseEnv(excel)
ag = TPPairWiseDQNAgent()

# ag.train_agent(env, 500000, "models/agent")
# ag.train_agent(env, 500, "models/agent_500_runs")

better_agent = ""
better_agent_num = 0
worse_agent = ""
worse_agent_num = 0

for i in range(10):
    worse_agent = (ag.test_agent(env, "models/agent_500_runs", 0))
    better_agent = (ag.test_agent(env, "models/agent", 0))
    
    better_agent_num += better_agent
    worse_agent_num += worse_agent
    
    with open("results/worse_agent", "a") as f:
        f.write(f"{worse_agent}\n")
        
    
    with open("results/better_agent", "a") as f:
        f.write(f"{better_agent}\n")

    
    
with open("results/worse_agent", "a") as f:
    f.write(worse_agent_num/10)
    
    
with open("results/better_agent", "a") as f:
    f.write(f"\n average = {better_agent_num/10}")
    
    


