import constants as const

class Rule(object):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def avaliableActions(self, state):
        raise NotImplementedError
    
    def getActionTypes(self) -> list:
        '''get all actions types
        '''
        raise NotImplementedError

    def getTileTypes(self) -> list:
        '''get all tiles type 
        Returns:

        '''
        raise NotImplementedError
    def getRoundTerminateConditions(self) -> dict:
        '''get one round terminate conditions
        '''
        raise NotImplementedError

    def isRoundTerminate(self, state) -> bool:
        raise NotImplementedError

    def isGameTerminate(self, state, roundState) -> bool:
        raise NotImplementedError


#class JPMahjongRule(Rule):
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#    
#    def getActionTypes(self):
#        return const.JP_OUT_TURN_ACTION_LIST +const.JP_TURN_ACTION_LIST