import constants as const
import numpy as np
import tool

class Rule(object):
    def __init__(self, name):
        super(Rule, self).__init__()
        self._ruleName = name
        # 总牌山
        self.yama = []
        # 玩家手牌
        self.handStack = [[],[],[],[]]
        # 牌河
        self.riverStack = [[],[],[],[]]
        # 鸣牌区域
        self.fuluStack = [[],[],[],[]]
        # 宝牌
        self.bao = []
        self.libao = []
        # 牌山位置指示
        self.yamaPos = 0
        self.yamaLast = 0
        self.baoPos = 0
        # 场风
        self.changfeng = 0
        # 4家各风
        self.playerWind = [0,1,2,3]
        self.playerLizhi = [0,0,0,0]
        self.diyizimo = [True,True,True,True]
        self.yifa = [False,False,False,False]
        # 场棒
        self.changbang = 0
        self.lizhibang = 0
        # 4家得分        
        self.score = [25000,25000,25000,25000]
        # 当前轮到的玩家
        self.curWind = 0
        self.qinjia = 0
        # 单局结束
        self.endSection = False
        # 是否连庄
        self.lianzhuang = False
        # 终庄指示
        self.endGame = False


    def avaliableActions(self, state, agent):
        '''get all possible action of a certain agent
        
        '''
        raise NotImplementedError
    
    def getActionTypes(self, state) -> list:
        '''get all actions types
        Returns:
           list [action_types]
        '''
        reAction = []
        if(self.curWind == state.seat):
            # 自己的回合
            reAction.append(const.JP_TURN_ACTION_LIST.KIRU)
        else:
            # 他人的回合
            reAction.append(const.JP_OUT_TURN_ACTION_LIST)
        return reAction
        #raise NotImplementedError

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
        tmplist = filter(lambda x: True if x else False ,self.playerLizhi)
        if(len(tmplist) == 4):
            return True
        # 荒牌流局
        return (self.yamaPos == self.yamaLast - 14)
      
        raise NotImplementedError

    def isGameTerminate(self, state) -> bool:
        '''check if game terminate, i.e. reset marks
        (e.g. in japanese mahjong, east-south has 8 rounds for one game)

        Requires:
            state 
        Return:
            bool
        '''
        # 结束整个对局
        if (np.min(self.score) < 0):
            # 有人被飞
            print('有人被飞')
            return True
        elif(self.changfeng == 2):
            # 西入时，只要有任何人超过30000 或到4局 即结束
            print('西入判定')
            return (self.qinjia == 3 or np.max(self.score) >= 30000)
        elif(self.changfeng >= 1 and self.qinjia == 3):
            # 南4判定
            print('南4判定')
            if(self.lianzhuang):
                aid = self.playerWind[0]
                print(aid)
                # 连庄 亲家若第一 结束
                return self.score[aid] == np.max(self.score)
            else:
                return np.max(self.score) >= 30000
              
        raise NotImplementedError

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
    
    
