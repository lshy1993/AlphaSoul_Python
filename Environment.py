import random
import time
import copy
import re
import tkinter as tk
from tool import PaiMaker
from tool import PtJudger
from tool import TingJudger
from tool import MianziMaker

MAX_Wind = 1 # 东风局0 南风局1

class Environment(tk.Tk,object):

    def __init__(self, rule, visualize=False):
        super().__init__()
        self._rule = rule
        self.msgList = [None,None,None,None]
        self.pp = 0
        self._visualize = visualize
        if(self._visualize):
            self.initwindow()
        
        self.initParam()

    def render(self):
        # time.sleep(0.01)
        if(self._visualize):
            for i in range(4):
                self.var[i].set( '{}: {}{}\n'.format(i,self.handStack[i],self.fuluStack[i]) )
            self.okVar.set(0)
            self.button.wait_variable(self.okVar)
            self.update()

    def initwindow(self):
        self.title('maj')
        self.geometry('{0}x{1}'.format(640,480))
        self.var = [tk.StringVar() for _ in range(4)]
        for i in range(4):
            l = tk.Label(self, textvariable=self.var[i], font=('Arial', 12), width=640, height=2)
            l.pack()
        self.okVar = tk.IntVar()
        self.button = tk.Button(self, text='next', font=('Arial', 12), width=10, height=1, command=lambda: self.okVar.set(1))
        self.button.pack()


    def newgame(self,SEED = None):
        random.seed(SEED)
        self.initParam()
        self.initWind()
        self.sendTile()
        return self

    def initParam(self):
        ''' 初始化开局
        '''
        self.resetParam()
        # 场风
        self.changfeng = 0
        # 4家各风
        self.playerWind = [0,1,2,3]
        # 场棒
        self.changbang = 0
        self.lizhibang = 0
        # 4家得分
        self.score = [25000,25000,25000,25000]
        # 庄家
        self.qinjia = 0


    def resetParam(self):
        ''' 重开发牌
        '''
        # 玩家手牌
        self.handStack = [[],[],[],[]]        
        # 牌河
        self.riverStack = [[],[],[],[]]
        # 鸣牌区域
        self.fuluStack = [[],[],[],[]]
        # 随机生成新牌堆
        self.yama = PaiMaker.GeneratePai()
        # 牌顶位置
        self.yamaPos = -1
        # 杠牌位置
        self.yamaLast = 135
        # 宝牌位置
        self.baoPos = 130
        # 翻开第一张宝牌 (宝牌倒着开)
        self.bao = [self.yama[self.baoPos]]
        self.libao = [self.yama[self.baoPos + 1]]
        # 下个宝牌
        self.baoPos -= 2
        # 4家立直
        self.playerLizhi = [0,0,0,0]
        # 4家巡数
        self.xunshu = [0,0,0,0]
        # 首巡
        self.diyizimo = [True,True,True,True]
        # 振听状态
        self.zhenting = [False, False, False, False]
        # 杠后牌
        self.gangflag = False
        # 一发状态
        self.yifa = [False,False,False,False]
        # 点数分配
        self.realfenpei = [0,0,0,0]
        # 当前轮到的玩家
        self.curWind = 0
        # 单局结束
        self.endSection = False
        # 是否连庄
        self.lianzhuang = False
        # 终庄指示
        self.endGame = False

    def isPlayerZhenting(self,i):
        ''' 判断是否振听
        '''
        pCount = PaiMaker.GetCount(self.handStack[i])
        tingpai = TingJudger.tingpai(pCount, self.fuluStack[i])
        riverstr = str(self.riverStack[i])
        # 是否有任何一张听牌是否出现在牌河内
        return TingJudger.IsZhenting(tingpai,riverstr)

    def getPlayerStatus(self,i):
        gs = {}
        gs['qinjia'] = self.qinjia
        gs['changfeng'] = self.changfeng
        gs['zifeng'] = self.playerWind[i]
        gs['changbang'] = self.changbang
        gs['lizhibang'] = self.lizhibang
        gs['score'] = self.score
        gs['bao'] = self.bao
        gs['handStack'] = self.handStack[i]
        gs['seat'] = i
        return gs

    def initWind(self):
        ''' 新开一局
        '''
        self.pp += 1
        print(['东','南','西','北'][self.changfeng]+str(self.qinjia+1)+'局')
        # print(' '.join(map(lambda x: 'p'+str(x)+':'+['东','南','西','北'][x], self.playerWind)))
        # 重置参数
        self.resetParam()
        #print(''.join(self.yama))
        # 摸4轮牌
        for t in range(4):
            # 4个玩家按照自风依次
            for p in range(4):
                if (t < 3):
                    # 前3轮 每轮连续摸4张
                    for _ in range(4):
                        self.yamaPos += 1
                        mpai = self.yama[self.yamaPos]
                        self.handStack[p].append(mpai)
                else:
                    # 第四轮
                    self.yamaPos += 1
                    mpai = self.yama[self.yamaPos]
                    self.handStack[p].append(mpai)

        # 自动牌局 东风起手
        self.curWind = -1
        self.endSection = False
        self.lianzhuang = False

    def sendTile(self):
        # 继续下一家 发送新牌
        # self.curWind += 1
        # if self.curWind == 4:
        #     self.curWind = 0
        self.curWind = (self.curWind+1) % 4
        # 当前玩家编号
        pid = (self.curWind+self.qinjia) % 4
        self.xunshu[pid] += 1
        # 从牌顶 摸牌
        self.yamaPos += 1
        mo = self.yama[self.yamaPos]
        self.handStack[pid].append(mo)
        if len(self.handStack[pid]) + len(self.fuluStack[pid]) * 3 != 14:
            print(pid, self.handStack[pid], self.fuluStack[pid])
            raise Exception('手牌数错误')
        # print(pid,'摸牌',mo)
        # 通知生成（暗杠 立直 胡牌 流局）
        self.allow_zimo(pid,mo)

    def getPlayerParam(self,i):
        ''' 获取玩家计分默认参数
        '''
        param = {}
        # 场风 (0: 東, 1: 南, 2: 西, 3: 北)
        param['zhuangfeng'] = self.changfeng
        # 自风 (0: 東, 1: 南, 2: 西, 3: 北)
        param['menfeng'] = self.playerWind[i]
        # 宝牌
        param['baopai'] = self.bao
        # 里宝牌
        param['fubaopai'] = []
        if self.playerLizhi[i] > 0:
            param['fubaopai'] = self.libao
        # 场棒
        param['changbang'] = self.changbang
        # 立直棒
        param['lizhibang'] = self.lizhibang

        # 状况役 0 无 1 立直 2 两立直
        param['lizhi'] = self.playerLizhi[i]
        # 一发
        param['yifa'] = self.yifa[i]
        # 抢杠
        param['qianggang'] = False
        # 岭上开花
        param['lingshang'] = self.gangflag
        # 1: 海底摸月(自摸) 2: 河底捞鱼（荣和）
        param['haidi'] = 0
        # 1: 天和, 2: 地和
        param['tianhu'] = 0
        if self.diyizimo[i]:
            param['tianhu'] = 2
            if self.playerWind[i] == 0:
                param['tianhu'] = 1
        return param

    def step(self,msg):
        ''' 优先处理多人同时消息
        '''
        finalres = None
        # 多人胡牌消息
        hu_res = []
        # 多人副露消息
        fulu_res = []
        # print('receive: {}'.format(msg))
        for act in msg:
            if act == None or act['type'] == 'cancel':
                continue
            # 胡 与 吃碰杠 分开

            if act['type'] == 'hu':
                hu_res.append(act)
            elif act['type'] == 'chipenggang':
                fulu_res.append(act)
            else:
            #if act['type'] == 'qiepai' or act['type'] == 'zimo':
                finalres = act
                break
                #raise Exception('未知类型 {}'.format(act))

        if len(hu_res) > 0:
            # 胡牌处理流程
            # print('胡消息',finalres)
            return self.hu(hu_res)            
        elif len(fulu_res) > 0:
            # 选择副露最优先的
            dd = sorted(fulu_res,key=lambda x: x['combination'][1])
            finalres = dd[0]
            # print('副露',finalres)
        elif finalres == None:
            # 立直宣告成立
            #if(act['lizhi']):
            #    self.lizhibang += 1
            #    self.score[pid] -= 1000
            pass

        return self.nextstep(finalres)

    def nextstep(self, action):
        ''' 进行步骤
        '''
        # print('msg: {}\n'.format(action), end='')
        self.msgList = [None,None,None,None]
        # 是否终庄
        if self.endSection:
            if min(self.score) < 0:
                # 有人被飞
                print('有人被飞')
                self.endGame = True
            elif self.changfeng > MAX_Wind:
                print('{}入判定'.format('东南西北'[MAX_Wind+1]))
                # 西入时，只要有任何人超过30000 或到西4局 即结束
                self.endGame = self.qinjia == 3 or max(self.score) >= 30000
            elif self.changfeng == MAX_Wind and self.qinjia == 3:
                print('{}4判定'.format('东南西北'[MAX_Wind]))
                # 南4判定
                if(self.lianzhuang):
                    pid = 0
                    for i,wind in enumerate(self.playerWind):
                        if wind == 0:
                            pid = i
                            break
                    print('南4庄家:', pid, self.playerWind[0])
                    # 亲家若第一则结束
                    self.endGame = self.score[pid] == max(self.score)
                else:
                    self.endGame = max(self.score) >= 30000
            
            if self.endGame:
                print('end game!',self.score)
                # 向所有玩家发送结束消息
                return self, [0,0,0,0], True
            elif self.lianzhuang:
                print('连庄')
                # 连庄增加场棒
                self.changbang += 1
                self.initWind()
            else:
                # 换庄
                t = self.playerWind.pop()
                self.playerWind.insert(0,t)
                # 场棒清空
                self.changbang = 0
                # 风局变动
                self.qinjia += 1
                if(self.qinjia == 4):
                    self.changfeng += 1
                    self.qinjia = 0
                # print('换庄',t,self.playerWind,self.qinjia)
                self.initWind()

        elif action == None:
            # 是否流局
            if self.Liuju():
                return self, self.realfenpei, False
            # 正常发牌
            self.sendTile()
        elif action['type'] == 'qiepai':
            # 切牌后判定他家副露
            self.allow_fulu(action)
        elif action['type'] == 'chipenggang':
            # 副露
            self.chipenggang(action)
        elif action['type'] == 'angangjiagang':
            # 杠类
            self.angangjiagang(action)
        elif action['type'] == 'zimo':
            # 自摸流程
            return self.zimo(action)
        elif action['type'] == 'cancel':
            # cancel
            pass

        return self, [0,0,0,0], False

    def Liuju(self):
        # 4风连打
        if max(self.xunshu) == 1 and min(self.xunshu) == 1:
            count = [0,0,0,0]
            dic = {'1z':0,'2z':1,'3z':2,'4z':3 }
            for i in range(4):
                if(len(self.riverStack[i]) > 0):
                    p = self.riverStack[i][0]
                    if(p in dic):
                        count[dic[p]] += 1
            if max(count) == 4:
                print('\n4风连打')
                self.realfenpei = [0,0,0,0]                
                self.lianzhuang = True
                self.endSection = True
                return True
        # 4家立直
        if max(self.playerLizhi) == 1 and min(self.playerLizhi) == 1:
            print('\n四家立直',self.score,self.lizhibang)
            self.realfenpei = [-1000,-1000,-1000,-1000]
            self.lianzhuang = True
            self.endSection = True
            return True

        # 计算4家是否听牌    
        if (self.yamaPos == self.yamaLast - 14):
            xiangting = [0,0,0,0]
            tingpai = [[],[],[],[]]
            for i in range(4):
                pcount = PaiMaker.GetCount(self.handStack[i])
                xiangting[i] = TingJudger.xiangting(pcount,self.fuluStack[i])
                if(xiangting[i] == 0):
                    tingpai[i] = TingJudger.tingpai(pcount,self.fuluStack[i])
                # print(i,':',xiangting,'向听');
                # 庄家是否听牌连庄
                if(self.playerWind[i] == 0):
                    self.lianzhuang = xiangting[i] == 0
            # 点数更新(id顺)
            tingSum = sum(xiangting)
            self.realfenpei = [0,0,0,0]
            if (tingSum > 0 and tingSum < 4):
                for i in range(4):
                    if xiangting[i] == 0:
                        self.realfenpei[i] = 3000 / tingSum
                    else:
                        self.realfenpei[i] = -3000 / (4 - tingSum)
                    self.score[i] += self.realfenpei[i]
            print('荒牌流局',self.realfenpei,self.lianzhuang)
            # for i in range(4):
            #     print('手牌{}: {}{}'.format(i,self.handStack[i],self.fuluStack[i]))
            self.endSection = True
            return True
        
        return False

    def allow_zimo(self,pid,mopai):
        msg = {}
        msg['tile'] = mopai
        # 判定可能出现的选项
        msg['operation'] = []
        # 处于立直状态 则无法改牌
        msg['lizhi_state'] = self.playerLizhi[pid] > 0
        if self.playerLizhi[pid] == 0:
            msg['operation'].append({
                'combination': [],
                'type': 1
            })
        # 获取信息
        fulu = self.fuluStack[pid]
        # 是否允 暗/加杠 (最后一张不允许杠)
        if (self.yamaLast-14) != self.yamaPos:
            oriCount = PaiMaker.GetCount(self.handStack[pid])
            gangmz = MianziMaker.get_gang_mianzi(oriCount,fulu,mopai+'_')
            for mz in gangmz:
                    msg['operation'].append({
                    'combination': mz[0],
                    'type': mz[1]
                })

        # 是否能自摸
        param = self.getPlayerParam(pid)
        param['haidi'] = 0
        if (self.yamaLast-14) == self.yamaPos:
            param['haidi'] = 1
        ptr = PtJudger.GetFen(self.handStack[pid], fulu, mopai+'_', param)
        if ptr['hupai'] or ptr['defen'] > 0:
            # print(ptr)
            msg['operation'].append({
                'combination': mopai+'_',
                'type':8
            })

        # 是否可以立直
        paiCount = PaiMaker.GetCount(self.handStack[pid])
        # 向听数
        xt = TingJudger.xiangting(paiCount, fulu)
        # 是否门清
        menqing = True
        for f in fulu:
            if re.match('[\-\+\=](?!\!)',f):
                menqing = False

        if(self.playerLizhi[pid] == 0 and menqing and xt == 0 and (self.yamaLast-14)-self.yamaPos >= 4 and self.score[pid] >= 1000):
            lizhipai = TingJudger.FindLizhi(self.handStack[pid],fulu, str(self.riverStack[pid]))
            msg['operation'].append({
                'combination': lizhipai,
                'type': 7
            })
        # 九种九牌流局
        #msg.liuju = false
        self.msgList[pid] = msg

    def allow_fulu(self,msg):
        ''' 玩家切牌
        '''
        pid = msg['from']
        # 变更当前玩家
        self.curWind = self.playerWind[pid]
        hand = self.handStack[pid]
        fulu = self.fuluStack[pid]
        # 立直是否改牌检测？
        if self.playerLizhi[pid] > 0:
            l = len(hand) - 1
            if msg['tile'] != hand[l]:
                print(msg['tile'], hand)
                raise ValueError('立直改牌')

        # 从手牌堆移除
        try:
            tilepos = hand.index(msg['tile'])
            hand.pop(tilepos)
        except:
            print(msg, self.handStack[pid],self.fuluStack[pid])
            raise Exception('不存在该张手牌')
        
        if len(hand) + len(fulu) * 3 != 13:
            print('not match error2!', msg, hand, fulu)
            raise Exception('切牌后手牌数目不符')

        # print(pid,'切牌:'+msg['tile'],tilepos,PaiMaker.GetSortPai(hand))
        # 进入牌河
        self.riverStack[pid].append(msg['tile'])

        # 收到立直信号
        if 'lizhi' in msg:
            # 是否两立直
            if self.diyizimo[pid]:
                self.playerLizhi[pid] = 2
            else:
                self.playerLizhi[pid] = 1
            # 一发开启
            self.yifa[pid] = True
        elif self.yifa[pid]:
            # 下一次切牌即一发结束
            self.yifa[pid] = False

        # 杠后的切牌 翻开宝牌
        if self.gangflag:
            dora = self.yama[self.baoPos]
            self.bao.append(dora)
            self.libao.append(self.yama[self.baoPos+1])
            self.baoPos -= 2
            self.gangflag = False

        # 第一巡状态结束
        if self.diyizimo[pid]:
            self.diyizimo[pid] = False

        mopai = msg['tile']
        # 为4个agent生成actions
        for id in range(4):
            # 打出者不判定
            if(id == pid):
                continue
            operation = []
            # 判断目标玩家是否能胡牌
            param = self.getPlayerParam(id)
            # 海底
            param['haidi'] = 0
            if (self.yamaLast-14) == self.yamaPos:
                param['haidi'] = 2
            # 加牌后的手牌
            new_hand = copy.copy(self.handStack[id])
            new_hand.append(mopai)
            # 来源标记
            label = ['_','+','=','-'][(4+pid-id) % 4]
            ptr = PtJudger.GetFen(new_hand, self.fuluStack[id], mopai+label, param)
            # 振听的判定
            if (ptr['hupai'] and not self.isPlayerZhenting(id)):
                operation.append({
                    'combination': mopai+label,
                    'type': 9
                })

            # 非立直则可以副露
            if(self.playerLizhi[id] == 0):
                # 判断目标玩家是否可以副露
                fulumz = MianziMaker.GetFuluMianzi(self.handStack[id],self.fuluStack[id],mopai+label)
                for mz in fulumz:
                    operation.append({
                        'combination': mz[0],
                        'type': mz[1]
                    })

            # 有操作可能的添加
            if len(operation) > 0:
                # 等待标记
                # self.waitFlag[id] = self.mode
                self.msgList[id] = { 'operation': operation }

    def chipenggang(self,msg):
        self.diyizimo = [False,False,False,False]
        self.yifa = [False,False,False,False]
        pid = msg['from']
        comb = msg['combination'] # ['2m|3m|4m',2]
        # 将牌从手牌中剔除，加入副露中
        tile = []
        fromlist = []
        fulustr = ''
        for p in comb[0].split('|'):
            fulustr += p[0]
            tile.append(p)

            if len(p) == 2:
                try:
                    self.handStack[pid].remove(p)
                except:
                    print(self.handStack[pid],self.fuluStack[pid],p, comb)
                    raise Exception('副露牌错误')
            elif len(p) > 2:
                fulustr += p[2]
                s = pid
                if p[2] == '+':
                    s += 1
                elif p[2] == '-':
                    s -= 1
                elif p[2] == '=':
                    s += 2
                s = s % 4
                fromlist.append(s)

        self.fuluStack[pid].append(p[1]+fulustr)

        # 生成通知消息
        obj = { 'tiles': tile,'froms': fromlist,'seat': pid,'opt': comb[1] }
        if(comb[1] != 5):
            # 非杠副露 检测是否问题
            if len(self.handStack[pid]) + len(self.fuluStack[pid]) * 3 != 14:
                print(msg)
                print(self.handStack[pid],self.fuluStack[pid])
                raise Exception('手牌组成错误')
            # 副露那家需要切牌
            obj['operation'] = [{'type':1,'combination':[]}]
            self.msgList[pid] = obj
        else:
            print('玩家选择明杠！',msg)
            # 摸杠牌
            self.nextstep({
                'type': 'gangpai',
                'from': pid
            })

    def angangjiagang(self,msg):
        print('收到暗杠加杠消息:',msg)
        pid = msg['from']
        type = msg['combination'][1]
        tiles = msg['combination'][0].split('|')
        gangpai = tiles[1]
        print('gangpai:',gangpai)
        if type == 4:
            # 暗杠
            for p in tiles:
                # 删除手牌
                try:
                    self.handStack[pid].remove(p)
                except:
                    raise Exception('error')

            ch = gangpai[1]
            num = gangpai[0]
            self.fuluStack[pid].append(ch+num+num+num+num)
            print(self.handStack[pid],self.fuluStack[pid])
        else:
            # 加杠
            tilepos = self.handStack[pid].index(gangpai)
            if tilepos != -1:
                self.handStack[pid].pop(tilepos)
            else:
                print('error')
            # 修改副露堆
            ch = gangpai[1]
            num = gangpai[0]
            fulu = self.fuluStack[pid]
            regexp = '^'+ch+num+'{2}'
            for i,p in enumerate(fulu):
                if re.match(regexp,p):
                    print(i,p)
                    self.fuluStack[pid][i] += num

        self.gangflag = True

    def hu(self,msg):
        #print('收到胡了消息 {}'.format(msg))
        self.realfenpei = [0,0,0,0]
        humsg = { 'data': [] }
        # 多人胡逐个处理
        for submsg in msg:
            humsg['data'].append(self.make_humsg(submsg))
        # 立直棒归零
        self.lizhibang = 0
        # 等待确认
        # self.waitFlag = [self.mode,self.mode,self.mode,self.mode]
        self.endSection = True
        return self,self.realfenpei,True

    def zimo(self,msg):
        #print('收到自摸消息 {}'.format(msg))
        self.realfenpei = [0,0,0,0]
        self.make_humsg(msg)
        # 立直棒归零
        self.lizhibang = 0
        # 等待确认
        # self.waitFlag = [self.mode,self.mode,self.mode,self.mode]
        self.endSection = True
        return self,self.realfenpei,True

    def gangpai(self,msg):
        print('发送杠牌')
        # 发送新牌
        pid = msg['from']
        # 从牌底 摸牌
        mo = self.yama[self.yamaLast]
        self.yamaLast -= 1
        print(pid,'杠后牌：',mo)
        self.handStack[pid].append(mo)
        if len(self.handStack[pid]) + len(self.fuluStack[pid]) * 3 != 14:
            print(pid, 'not match in 发送杠牌!', self.handStack[pid], self.fuluStack[pid])
            raise Exception
        # 标记 杠操作
        self.gangflag = True
        # 通知生成（暗杠 立直 胡牌 流局）
        self.allow_zimo(pid, mo)
        # 等待标记
        #self.waitFlag[pid] = self.mode

    def make_humsg(self,submsg):
        print(submsg)
        pid = submsg['from']
        hand = copy.copy(self.handStack[pid])
        tile = submsg['tile']
        if(tile[2] != '_'):
            # 他人胡牌，手牌需加上荣牌
            hand.append(tile)

        param = self.getPlayerParam(pid)
        param['haidi'] = 0
        if (self.yamaLast-14) == self.yamaPos:
            param['haidi'] = 1
            if tile[2] != '_':
                param['haidi'] = 2

        param['tianhu'] = 0
        if (self.diyizimo[pid] and tile[2] == '_'):
            param['tianhu'] = 2
            if(param['zhuangfeng'] == 0):
                param['tianhu'] = 1
        
        ptres = PtJudger.GetFen(hand,self.fuluStack[pid],tile,param)
        handstr = PaiMaker.GetSortPai(self.handStack[pid])
        print(pid,'胡了',handstr,tile,self.fuluStack[pid])
        print('宝牌:{} 里宝:{}'.format(self.bao, self.libao))
        if( not 'hupai' in ptres or ptres['hupai'] == None):
            print(param)
            raise Exception('无役和了')
        print(ptres['hupai'])
        print('{}符{}番 {}'.format(ptres['fu'],ptres['fanshu'],ptres['defen']))

        # 处理得分
        for i in range(4):
            # 将fenpei的风顺序  改为玩家顺序
            wind = self.playerWind[i]
            self.realfenpei[i] += ptres['fenpei'][wind]
            self.score[i] += ptres['fenpei'][wind]

        ptres['fenpei'] = self.realfenpei
        # 连庄判定
        if(self.playerWind[pid] == 0):
            self.lianzhuang = True

    def getActions(self):
        ''' possible for player
        '''
        #print(self.msgList)
        return copy.copy(self.msgList)
