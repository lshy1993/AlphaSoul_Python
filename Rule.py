import constants as const

class Rule(object):
    def __init__(self, name):
        super(Rule, self).__init__()
        self._ruleName = name

    def avaliableActions(self, state, agent):
        '''get all possible action of a certain agent
        
        '''
        raise NotImplementedError
    
    def getActionTypes(self) -> list:
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
        raise NotImplementedError

    def isGameTerminate(self, state) -> bool:
        '''check if game terminate, i.e. reset marks
        (e.g. in japanese mahjong, east-south has 8 rounds for one game)

        Requires:
            state 
        Return:
            bool
        '''
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
    
    
