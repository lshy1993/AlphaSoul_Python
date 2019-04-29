import random
import Rule
import Environment
from tool import PaiMaker
from tool import MianziMaker 

SEED = 2019
def main():
    random.seed(SEED)

    # 牌山生成
    # yama = tool.PaiMaker.GeneratePai()
    # print(yama)
    
    handStack = [ "0p", "5p", "5p", "3p", "5p", "4p", "3m", "4m", "6m", "7m", '5m','5m', '0m' ]
    fuluStack = [ ]
    mopai = "0m"
    mianzi = MianziMaker.GetFuluMianzi(handStack,fuluStack,mopai+'-')
    print(mianzi)




if __name__ == "__main__":
    main()