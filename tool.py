import re
import math
import random
import constants as const
import copy


class MianziMaker:
    def hong(n, flag):
        if(n != 5):
            return str(n)
        elif(flag):
            return "0"
        return "5"
    hong = staticmethod(hong)

    #const hong = (n)=>{ return n != 5 ? n : bingpai[0] > 0 ? 0 : 5}
    # 是否能吃
    def get_chi_mianzi(pCount, p):
        mianzi = []
        s = p[1]
        n = int(p[0])
        if(n == 0):
            n = 5
        d = p[2]
        bingpai = pCount[s]
        # 上家打牌 and 非字牌
        if (s == 'z' or d != '-'):
            return []
        # 存在红宝时 优先计算红
        # n-2 n-1 n
        if (3 <= n and bingpai[n-2] > 0 and bingpai[n-1] > 0):
            p1 = MianziMaker.hong(n-2, bingpai[0] > 0) + s
            p2 = MianziMaker.hong(n-1, bingpai[0] > 0) + s
            mianzi.append([p1+"|"+p2+"|"+p, 2])
            if(n-2 == 5 and bingpai[5] - bingpai[0] > 0):
                mianzi.append([("5"+s)+"|"+p2+"|"+p, 2])
            if(n-1 == 5 and bingpai[5] - bingpai[0] > 0):
                mianzi.append([p1+"|"+("5"+s)+"|"+p, 2])
        
        # n-1 n n+1
        if (2 <= n and n <= 8 and bingpai[n-1] > 0 and bingpai[n+1] > 0):
            p1 = MianziMaker.hong(n-1, bingpai[0] > 0) + s
            p2 = MianziMaker.hong(n+1, bingpai[0] > 0) + s
            mianzi.append([p1+"|"+p+"|"+p2, 2])
            if(n-1 == 5 and bingpai[5] - bingpai[0] > 0):
                mianzi.append([("5"+s)+"|"+p+"|"+p2, 2])
            if(n+1 == 5 and bingpai[5] - bingpai[0] > 0):
                mianzi.append([p1+"|"+p+"|"+("5"+s), 2])
        
        # n n+1 n+2
        if (n <= 7 and bingpai[n+1] > 0 and bingpai[n+2] > 0):
            p1 = MianziMaker.hong(n+1, bingpai[0] > 0) + s
            p2 = MianziMaker.hong(n+2, bingpai[0] > 0) + s
            mianzi.append([p+"|"+p1+"|"+p2, 2])
            if(n+1 == 5 and bingpai[5]-bingpai[0] > 0):
                mianzi.append([p+"|"+("5"+s)+"|"+p2, 2])
            if(n+2 == 5 and bingpai[5]-bingpai[0] > 0):
                mianzi.append([p+"|"+p1+"|"+("5"+s), 2])

        return mianzi
    get_chi_mianzi = staticmethod(get_chi_mianzi)

    # 是否能碰
    def get_peng_mianzi(pCount,p):
        mianzi = []
        s = p[1]
        n = int(p[0])
        if(n == 0):
            n = 5
        d = p[2]
        bingpai = pCount[s]
        if(d == '_'):
            return mianzi
        # n n n
        if(bingpai[n] >= 2):
            p1 = MianziMaker.hong(n,bingpai[0]>0) + s
            p2 = MianziMaker.hong(n,bingpai[0]>1) + s
            mianzi.append([p1+"|"+p2+"|"+p,3])
            if(n == 5 and bingpai[5] > 2):
                mianzi.append([("5"+s)+"|"+p2+"|"+p,3])
            # if(n == 5 and bingpai[5] > 3):
            #     mianzi.append([("5"+s)+"|"+("5"+s)+"|"+p,3])
        
        return mianzi
    get_peng_mianzi = staticmethod(get_peng_mianzi)

    # 是否能杠
    def get_gang_mianzi(pCount,fulu,p):
        mianzi = []
        s = p[1]
        n = int(p[0])
        if(n == 5):
            n = 5
        shoupai = pCount
        bingpai = shoupai[s]
        # 明杠
        if (bingpai[n] == 3):
            p1 = MianziMaker.hong(n,bingpai[0]>2) + s
            p2 = MianziMaker.hong(n,bingpai[0]>1) + s
            p3 = MianziMaker.hong(n,bingpai[0] > 0) + s
            mianzi.append([p1+"|"+p2+"|"+p3+"|"+p,5])
        # 暗/加杠
        if(p[2] != '_'):
            return mianzi
        for s in shoupai:
            bingpai = shoupai[s]
            for n in range(1,len(bingpai)):
                if (bingpai[n] == 0):
                    next
                if (bingpai[n] == 4):
                    p0 = MianziMaker.hong(n,bingpai[0] > 3) + s
                    p1 = MianziMaker.hong(n,bingpai[0] > 2) + s
                    p2 = MianziMaker.hong(n,bingpai[0] > 1) + s
                    p3 = MianziMaker.hong(n,bingpai[0] > 0) + s
                    mianzi.append([p0+"|"+p1+"|"+p2+"|"+p3,4])
                else:
                    for m in fulu:
                        if (re.sub(r"0","5",m)[0:4] == s+str(n)+str(n)+str(n)):
                            p0 = MianziMaker.hong(n,bingpai[0] > 0) + s
                            mianzi.append([m+"|"+p0,6])

        return mianzi
    get_gang_mianzi = staticmethod(get_gang_mianzi)

    def GetFuluMianzi(handStack,fuluStack,hupai):
        pCount = PaiMaker.GetCount(handStack)
        fulumz = []
        for m in MianziMaker.get_gang_mianzi(pCount,fuluStack,hupai):
            fulumz.append(m)
        
        for m in MianziMaker.get_peng_mianzi(pCount,hupai):
            fulumz.append(m)
        
        for m in MianziMaker.get_chi_mianzi(pCount,hupai):
            fulumz.append(m)
        
        return fulumz
    GetFuluMianzi = staticmethod(GetFuluMianzi)


