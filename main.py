import random
import Rule
import Environment
from tool import PaiMaker
from tool import MianziMaker
from tool import RonJudger
from tool import TingJudger

SEED = 2019
def main():
    random.seed(SEED)


    a = [1]
    b = [2]
    c = a
    c.extend(b)
    print(c,a)

    # 牌山生成
    # yama = tool.PaiMaker.GeneratePai()
    # print(yama)
    
    #handStack = ["1m", "1m", "2m", "2m", "3m", "3m", "4m", "4m", "5m", "5m", "6m", "6m", "7m" ]
    handStack = [ "1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z" ]
    fuluStack = [ ]
    mopai = "7z_"
    handStack.append(mopai)
    #mianzi = MianziMaker.GetFuluMianzi(handStack,fuluStack,mopai+'-')
    #print(mianzi)
    

    pcount = PaiMaker.GetCount(handStack)
    # print(pcount)

    #print(RonJudger.MianziPick('m',pcount['m'],1))
    #print(RonJudger.MianziDevide(pcount,fuluStack))
    print(RonJudger.Ron(handStack,mopai,fuluStack))
    




if __name__ == "__main__":
    main()