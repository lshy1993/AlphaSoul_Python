import constants as const
import numpy as np
import tool

class Rule(object):
    def __init__(self):
        super(Rule, self).__init__()
        # self._ruleName = name

    def avaliableActions(self, state, action):
        '''get all possible action of a certain agent
        
        '''
        agent = int(action['from'])
        hand = state.handStack[agent]
        fulu = state.fuluStack[agent]
        print(action)
        print(agent,hand,fulu)
        # 0-13 14吃15碰16杠 17胡18自摸 19取消
        if len(hand) + len(fulu) * 3 == 13:
            # 他人的回合
            return action in [14,15,16,17,19]
        elif len(hand) + len(fulu) * 3 == 14:
            # 自己的回合
            return action in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,16,18]
        else:
            print('手牌数目不符')
            return False
        # raise NotImplementedError
    
    def getActionTypes(self, state) -> list:
        '''get all actions types
        Returns:
           list [action_types]
        '''
        raise NotImplementedError

    def getTileTypes(self) -> dict:
        '''get all tiles type 
        Returns:
            dictionary (tile_type, number) tiles type with number of tiles
        '''
        raise NotImplementedError

    def isRoundTerminate(self, state) -> bool:
        '''check if round is terminates 
        (e.g. in japanese mahjong, east-south has 8 rounds for one game)

        Requires:
            state 
        Return:
            bool
        '''
        # 胡牌/自摸
        
        # 四家立直
        tmplist = filter(lambda x: True if x else False ,state.playerLizhi)
        if(len(tmplist) == 4):
            return True
        # 荒牌流局
        return (state.yamaPos == state.yamaLast - 14)
      
        # raise NotImplementedError

    def isGameTerminate(self, state) -> bool:
        '''check if game terminate, i.e. reset marks
        (e.g. in japanese mahjong, east-south has 8 rounds for one game)

        Requires:
            state 
        Return:
            bool
        '''
        # 结束整个对局
        if (np.min(state.score) < 0):
            # 有人被飞
            print('有人被飞')
            return True
        elif(state.changfeng == 2):
            # 西入时，只要有任何人超过30000 或到4局 即结束
            print('西入判定')
            return (state.qinjia == 3 or np.max(state.score) >= 30000)
        elif(state.changfeng >= 1 and state.qinjia == 3):
            # 南4判定
            print('南4判定')
            if(state.lianzhuang):
                aid = state.playerWind[0]
                print(aid)
                # 连庄 亲家若第一 结束
                return state.score[aid] == np.max(state.score)
            else:
                return np.max(state.score) >= 30000
              
        #raise NotImplementedError

    def initRound(self, state) -> None:
        '''initialize a round, all change update state obj e.g. reset tile mountain

        Requires:
            state 
        '''
        raise NotImplementedError

    def finishRound(self, state) -> None:
        '''finish round and count mark, all change update state obj

        Requires:
            state 
        '''
        raise NotImplementedError
    
    def initGame(self, state) -> None:
        '''init a game, e.g. reset marks, all change update state obj
        Requires:
            state 
        '''
        
        raise NotImplementedError

    def finishGame(self, state) -> None:
        '''finish a game, get the winner. all change update state obj

        Requires:
            state 
        '''
        
        raise NotImplementedError

class JPMahjongRule(Rule):
    def __init__(self):
        super(JPMahjongRule, self).__init__('Japan Mahjong Rule')
    
    def getActionTypes(self):
        return const.JP_ACTION_LIST

    def getTileTypes(self):
        return const.JP_TILES_DICT
    
    
