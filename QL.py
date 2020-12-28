from Environment import Environment
from Rule import Rule
from Agent import QLearningTable
from tool import PaiMaker
import re
import sys
import time
import random

def update():
    for episode in range(5):
        print('episode{} start\n'.format(episode))
        start = time.time()
        # initial observation
        observation = env.newgame()
        # 记录开局后所有state
        statelist = [[],[],[],[]]
        while True:
            # fresh env
            env.render()
            # 可行的操作
            possible = observation.getActions()
            # print(possible)
            # agent 作出的选择
            action = [None,None,None,None]
            # 发回给env的参数
            msgList = [None,None,None,None]
            for k,act in enumerate(possible):
                if act == None or len(act) == 0:
                    continue
                res = Plist(act,observation,k)
                code = PaiMaker.coding(observation,k)
                # RL choose action based on observation
                action[k] = RL.choose_action(code,list(res.keys()))
                # 记录state与action
                statelist[k].append({'state':code,'action':action[k]})
                # msg sender
                msgList[k] = msgBuilder(action[k],k,res)
            #print('act: {}'.format(action))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(msgList)
            #print('reward: {}'.format(reward))
            
            for k,act in enumerate(action):
                if act == None:
                    continue
                code_ = PaiMaker.coding(observation_,k)
                # RL learn from this transition
                RL.learn(code, act, reward[k], code_)

            # swap observation
            observation = observation_

            if env.endSection:
                # 有奖励则将整个过程学习
                for i in range(4):
                    if reward[i] > 0:
                        st = statelist[i]
                        print(st)
                        for k in range(len(st)):
                            state_old = st[k]['state']
                            if(k+1 == len(st)):
                                state_next = 'terminal'
                            else:
                                state_next = st[k+1]['state']
                            act = st[k]['action']
                            RL.learn(state_old,act,reward[i],state_next)
                # 清空
                statelist = [[],[],[],[]]
                break
            
            # break while loop when end of this episode
            if done:
                break
        end = time.time()
        print('episode{} end, time:{:.2f}, total {} game played'.format(episode,end-start,env.pp))
        # 5个episode保存qtable
        #if episode % 5 == 0:
        #RL.save()

    print('train end')
    # env.destroy()

def Plist(act,env,k):
    # 0     -> 取消
    # 1-14  -> 1切牌
    # 15-28 -> 7立直
    # 29-37 -> 2吃 9种可能
    # 38    -> 3碰
    # 39    -> 4暗杠 5明杠 6加杠
    # 40    -> 8自摸 9胡
    # 41    -> 10九种    
    #       -> 拔北
    res = { 0: None }
    for opt in act['operation']:
        if opt['type'] == 1:
            if(0 in res):
                res.pop(0)
            for i,p in enumerate(env.handStack[k]):
                res[i+1] = p
        elif opt['type'] == 7:
            if(0 in res):
                res.pop(0)
            dd = []
            for sub in opt['combination']:
                dd.append(sub['dapai'])
            for i,p in enumerate(env.handStack[k]):
                if(p in dd):
                    res[i+1] = p
        elif opt['type'] == 2:
            ddd = opt['combination'].split('|')
            # print(ddd)
            if(len(ddd[0]) == 3 and ddd[0][2] == '-'):
                if(ddd[1][0] == '0'):
                    res[30] = opt
                elif(ddd[2][0] == '0'):
                    res[31] = opt
                else:
                    res[29] = opt
            elif(len(ddd[1]) == 3 and ddd[1][2] == '-'):
                if(ddd[0][0] == '0'):
                    res[33] = opt
                elif(ddd[2][0] == '0'):
                    res[34] = opt
                else:
                    res[32] = opt
            elif(len(ddd[2]) == 3 and ddd[2][2] == '-'):
                if(ddd[0][0] == '0'):
                    res[36] = opt
                elif(ddd[1][0] == '0'):
                    res[37] = opt
                else:
                    res[35] = opt
            else:
                raise Exception('组合错误')
        elif opt['type'] == 3:
            res[38] = opt 
        elif opt['type'] <= 6:
            res[39] = opt
        elif opt['type'] <= 9:
            res[40] = opt
        elif opt['type'] == 10:
            res[41] = opt
    #print(res)
    return res

def msgBuilder(action,k,opt):
    # 0     -> 取消
    # 1-14  -> 1切牌
    # 15-28 -> 7立直
    # 29-37 -> 2吃 9种可能
    # 38    -> 3碰
    # 39    -> 4暗杠 5明杠 6加杠
    # 40    -> 8自摸 9胡
    # 41    -> 10九种
    # 1切 2吃 3碰 4暗杠 5明杠 6加杠 7立直 8自摸 9胡
    dic = { 'from': k }
    if(action == 0):
        dic['type'] = 'cancel'
    elif(action <= 14):
        hand = env.handStack[k]
        dic['type'] = 'qiepai'
        dic['tile'] = hand[action-1]
    elif(action <= 28):
        hand = env.handStack[k]
        dic['type'] = 'qiepai'
        dic['tile'] = hand[action-1]
        dic['lizhi'] = True
    elif(action <= 37):
        dic['type'] = 'chipenggang'
        combination = opt[action]['combination']
        dic['combination'] = [combination, 2]
    elif(action == 38):
        dic['type'] = 'chipenggang'
        combination = opt[action]['combination']
        dic['combination'] = [combination, 3]
    elif(action == 39):
        t = opt[action]['type']
        if(t == 5):
            dic['type'] = 'chipenggang'
        else:
            dic['type'] = 'angangjiagang'
        combination = opt[action]['combination']
        dic['combination'] = [combination, t]
    elif(action == 40):
        print(opt[action])
        t = opt[action]['type']
        dic['tile'] = opt[action]['combination']
        if(t == 8):
            dic['type'] = 'hu'
        elif(t == 9):
            dic['type'] = 'zimo'
    elif(action == 41):
        pass
    return dic

if __name__ == "__main__":
    vis = False
    print(len(sys.argv))
    if len(sys.argv) > 1:
        # vis = True
        pass
    env = Environment(rule=Rule(),yama=PaiMaker.GeneratePai(1))
    RL = QLearningTable(actions=list(range(41)))
    update()

    # env.after(100, update)
    # env.mainloop()