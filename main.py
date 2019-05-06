import random
import Rule
import Environment
from tool import PaiMaker
from tool import MianziMaker
from tool import RonJudger
from tool import TingJudger
from tool import PtJudger
import re

SEED = 2019
def main():
    random.seed(SEED)

    # 牌山生成
    # yama = tool.PaiMaker.GeneratePai()
    # print(yama)

    
    #print(re.fullmatch(r'国','国世无双国'))

    print(re.match(r"[\-\+\=]", '111='))
    print(re.findall(r"[\-\+\=]", '111='))


    handStack = ["1m", "1m", "2m", "2m", "3m", "3m", "4m", "4m", "5m", "5m", "6m", "6m", "7m" ]
    #handStack = [ "1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z" ]
    #handStack = [ "1m", "1m", "9p", "9p" ]
    #fuluStack = [ "z555-", "z666-", "z777=" ]
    fuluStack = []
    mopai = "1m"
    handStack.append(mopai)
    paiCount = PaiMaker.GetCount(handStack)

    #print(RonJudger.MianziDevide(paiCount, fuluStack))
    #print(TingJudger.tingpai(paiCount,fuluStack))

    #mianzi = MianziMaker.GetFuluMianzi(handStack,fuluStack,mopai+'-')
    #print(mianzi)
    #pcount = PaiMaker.GetCount(handStack)

    #print(RonJudger.Ron(handStack,mopai,fuluStack))

    param = {
        'zhuangfeng': 0,
        'menfeng': 0,
        'baopai': ['1z'],
        'fubaopai': [],
        'changbang': 0,
        'lizhibang': 0,
        'lizhi':      0,
        'yifa':       0,
        'qianggang':  False,
        'lingshang':  False,
        'haidi':      0,
        'tianhu':     0
    }
    ptres = PtJudger.GetFen(handStack,fuluStack,mopai+'-',param)
    print(ptres)
    




if __name__ == "__main__":
    main()