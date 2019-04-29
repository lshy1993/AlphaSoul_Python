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
        if (p[2] != '_' and bingpai[n] == 3):
            p1 = MianziMaker.hong(n,bingpai[0]>2) + s
            p2 = MianziMaker.hong(n,bingpai[0]>1) + s
            p3 = MianziMaker.hong(n,bingpai[0] > 0) + s
            mianzi.append([p1+"|"+p2+"|"+p3+"|"+p,5])
        # 他人打出牌结束
        if(p[2] != '_'):
            return mianzi
        
        # 加杠
        for m in fulu:
            if (re.sub(r"0","5",m)[0:4] == s+str(n)+str(n)+str(n)):
                p0 = MianziMaker.hong(n,bingpai[0] > 0) + s
                mianzi.append([m+"|"+p0,6])
        
        # 暗杠
        for s in shoupai:
            bingpai = shoupai[s]
            for n in range(1,len(bingpai)):
                if (bingpai[n] == 0):
                    continue
                if (bingpai[n] == 4):
                    p0 = MianziMaker.hong(n,bingpai[0] > 3) + s
                    p1 = MianziMaker.hong(n,bingpai[0] > 2) + s
                    p2 = MianziMaker.hong(n,bingpai[0] > 1) + s
                    p3 = MianziMaker.hong(n,bingpai[0] > 0) + s
                    mianzi.append([p0+"|"+p1+"|"+p2+"|"+p3,4])
                    

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

    def GetCountOff(hand,p):
        newPaiCount = PaiMaker.GetCount(hand)
        ch = p[1]
        num = int(p[0])
        if(p[0] == "0"):
            newPaiCount[ch][5] -= 1
        newPaiCount[ch][num] -= 1
        return newPaiCount
    GetCountOff = staticmethod(GetCountOff)

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


