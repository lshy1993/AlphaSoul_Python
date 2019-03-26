import random
from Rule import JPMahjongRule
import constants as const

class JPState:

    @property
    def tileStack(self):
        return self._tileStack

    @tileStack.setter
    def tileStack(self, value):
        self._tileStack = value

    def shuffleTileStack(self):
        random.shuffle(self._tileStack)

    def __init__(self, agentSize: int, rule: JPMahjongRule):
        self._agentSize = agentSize
        self._rule = rule

        self.id2tile = [(tile, i) for tile, value in self.rule.getTileTypes.items() for i in range(value)]
        self.tile2id = {tile: self.id2tile.index(tile) for tile in self.id2tile}
        

    def resetTurn(self):
        self._tileStack = list(range(len(self.id2tile))) # 牌堆 represents one turn stack
        self.shuffleTileStack()
        # hand tiles: [tileID]
        self._handTiles =  [[] for i in range(self._agentSize)]  # 手牌 tiles in hand
        # river tiles: [tileID]
        self._riverTiles = [[] for i in range(self._agentSize)]  # 牌河 tiles in river
        # open tiles: [(tileID, tileOpenType)] open type = 
        self._openTiles =  [[] for i in range(self._agentSize)]  # 副露 tiles opened
        self._riichii = {i:-1 for i in range(self._agentSize)}

<<<<<<< HEAD
=======
        for i in range(self._agentSize):
            self._handTiles[i], self._tileStack = self._tileStack[:13], self._tileStack[13:]

        allMountains, self._tileStack = self._tileStack[-10:], self._tileStack[:-10]
        self._montainTiles = (allMountains[:5], allMountains[5:])
        self._mountainIndicatorId = 0

    def getNumericRepresentation(self):
        pass

    def getNumericRepresentationPartial(self, agentId):
        '''i.e. fetures, including:
        handtiles, rivertiles, opentiles, marks, wind
        '''
        pass

>>>>>>> 8be77d6f984c5a3cc56faa39914ab94da221365c
    def resetGame(self):
        self._wind = 0 # E - S - W - N
        self._roundCount = 0
        self._marks = [25000 for i in range(self.agentSize)] # 分数
        self.resetTurn()


    def getPartialState(self, agentId):
        '''since the global state is not visible to each agent, returns a partial state when required
        '''
        return {
            'tiles': (self._handTiles[agentId], 
                self._riverTiles, 
                self._openTiles,
                self._montainTiles
                ),
            'marks': self._marks,
            'wind': self._wind
        }