class PaiMaker:
    # 生成随机牌山
    def GeneratePai():
        resArr = []
        for i in range(136):
            resArr.append(i)
        random.shuffle(resArr)
        # 生成牌
        resList = []
        for p in resArr:
            k = p % 34
            # 初始宝牌设定
            if(p == 4):
                kn = '0m'
            elif(p == 13):
                kn = '0p'
            elif(p == 22):
                kn = '0s'
            else:
                kn = const.JP_TILES_CODE[k]
            resList.append(kn)
        return resList
    GeneratePai = staticmethod(GeneratePai)

    # 统计牌组构成
    def GetCount(plist):
        paiCount = {
            'm': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            's': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'z': [0, 0, 0, 0, 0, 0, 0, 0]
        }
        for p in plist:
            num = int(p[0])
            ch = p[1]
            # print(ch,num)
            if (num == 0):
                # 红宝 同时充当0与5，计算2次
                paiCount[ch][5] += 1
            paiCount[ch][num] += 1
        return paiCount
    GetCount = staticmethod(GetCount)

    # 复制牌统计
    def CopyCount(self,pcount):
        return copy.deepcopy(pcount)
        # newCount = {
        #     m: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     p: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     s: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     z: [0, 0, 0, 0, 0, 0, 0, 0]
        # }
        # for ch in pcount:
        #     newCount[ch] = pcount[ch].concat()
        # return newCount

    # 获取副露后的代码
    def FuluCode(self,mianzi):
        ch = ""
        code = ""
        for p in mianzi.split("|"):
            ch = p[1]
            code += p
        code = re.sub(ch,"",code) # code.replace(new RegExp(ch,"g"),"")
        return ch+code

    # 计算副露后的统计
    def GetFuluOff(self,plist,mianzi):
        newHand = copy.deepcopy(plist)
        if(mianzi[1] == 6):
        # 加杠牌
            mz = [ mianzi[0].split("|")[1] ]
        else:
            mz = mianzi[0].split("|")
        for p in mz:
            ii = newHand.indexOf(p)
            newHand.splice(ii,1)
        return newHand

    # 根据宝牌代码获取真宝牌
    def GetBao(self,baostr):    
        num = baostr[0] - 0 or 5
        ch = baostr[1]
        if (ch == 'z'):
            if (num == 4):
                num = 1
            elif (num == 7):
                num = 5
            else:
                num = num + 1
        else:
            if(num == 9):
                num = 1
            else:
                num = num + 1
        return num+ch
        
    def GetSortPai(self,hand):
        nh = copy.deepcopy(hand)
        nh.sort(self.cmp)
        return nh

    def cmp(self,a,b):
        tv = {"m":0,"p":1,"s":2,"z":3}
        a = a.replace('0','5')
        b = b.replace('0','5')
        if(a[1] == b[1]):
            return a[0] < b[0]
        return tv[a[1]] < tv[b[1]]
