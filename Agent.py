import numpy as np
import pandas as pd
import os
# import Rule

class Agent(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self._rule = Rule() # Maj rule
            
    def act(self):
        raise NotImplementedError

ROOT_PATH = 'E:/MAJ/pandas_obj.zip'

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # possible action list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        if(os.path.exists(ROOT_PATH)):
            self.q_table = pd.read_pickle(ROOT_PATH)
            print('qtable loaded')
        else:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
            print('qtable renew')

    def choose_action(self,observation,pact):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            dd = state_action[ lambda x: x.index.isin(pact) ]
            di = dd[dd == np.max(dd)].index
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(di)
        else:
            # choose random action
            action = np.random.choice(pact)
        return action

    def _action(self):
        # action = None
        # while not self._rule.avaliableActions(self, action):
        pass

    def learn(self, s, a, r, s_):
        print('\r{}, Action:{}, Reward:{}'.format(s_,a,r), end='')
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def save(self):
        self.q_table.to_pickle(ROOT_PATH)
        print('qtable saved')