class TingJudger:
    def _xiangting(m, d, g, j):
        # 雀頭がない場合は5ブロック必要
        if(j):
            n = 4
        else:
            n = 5
        # 面子過多の補正
        if (m > 4):
            d += m - 4
            m = 4
        # 搭子過多の補正
        if (m + d > 4):
            g += m + d - 4
            d = 4 - m
        # 孤立牌過多の補正
        if (m + d + g > n):
            g = n - m - d
        # 雀頭がある場合は搭子として数える
        if (j):
            d = d + 1
        return 13 - m * 3 - d * 2 - g
    _xiangting = staticmethod(_xiangting)


    # 求向听数
    def xiangting(paiCount, fulu):
        max_yiban = TingJudger.xiangting_yiban(paiCount, fulu)
        xg = TingJudger.xiangting_guoshi(paiCount)
        xq = TingJudger.xiangting_qiduizi(paiCount)
        return min(max_yiban, min(xg, xq))
    xiangting = staticmethod(xiangting)

    def xiangting_yiban(paiCount, fulu):
        # 没有指定雀头的情况下向听数作为最小值
        min_xiangting = TingJudger.mianzi_all(paiCount, fulu)
        # 遍历4种牌
        for ch in paiCount:
            shoupai = paiCount[ch]
            for n in range(1,len(shoupai)):
                # 非雀头
                if (shoupai[n] < 2):
                    continue
                # 剩余手牌拆面子
                paiCount[ch][n] -= 2
                xiangting = TingJudger.mianzi_all(paiCount, fulu, True)
                paiCount[ch][n] += 2
                
                # 替换最小值
                min_xiangting = min(xiangting, min_xiangting)

        return min_xiangting
    xiangting_yiban = staticmethod(xiangting_yiban)


    def mianzi_all(paiCount, fulu, jiangpai = False):
        # 分别计算 m p s 的面子与搭子数目
        rm = TingJudger.mianzi(paiCount["m"], 1)
        rp = TingJudger.mianzi(paiCount["p"], 1)
        rs = TingJudger.mianzi(paiCount["s"], 1)
        # 字牌
        z = [0, 0, 0]
        for n in range(1,8):
            # 面子
            if (paiCount["z"][n] >= 3):
                z[0] += 1
            # 搭子
            if (paiCount["z"][n] == 2):
                z[1] += 1
            # 字牌の孤立牌数取得を追加
            if (paiCount["z"][n] == 1):
                z[2] += 1

        # 副露牌作为面子
        if(fulu == None):
            n_fulou = 0
        else:
            n_fulou = len(fulu)

        # 最小向聴数 最大值8
        min_xiangting = 13

        # 萬子、筒子、索子、字牌それぞれの面子・搭子の数についてパターンA、Bの
        #    組合わせで向聴数を計算し、最小値を解とする
        for m in rm:
            for p in rp:
                for s in rs:
                    n_mianzi = m[0] + p[0] + s[0] + z[0] + n_fulou
                    n_dazi = m[1] + p[1] + s[1] + z[1]
                    n_guli = m[2] + p[2] + s[2] + z[2]
                    if (n_mianzi + n_dazi > 4):
                        n_dazi = 4 - n_mianzi
                    # 搭子过多修正
                    xiangting = TingJudger._xiangting(n_mianzi, n_dazi, n_guli, jiangpai)
                    min_xiangting = min(xiangting, min_xiangting)

        return min_xiangting
    mianzi_all = staticmethod(mianzi_all)

    def mianzi(bingpai, n):
        if (n > 9):
            return TingJudger.dazi(bingpai)

        # まずは面子を抜かず位置を1つ進め試行
        max = TingJudger.mianzi(bingpai, n + 1)

        # 順子抜き取り
        if (n <= 7 and bingpai[n] > 0 and bingpai[n + 1] > 0 and bingpai[n + 2] > 0):
            bingpai[n] -= 1
            bingpai[n + 1] -= 1
            bingpai[n + 2] -= 1
            # 抜き取ったら同じ位置でもう一度試行
            r = TingJudger.mianzi(bingpai, n)
            bingpai[n] += 1
            bingpai[n + 1] += 1
            bingpai[n + 2] += 1
            # 各パターンの面子の数を1増やす
            r[0][0] += 1
            r[1][0] += 1
            # 必要であれば最適値の入替えをする
            if (r[0][0] * 2 + r[0][1] > max[0][0] * 2 + max[0][1]):
                max[0] = r[0]
            if (r[1][0] * 10 + r[1][1] > max[1][0] * 10 + max[1][1]):
                max[1] = r[1]

        # 刻子抜き取り
        if (bingpai[n] >= 3):
            bingpai[n] -= 3
            r = TingJudger.mianzi(bingpai, n)
            bingpai[n] += 3
            r[0][0] += 1
            r[1][0] += 1
            if (r[0][0] * 2 + r[0][1] > max[0][0] * 2 + max[0][1]):
                max[0] = r[0]
            if (r[1][0] * 10 + r[1][1] > max[1][0] * 10 + max[1][1]):
                max[1] = r[1]

        return max
    mianzi = staticmethod(mianzi)
    

    # 计算搭子数
    def dazi(bingpai):
        n_pai = 0
        n_dazi = 0
        n_guli = 0
        for n in range(1,10):
            n_pai += bingpai[n]
            if (n <= 7 and bingpai[n + 1] == 0 and bingpai[n + 2] == 0):
                #n_dazi += n_pai / 2
                n_dazi += n_pai >> 1
                n_guli += n_pai % 2
                n_pai = 0

        #n_dazi += n_pai / 2
        n_dazi += n_pai >> 1
        n_guli += n_pai % 2

        return [[0, n_dazi, n_guli], [0, n_dazi, n_guli]]
    dazi = staticmethod(dazi)


    # 七对子形的向听数
    def xiangting_qiduizi(paiCount):
        n_duizi = 0
        n_danqi = 0

        for kv in paiCount:
            pnum = paiCount[kv]
            for n in range(1,len(pnum)):
                if (pnum[n] >= 2):
                    n_duizi += 1
                elif (pnum[n] == 1):
                    n_danqi += 1

        # 対子過多の補正
        if (n_duizi > 7):
            n_duizi = 7
        # 孤立牌過多の補正
        if (n_duizi + n_danqi > 7):
            n_danqi = 7 - n_duizi

        return 13 - n_duizi * 2 - n_danqi
    xiangting_qiduizi = staticmethod(xiangting_qiduizi)

    # 国士无双 向听
    def xiangting_guoshi(paiCount):
        n_yaojiu = 0
        you_duizi = False
        for ch in paiCount:
            bingpai = paiCount[ch]
            if(ch == 'z'):
                nn = [1, 2, 3, 4, 5, 6, 7]
            else:
                nn = [1, 9]
            for n in nn:
                if (bingpai[n] > 0):
                    n_yaojiu += 1
                if (bingpai[n] > 1):
                    you_duizi = True

        if(you_duizi):
            return 12 - n_yaojiu
        else:
            13 - n_yaojiu
    xiangting_guoshi = staticmethod(xiangting_guoshi)

    # 求可以（进张）听的牌
    def tingpai(paiCount, fulu):
        pai = []
        # 原先向听数
        n_xiangting = TingJudger.xiangting(paiCount, fulu)
        for ch in paiCount:
            bingpai = paiCount[ch]
            for n in range(1,len(bingpai)):
                if (bingpai[n] >= 4):
                    continue
                paiCount[ch][n] += 1
                if (TingJudger.xiangting(paiCount, fulu) < n_xiangting):
                    pai.append(n+ch)
                paiCount[ch][n] -= 1

        return pai
    tingpai = staticmethod(tingpai)

    # 求可立直牌
    def FindLizhi(handStack,fuluStack,riverstr):
        caldic = []
        pCount = PaiMaker.GetCount(handStack)
        n_xiangting = TingJudger.xiangting(pCount, fuluStack)
        lastp = ''
        for i in range(len(handStack)):
            # 遍历每一张牌
            p = handStack[i]
            if(lastp == p):
                continue
            lastp = p
            newCount = PaiMaker.GetCountOff(handStack,p)
            new_xiangting = TingJudger.xiangting(newCount, fuluStack)
            # 不选择向听数增加的情形
            if (new_xiangting > n_xiangting):
                continue
            # 获取有效进张
            tingpai = TingJudger.tingpai(newCount, fuluStack)
            zhenting = TingJudger.IsZhenting(tingpai,riverstr)
            caldic.append({
                "dapai": p,
                "ting": tingpai,
                "zhenting": zhenting
            })
            
        return caldic
    FindLizhi = staticmethod(FindLizhi)

    def IsZhenting(tingpai,riverstr):
        riverstr = riverstr.replace('0','5')
        for p in tingpai:
            if(re.match(p,riverstr) != None):
                return True
        return False
    IsZhenting = staticmethod(IsZhenting)

