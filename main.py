from Environment import Environment
from Rule import Rule
from DQN import DeepQNetwork

def main():
    step = 0
    for episode in range(300):
        # initial observation
        observation = env.newgame()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

    # end of game
    print('game over')
    # env.destroy()

if __name__ == "__main__":
    env = Environment(rule=Rule())
    RL = DeepQNetwork(list(range(41)), 2,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    main()
    RL.plot_cost()