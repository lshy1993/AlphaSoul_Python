import random
from Rule import JPMahjongRule
import constants as const

class JPState:
    def __init__(self, agentSize: int, rule: JPMahjongRule, seed=2019):
        self.agentSize = agentSize
        self.seed = seed
        self.rule = rule
        random.seed(seed)

    def resetTurn(self):
        self.handTiles =  [[] for i in range(self.agentSize)]  # 手牌 tiles in hand
        self.riverTiles = [[] for i in range(self.agentSize)]  # 牌河 tiles in river
        self.openTiles =  [[] for i in range(self.agentSize)]  # 副露
        self.montainTiles = [] 
        self.tilesSeries = [(tile, id) for tile, value in self.rule.getTileTypes.items() for i in range(value)]
        random.shuffle(self.tilesSeries)

        for i in range(self.agentSize):
            self.handTiles[i], self.tilesSeries = self.tilesSeries[:13], self.tilesSeries[13:]
        assert len(self.handTiles[0]) == 13

        allMountains, self.tilesSeries = self.tilesSeries[-10:], self.tilesSeries[:-10]
        self.montainTiles = (allMountains[:5], allMountains[5:])
        self.mountainIndicatorId = 0




    def resetGame(self):
        self.wind = 0 # E - S - W - N
        self.roundCount = 0
        self.marks = [25000 for i in range(self.agentSize)] # 分数
        self.resetTurn()


    def getPartialState(self, agentId):
        '''since the global state is not visible to each agent, returns a partial state when required
        '''
        return {
            'tiles': (self.handTiles[agentId], 
                self.riverTiles, 
                self.openTiles,
                self.montainTiles),
            'marks': self.marks,
            'wind': self.wind
        }