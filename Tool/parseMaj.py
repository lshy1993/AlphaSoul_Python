# from xml.dom.minidom import parse
import xml.etree.cElementTree as ET
import numpy as np
import pandas as pd
import os
import re
# import math
# from tool import PaiMaker

''' 天凤牌谱解析
'''

ROOT = 'E:/MAJ/tenhou/log/'
OUT_PATH = 'E:/MAJ/tenhou/state/'
hai = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
    "1z", "2z", "3z", "4z", "5z", "6z", "7z","0m","0p","0s"]

class State():
    def __init__(self,fname):
        self.fname = fname
        self.reset()
        self.changfeng = 0
        self.changbang = 0
        self.lizhibang = 0
        self.score = [25000,25000,25000,25000]
        # self.table = pd.DataFrame(columns=range(24),dtype=np.int)
        self.table = pd.DataFrame(columns=range(187),dtype=np.int)
        self.actionList = []
        self.step = 0
        self.rnd = 0

    def reset(self):
        self.handStack = [[],[],[],[]]
        self.fuluStack = [[],[],[],[]]
        self.riverStack = [[],[],[],[]]
        self.lizhiflag = [False,False,False,False]
        self.bao = []

    def getTile(self, id):
        p = hai[id >> 2]
        if id in [16,52,88]:
            p = p.replace('5','0')
        # print(id,num,p)
        return p

    def codeTile(self,p):
        return hai.index(p)+1
    
    def getYaku(self,id):
        return [
            # 一飜
            "門前清自摸和","立直","一発","槍槓","嶺上開花",
            "海底摸月","河底撈魚","平和","断幺九","一盃口",
            "自風 東","自風 南","自風 西","自風 北",
            "場風 東","場風 南","場風 西","場風 北",
            "役牌 白","役牌 發","役牌 中",
            # 二飜
            "両立直","七対子","混全帯幺九","一気通貫","三色同順",
            "三色同刻","三槓子","対々和","三暗刻","小三元","混老頭",
            # 三飜
            "二盃口","純全帯幺九","混一色",
            # 六飜
            "清一色",
            # 満貫
            "人和",
            # 役満
            "天和","地和","大三元","四暗刻","四暗刻単騎","字一色",
            "緑一色","清老頭","九蓮宝燈","純正九蓮宝燈","国士無双",
            "国士無双１３面","大四喜","小四喜","四槓子",
            # 懸賞役
            "ドラ","裏ドラ","赤ドラ"
        ][id]

    def fuluState(self,nid):
        res = [0 for i in range(24)]
        fulu = self.fuluStack[nid]
        t = 0
        for mz in fulu:
            mz = re.sub(r'[\+\-\=\_]','',mz)
            ch = mz[0]
            for j in range(1,len(mz)):
                n = mz[j]
                res[t] = self.codeTile(n+ch)
                t += 1
        return res
        
    def saveState_o(self,pid,action):
        ''' 按照谁的视角保存 pid action
        '''
        # 24*10 矩阵
        table = np.zeros((10,24),dtype=np.int)
        # 第1行
        # 0场风 0-3东4-7南8-11西
        table[0,0] = self.changfeng
        # 1场棒
        table[0,1] = self.changbang
        # 2立直棒
        table[0,2] = self.lizhibang
        # 3-7宝牌 5张
        for i in range(len(self.bao)):
            table[0,3+i] = self.codeTile(self.bao[i])
        # 8-11点数 4家
        for i in range(4):
            table[0,8+i] = self.score[(i+pid)%4]
        # 记录该State的输出label
        table[0,-1] = action
        # 2-4行
        # 自己手牌 14张
        hand = self.handStack[pid]
        for i in range(len(hand)):
            table[1,i] = self.codeTile(hand[i])
        # 自己副露 16张
        table[2] = self.fuluState(pid)
        # 自己牌河 24张
        river = self.riverStack[pid]
        for i in range(len(river)):
            table[3,i] = self.codeTile(river[i])
        # 接下来的2行*3 下家 对家 上家顺序
        for k in range(1,4):
            nid = (pid+k)%4
            # 副露 16张
            table[3+(k-1)*2] = self.fuluState(nid)
            # 牌河 24张
            river = self.riverStack[nid]
            for i in range(len(river)):
                table[3+(k-1)*2+1,i] = self.codeTile(river[i])

        df = pd.DataFrame(table, dtype=np.int)
        # fname = '{}_{:02d}{:03d}.pkl'.format(self.fname[13:],self.rnd,self.step)
        # df.to_pickle(OUT_PATH + fname)
        # fname = '{}_{:02d}{:03d}.csv'.format(self.fname[13:],self.rnd,self.step)
        # df.to_csv(OUT_PATH + fname,index=False,header=0)
        self.table = self.table.append(df)

        self.step += 1

    def saveState(self,pid,action):
        ''' 按照谁的视角保存 pid action
        '''
        # 186*1 矩阵
        table = np.zeros((1,187),dtype=np.int)
        # 第1行
        # 0场风 0-3东4-7南8-11西
        table[0,0] = self.changfeng
        # 1场棒
        table[0,1] = self.changbang
        # 2立直棒
        table[0,2] = self.lizhibang
        # 3-7宝牌 5张
        for i in range(len(self.bao)):
            table[0,3+i] = self.codeTile(self.bao[i])
        # 8-11点数 4家
        for i in range(4):
            table[0,8+i] = self.score[(i+pid)%4]
        # 记录该State的输出label
        table[0,-1] = action
        # 2-4行
        # 自己手牌 14张
        hand = self.handStack[pid]
        for i in range(len(hand)):
            table[0,12+i] = self.codeTile(hand[i])
        # 接下来的2行*4 自己 下家 对家 上家顺序
        for k in range(4):
            nid = (pid+k)%4
            # 副露 16张 26-41
            for i in range(16):
                table[0,26+k*(16+24)+i] = self.fuluState(nid)[i]
            # 牌河 24张 42-65
            river = self.riverStack[nid]
            for i in range(len(river)):
                table[0,26+k*(16+24)+16+i] = self.codeTile(river[i])

        df = pd.DataFrame(table, dtype=np.int)
        self.table = self.table.append(df,ignore_index=True)
        self.step += 1


    def saveToFile(self):
        # df = pd.DataFrame(self.table, dtype=np.int)
        # fname = '{}.pkl'.format(self.fname[13:])
        # self.table.to_pickle(OUT_PATH + fname)
        fname = '{}.csv'.format(self.fname[13:])
        self.table.to_csv(OUT_PATH + fname)

    def showChang(self):
        print( '{}{}局'.format('东南西北'[int(self.changfeng/4)], self.changfeng%4+1) )

    def inithand(self,attrib):
        self.step = 0
        self.rnd += 1
        self.reset()
        seed = list(attrib['seed'].split(','))
        self.changfeng = int(seed[0])
        self.changbang = int(seed[1])
        self.lizhibang = int(seed[2])
        self.dora(int(seed[5]))
        ten = attrib['ten']
        for i,score in enumerate(ten.split(',')):
            self.score[i] = int(score)
        for i in range(4):
            tt = 'hai'+str(i)
            hand = list(attrib[tt].split(','))
            for num in hand:
                p = self.getTile(int(num))
                self.handStack[i].append(p)
            # hand_s = PaiMaker.GetSortPai(self.handStack[i])
            # print( '{}p: {}'.format(i, ' '.join(hand_s)) )
    
    def dora(self,num):
        p = self.getTile(num)
        self.bao.append(p)

    def mopai(self,tag):
        who = ord(tag[0]) - ord('T')
        p = self.getTile(int(tag[1:]))
        self.handStack[who].append(p)
        # hand_s = PaiMaker.GetSortPai(self.handStack[who])
        # print( '{}p 摸牌: {} {} {}'.format(who, p, ''.join(hand_s), ' '.join(self.fuluStack[who])) )

    def discard(self,tag):
        who = ord(tag[0]) - ord('D')
        p = self.getTile(int(tag[1:]))
        # print(self.handStack[who])
        # 保存当前state 和 action
        try:
            act = self.handStack[who].index(p) + 1
        except:
            print(tag,p,' '.join(self.handStack[who]))
            raise Exception()
        if(self.lizhiflag[who]):
            act += 14
        self.saveState(who,act)
        if act == 0:
            print(p,self.lizhiflag[who])
            raise Exception('action=0')
        # hand_s = PaiMaker.GetSortPai(self.handStack[who])
        # print( '{}p 切牌: {} {} {} {}'.format(who, p, ''.join(hand_s), ' '.join(self.fuluStack[who]), self.lizhiflag[who]) )

        # 删除手牌进入牌河
        self.handStack[who].remove(p)
        self.riverStack[who].append(p)
        if self.lizhiflag[who]:
            self.lizhiflag[who] = False

    def reach(self,attrib):
        who = int(attrib['who'])
        if attrib['step'] == '1':
            # 立直宣告
            self.lizhiflag[who] = True
        elif attrib['step'] == '2':
            # 没有被吃碰胡 成功            
            self.lizhibang += 1
            self.score[who] -= 1000

    def fulu(self,attrib):
        # <N who="3" m="42031" />
        who = int(attrib['who'])
        m = int(attrib['m']) # 16bit整数
        # 1-2 下家1 对家2 上家3
        pid = m & 0x0003
        if(m & 0x0004 != 0):
            # 吃
            if(pid != 3):
                raise Exception('吃格式错误')
            
            # 4-5 最小の数牌のID mod 4
            minp = m & 0x0018 # % 4
            # 6-7 真ん中の数の数牌のID mod 4
            midp = m & 0x0060 # % 4
            # 8-9 最大の数牌のID mod 4
            maxp = m & 0x0180 # % 4
            # 11-16	形式
            t = (m & 0xFC00) >> 10
            r = t % 3 # 左中右哪一张牌是吃进来的
            t = int(t/3)
            ch = ['m','p','s'][int(t/7)]
            n = t % 7 + 1
            fulu = [n,n+1,n+2]
            for i in range(3):
                if fulu[i] == 5 and [minp,midp,maxp][i] == 0:
                    fulu[i] = '0'+ch
                else:
                    fulu[i] = str(fulu[i]) + ch
                if i == r:
                    fulu[i] += ['','+','=','-'][pid]
            # print(t,r,fulu)
            act = 29 + r * 3
            if(minp == 0):
                act += 0
            elif(midp == 0):
                act += 1
            elif(maxp == 0):
                act += 2
            self.saveState(who,act)
            if(act == 0):
                raise Exception('act=0')
            # print('吃',fulu,act)
            # 移除手牌
            try:
                self.riverStack[(who+pid) % 4].remove(fulu[r][:2])
            except:
                print('移除他家手牌',self.riverStack[(who+pid) % 4])
                raise Exception()
            fulu_s = ch
            for i in range(3):
                fulu_s += fulu[i][0]
                if i != r:
                    try:
                        self.handStack[who].remove(fulu[i])
                    except:
                        print('移除自身手牌',i,self.handStack[who])
                        raise Exception() 
                else:
                    fulu_s += ['','+','=','-'][pid]
            self.fuluStack[who].append(fulu_s)
            # hand_s = PaiMaker.GetSortPai(self.handStack[who])
            # print("{}p 吃: {} {}".format(who,''.join(hand_s),self.fuluStack[who]))
            
        elif(m & 0x0018 != 0):
            # 6-7 未使用牌ID mod4
            unused = (m & 0x0060) # % 4
            # 10-16 形式
            t = (m & 0xFE00) >> 9
            r = t % 3 # 左中右哪一张牌是碰进来的
            t = int(t/3)
            ch = ['m','p','s','z'][int(t/9)]
            n = str(t % 9 + 1)
            fulu = [n+ch,n+ch,n+ch,n+ch] # 默认杠 碰只取前3位
            if(ch != 'z' and n == '5'):
                if (unused == 0):
                    fulu[3] = '0'+ch # 无红宝 4位
                elif r == 0:
                    fulu[2] = '0'+ch # 碰红宝 3位
                else:
                    fulu[0] = '0'+ch # 有红宝 1位
            self.saveState(who,38)
            # print('碰',t,r,fulu)
            if(m & 0x0010 != 0):
                # 加杠
                # 修改自身副露
                try:
                    self.handStack[who].remove(fulu[3])
                except:
                    self.showChang()
                    print(fulu,self.handStack[who])
                    raise Exception('移除自身手牌错误')
                for index,fulu in enumerate(self.fuluStack[who]):
                    if re.match(ch+n+'{2}',fulu):
                        self.fuluStack[who][index] += n
                
                # hand_s = PaiMaker.GetSortPai(self.handStack[who])
                # print("{}p 加杠:{} {}".format(who,''.join(hand_s),self.fuluStack[who]))
            elif(m & 0x0008 != 0):
                # 碰
                # 拾取牌河 添加副露
                try:
                    self.riverStack[(who+pid) % 4].remove(fulu[2])
                except:
                    print(self.riverStack[(who+pid) % 4])
                    raise Exception()
                try:
                    self.handStack[who].remove(fulu[0])
                except:
                    print(fulu,self.handStack[who])
                    raise Exception()
                try:
                    self.handStack[who].remove(fulu[1])
                except:
                    print(fulu,self.handStack[who])
                    raise Exception()

                fulu_s = ch
                for i in range(3):
                    fulu_s += fulu[i][0]
                fulu_s += ['','+','=','-'][pid]
                self.fuluStack[who].append(fulu_s)

                # hand_s = PaiMaker.GetSortPai(self.handStack[who])
                # print("{}p 碰:{} {}".format(who,''.join(hand_s),self.fuluStack[who]))
            else:
                raise Exception("副露格式错误")
        elif(m & 0x0020 != 0):
            # 拨北
            # 1-5	0x001f	空き
            # 6	0x0020	北抜きフラグ
            # 7-8	0x00c0	空き
            # 9-16	0xff00	牌ID
            pass
        else:
            # 大明槓・暗槓
            self.saveState(who,39)
            # 9-16 鳴いた牌ID
            t = (m & 0xff00) >> 8
            r = t % 4 # 哪一张牌是杠进来的
            t = int(t/4)
            ch = ['m','p','s','z'][int(t/9)]
            n = str(t % 9 + 1)
            fulu = [n+ch,n+ch,n+ch,n+ch]
            if(ch != 'z' and n == '5'):
                if (pid == 0):
                    fulu[3] = '0'+ch # 暗杠红宝在4位
                elif r == 0:
                    fulu[3] = '0'+ch # 明杠红宝在4位
                else:
                    fulu[2] = '0'+ch # 手牌红宝3位
            # print('杠',t,r,fulu)
            # 移除手牌
            try:
                self.handStack[who].remove(fulu[0])
            except:
                print(fulu,self.handStack[who])
                raise Exception()
            try:    
                self.handStack[who].remove(fulu[1])
            except:
                print(fulu,self.handStack[who])
                raise Exception()
            try:
                self.handStack[who].remove(fulu[2])
            except:
                print(fulu,self.handStack[who])
                raise Exception()
            
            if(pid == 0):
                self.handStack[who].remove(fulu[3])
            else:
                self.riverStack[(who+pid) % 4].remove(fulu[3])
            fulu_s = ch
            for i in range(4):
                fulu_s += fulu[i][0]
            fulu_s += ['','+','=','-'][pid]
            self.fuluStack[who].append(fulu_s)
            # hand_s = PaiMaker.GetSortPai(self.handStack[who])
            # print("{}p 杠: {} {}".format(who,''.join(hand_s),self.fuluStack[who]))


    def hu(self,attrib):
        # <AGARI ba="2,2" hai="17,22,26,68,70,74,77,81,84,91,94" m="44618" machi="91" ten="30,2000,0" yaku="12,1,52,1" doraHai="73" who="1" fromWho="1" sc="215,-7,285,46,328,-7,152,-12" />
        # print(attrib)
        ba = list(attrib['ba'].split(','))
        # print('场棒:{} 立直棒:{}'.format(ba[0],ba[1]))
        who = int(attrib['who'])
        fromWho = int(attrib['fromWho'])
        self.saveState(who,40)
        return
        # 手牌（含和牌）
        hai = list(attrib['hai'].split(','))
        # 副露
        if 'm' in attrib:
            m = list(attrib['m'].split(','))
        # 和牌
        machi = attrib['machi']
        # 番
        ten = list(attrib['ten'].split(','))
        ddstr = ['','満貫','跳満','倍満','三倍満','役満'][int(ten[2])]
        print('{}符 {}点 {}'.format(ten[0],ten[1],ddstr))
        # 役
        yaku = list(attrib['yaku'].split(','))
        for i in range( int(len(yaku)/2) ):
            t = int(yaku[i*2])
            print(self.getYaku(t),yaku[i*2+1])
        # 役满
        if 'yakuman' in attrib:
            yakuman = list(attrib['yakuman'].split(','))
            print(yakuman)
        # 宝牌
        doraHai = list(attrib['doraHai'].split(','))
        # 里宝牌
        if 'doraHaiUra' in attrib:
            doraHaiUra = list(attrib['doraHaiUra'].split(','))

        sc = list(attrib['sc'].split(','))
        for i in range( int(len(sc)/2) ):
            # 之前的点数 变化
            print( 'p{}:{} {}'.format(i,sc[i*2],sc[i*2+1]) )
        # input()
        if 'owari' in attrib:
            print("end")

    def liuju(self,attrib):
        # <RYUUKYOKU ba="1,2" sc="200,15,270,15,343,-15,167,-15" hai0="8,9,15,19,20,24,25,26,29,33,41,47,50" hai1="27,30,52,53" />
        ba = list(attrib['ba'].split(','))
        # print('场棒:{} 立直棒:{}'.format(ba[0],ba[1]))
        print('流局')
        sc = list(attrib['sc'].split(','))
        for i in range(len(sc)/2):
            # 之前的点数 变化
            print( 'p{}:{} {}'.format(i,sc[i*2],sc[i*2+1]) )

        if 'hai0' in attrib:
            who = 0
        if 'hai1' in attrib:
            who = 1
        if 'hai2' in attrib:
            who = 2
        if 'hai3' in attrib:
            who = 3

        if 'type' in attrib:
            dic = {
                'yao9':'九種九牌',
                'reach4':'四家立直',
                'ron3':'三家和了',
                'kan4':'四槓散了',
                'kaze4':'四風連打',
                'nm':'流し満貫'
            }
            print(dic[ attrib['type'] ])
            if attrib['type'] == 'yao9':
                self.saveState(who,41)
        if 'owari' in attrib:
            print("end")

def readFile(file_name):
    print(file_name)
    DOMTree = ET.ElementTree(file=ROOT+file_name)
    root = DOMTree.getroot()
    # print(root.tag)
    state = State(file_name)
    for child_of_root in root:
        tag,attrib = child_of_root.tag,child_of_root.attrib
        # print(tag,attrib)
        if tag == 'TAIKYOKU':
            oya = attrib['oya']
            continue
        elif tag == 'INIT':
            state.inithand(attrib)
            continue
        elif tag == 'REACH':
            state.reach(attrib)
        elif tag == 'N':
            state.fulu(attrib)
        elif tag == 'DORA':
            num = int(attrib['hai'])
            state.dora(num)
        elif tag == 'AGARI':
            state.hu(attrib)
        elif re.match(r'[D-G](\d+)',tag) != None:
            state.discard(tag)
        elif re.match(r'[T-W](\d+)',tag) != None:
            state.mopai(tag)
        else:
            pass
    # state.saveToFile()

file_max = 1000
dirs = os.listdir(ROOT)
count = 0
for file in dirs:
    if(count == file_max):
        break
    readFile(file)
    count += 1