class RonJudger:
    # 荣和判定面子拆分
    def Ron(hand, moPai, fulu):
        paiCount = PaiMaker.GetCount(hand)
        # 七对子判定
        qiduim = RonJudger.Ron_qiduizi(paiCount, moPai)
        # 国士无双判定
        guoshim = RonJudger.Ron_guoshi(paiCount, moPai)
        # 九宝莲灯
        jiulianm = RonJudger.Ron_jiulian(paiCount, moPai)
        # 一般 4面1头形
        yibanm = RonJudger.Ron_normal(paiCount, moPai, fulu)
        
        mianzi = []
        mianzi.extend(qiduim)
        mianzi.extend(guoshim)
        mianzi.extend(jiulianm)
        mianzi.extend(yibanm)
        
        return mianzi
    Ron = staticmethod(Ron)

  
    # 七对子判定
    def Ron_qiduizi(paiCount, hulepai):
        paixing = []
        for ch in paiCount:
            shoupai = paiCount[ch]
            for n in range(1,len(shoupai)):
                pcount = shoupai[n]
                if (pcount == 0):
                    continue
                if (pcount == 2):
                    p = ch + str(n) + str(n)
                    if (ch == hulepai[1] and n == int(hulepai[0])):
                        p += hulepai[2] + "!"
                    paixing.append(p)
                else:
                    # 対子でないものがあった場合、和了形でない。
                    return []
        if(len(paixing) == 7):
            return [paixing]
        else:
            return []
    Ron_qiduizi = staticmethod(Ron_qiduizi)

    # 国士无双
    def Ron_guoshi(paiCount,hulepai):
        mianzi = []
        you_duizi = False
        for ch in paiCount:
            shoupai = paiCount[ch]
            if(ch == 'z'):
                nn = [1, 2, 3, 4, 5, 6, 7]
            else:
                nn = [1, 9]
            for n in nn:
                if (shoupai[n] == 2):
                    p = ch + str(n) + str(n)
                    if (ch == hulepai[1] and n == int(hulepai[0])):
                        p += hulepai[2] + "!"
                    mianzi.append(p)
                    you_duizi = True
                elif (shoupai[n] == 1):
                    p = ch + str(n)
                    if (ch == hulepai[1] and n == int(hulepai[0])):
                        p += hulepai[2] + "!"
                    mianzi.append(p)
                else:
                    # 足りない幺九牌があった場合、和了形でない。
                    return []
        if(you_duizi):
            return [mianzi]
        else:
            return []
    Ron_guoshi = staticmethod(Ron_guoshi)

    def Ron_jiulian(paiCount, hulepai):
        # 如果存在字牌 则不是九莲
        if(sum(paiCount['z']) > 0):
            return []

        # 遍历4种牌
        for ch in ['m','p','s']:
            shoupai = paiCount[ch]
            mianzi = ch
            # 对于该牌型检查
            for n in range(1,10):
                # 1和9不满3张则无效
                if ((n == 1 or n == 9) and shoupai[n] < 3):
                    return []
                # 缺少某一个数字则无效
                if (shoupai[n] == 0):
                    return []
                # 牌数
                if(n == int(hulepai[0])):
                    nn = shoupai[n] - 1
                else:
                    nn = shoupai[n]
                
                for i in range(0,nn):
                    mianzi += str(n)

            if (len(mianzi) == 14):
                mianzi += str(hulepai[0])+str(hulepai[2]) + "!"
                return [[mianzi]]

        return []
    Ron_jiulian = staticmethod(Ron_jiulian)

  
    # 一般型判定
    def Ron_normal(paiCount, hulepai, fulu):
        mzlist = []
        # 遍历4种牌
        for ch in paiCount:
            shoupai = paiCount[ch]
            for n in range(1,len(shoupai)):
                # 先挑选雀头
                if (shoupai[n] < 2):
                    continue
                jiangpai = ch + str(n) + str(n)
                # 剩余手牌拆面子
                paiCount[ch][n] -= 2
                for mianzi in RonJudger.MianziDevide(paiCount, fulu):
                    mianzi.insert(0,jiangpai)
                    if (len(mianzi) != 5):
                        continue
                    mark = RonJudger.AddMark(mianzi, hulepai)
                    mzlist.extend(mark)
                paiCount[ch][n] += 2

        return mzlist
    Ron_normal = staticmethod(Ron_normal)


    # 面子拆分
    def MianziDevide(paiCount,fulou):
        all_mianzi = [[]]
        # 万饼索分别检测
        for ch in ['m', 'p', 's']:
            new_mianzi = []
            sub_mianzi = RonJudger.MianziPick(ch, paiCount[ch], 1)
            #print(ch,sub_mianzi)
            for mm in all_mianzi:
                for nn in sub_mianzi:
                    aa = copy.deepcopy(mm)
                    aa.extend(nn)
                    new_mianzi.append(aa)
            #print('new',ch,sub_mianzi)
            all_mianzi = new_mianzi

        
        # 字牌检测
        mianzi_z = []
        for n in range(1,8):
            if (paiCount['z'][n] == 0):
                continue
            if (paiCount['z'][n] != 3):
                return []
            mianzi_z.append('z' + str(n) + str(n) + str(n))

        # 组合
        for i in range(len(all_mianzi)):
            all_mianzi[i].extend(mianzi_z)
            all_mianzi[i].extend(fulou)
            #all_mianzi[i] = all_mianzi[i].extend(mianzi_z).extend(fulou)
        
        return all_mianzi
    MianziDevide = staticmethod(MianziDevide)

    #面子拆分搜索
    def MianziPick(s, shoupai, n):
        if (n > 9):
            return [[]]

        # 面子を抜き取り終わったら、次の位置に進む
        if (shoupai[n] == 0):
            return RonJudger.MianziPick(s, shoupai, n + 1)

        shunzi = []
        # 順子を抜き取る
        if (n <= 7 and shoupai[n] > 0 and shoupai[n + 1] > 0 and shoupai[n + 2] > 0):
            shoupai[n] -= 1
            shoupai[n + 1] -= 1
            shoupai[n + 2] -= 1
            shunzi = RonJudger.MianziPick(s, shoupai, n)  # 抜き取ったら同じ位置でもう一度試行
            shoupai[n] += 1
            shoupai[n + 1] += 1
            shoupai[n + 2] += 1

            for s_mianzi in shunzi:
                s_mianzi.insert(0,s+str(n)+str(n+1)+str(n+2))

        kezi = []
        # 刻子を抜き取る
        if (shoupai[n] >= 3):
            shoupai[n] -= 3
            kezi = RonJudger.MianziPick(s, shoupai, n)    # 抜き取ったら同じ位置でもう一度試行
            shoupai[n] += 3
            for k_mianzi in kezi:
                k_mianzi.insert(0,s+str(n)+str(n)+str(n))
        
        if(shunzi == [] and kezi == []):
            return [[]]
            
        #print(s,n,shunzi,kezi)
        shunzi.extend(kezi)
        #print('extend:',shunzi)

        return shunzi
    MianziPick = staticmethod(MianziPick)

    def AddMark(mianzi, p):
        ppp = p[0]
        if(ppp == "0"):
            ppp = "5"
        regexp = "^(" + p[1] + ".*" + ppp + ")"
        # replacer = "$1" +  p[2] + "!"
        replacer = p[2] + "!"

        new_mianzi = []
        for i in range(len(mianzi)):
            # 副露面
            if ( re.match("[\-\+\=]",mianzi[i]) != None ):
                continue
            # 相同略
            if (i > 0 and mianzi[i] == mianzi[i - 1]):
                continue
            ss = re.match(regexp,mianzi[i])
            if(ss):
                replacer = ss.group()+p[2] + "!"
            m = re.sub(regexp,replacer,mianzi[i],1)
            if (m == mianzi[i]):
                continue
            tmp_mianzi = copy.deepcopy(mianzi)
            tmp_mianzi[i] = m
            new_mianzi.append(tmp_mianzi)

        return new_mianzi
    AddMark = staticmethod(AddMark)

