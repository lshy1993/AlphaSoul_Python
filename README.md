# alphasoul_python

# Envrionment Variables 环境总变量
|变量名|类型|说明|附|
|-|-|-|-|
|yama| string[] | 牌山代码，随机洗牌生成 ||
|handStack| string[4][] | 4个玩家手牌列 ||
|riverStack| string[4][] | 4个玩家牌河列 ||
|fuluStack| string[4][] | 4个玩家副露牌列 ||
|bao| string[] | 宝牌指示牌 ||
|libao| string[] | 里宝牌指示牌 ||
|yamaPos| int | 当前的牌顶位置 ||
|yamaLast| int | 海底牌位置 ||
|baoPos| int | 宝牌翻开位置 ||
|changfeng| int | 场（庄）风（0: 东 1:南 2: 西 3:北） ||
|playerWind| int[4] | 4个玩家的自风 | 例`[3,0,1,2]`代表 0号玩家为北风，1号玩家为东风 |
|playerLizhi| int[4] | 4个玩家的立直状态（0:无 1:立直 2:两立直） | |
|diyizimo| bool[4] | 4个玩家的第一自摸状态 | |
|yifa| bool[4] | 4个玩家的一发状态 | |
|changbang| int | 寄存的场棒（连庄）数 | |
|lizhibang| int | 寄存的立直棒数 | |
|score| int[] | 4个玩家的分数 ||
|curWind| int | 轮到的玩家编号 ||
|qinjia| int | 当前坐庄（东风）的玩家编号 ||
|endSection| bool | 是否结束当前的风 ||
|lianzhuang| bool | 是否连庄 ||

# State 状态（玩家所见）
|变量名|类型|说明|附|
|-|-|-|-|
|seat| int | 玩家编号 ||
|zifeng| int | 自风 ||
|handStack| string[] | 玩家手牌代码 ||
|riverStack| string[4][] | 4个玩家牌河列 ||
|fuluStack| string[4][] | 4个玩家副露牌列 ||
|bao| string[] | 宝牌指示牌 ||
|restyama| int | 剩余牌数 ||
|changfeng| int | 场（庄）风（0: 东 1:南 2: 西 3:北） ||
|playerLizhi| int[4] | 4个玩家的立直状态（0:无 1:立直 2:两立直） | |
|changbang| int | 寄存的场棒（连庄）数 | |
|lizhibang| int | 寄存的立直棒数 | |
|score| int[] | 4个玩家的分数 ||
|curWind| int | 轮到的玩家编号 ||
|qinjia| int | 当前坐庄（东风）的玩家编号 ||
|paishu| dict[] | 除了可见牌外，理论剩余的牌数目 ||

# GameFlow

# Server端消息
## Operation 玩家操作
|type|含义|combination|说明|
|-|-|-|-|
|1|切牌| string[] | 禁手牌 |
|2|吃| string | 吃牌可能，例如`'2m|3m|4m-'` |
|3|碰| string | 碰牌可能，例如`'2m|2m|2m+'` |
|4|暗杠| string | 暗杠 `'2m|2m|2m|2m_'` |
|5|明杠| string | 明杠例如`'m222|2m_'` |
|6|加杠| ['2m|3m|4m-',2][] | |
|7|立直| ['2m|3m|4m-',2][] | |
|8|自摸| string | 自摸牌，例 `'2m_'` |
|9|胡| string | 胡牌，例如 `'2m+'` |
|10|九种| - | |
|11|拔北| - | |


## ActionNewRound 新起一轮牌局
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionNewRound'|消息类型|
|seat|int|是|[1,2,3,4]|玩家的编号|
|qinjia|int|是|[1,2,3,4]|庄家位置|
|changfeng|int|是|[1,2,3,4]|场风 1：东 2：南 3：西 4：北|
|zifeng|int|是|[1,2,3,4]|该玩家的门风 1：东 2：南 3：西 4：北|
|changbang|int|是|-|场棒数目|
|lizhibang|int|是|-|寄存的立直棒数目|
|score|int[]|是|-|当前所有玩家的分数|
|bao|string[]|是|-|翻开的宝牌指示牌|
|handStack|string[]|是|-|发给玩家的手牌 参照麻将牌编码|

## ActionDealTile 摸牌消息
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionDealTile'|消息类型|
|seat|int|是|[1,2,3,4]|玩家的编号|
|restyama|int|是|-|剩余牌数|
|tile|string| |-|发给玩家的牌，非目标玩家不可见|
|operation| object[] | | |该玩家可能产生的操作 详见operation|

## ActionDiscardTile 切牌消息
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionDiscardTile'|消息类型|
|seat|int|是|[1,2,3,4]|玩家的编号|
|tile|string| |-|玩家打出的牌|
|tilepos|int|是|-|切牌的位置|
|is_wliqi|bool| |-|是否宣告两立直|
|is_liqi|bool| |-|是否宣告立直|
|restyama|int| |-|剩余牌数|
|operation| object[] | | |该玩家可能产生的操作 详见operation|

## ActionChipenggang 吃碰杠 （他人）副露消息
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionChiPengGang'|消息类型|
|seat|int|是|[1,2,3,4]|副露玩家的编号|
|tile| string[] |是|-|副露牌|
|from| int[] |是|-|副露牌的来源玩家编号|
|opt|int| |-|副露类型（2:吃 3:碰 5:明杠）|
|operation| object[] | | |副露的玩家，将会收到切牌信号 详见operation|

## ActionAngangJiagang 暗杠加杠 （自己）副露消息
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionChiPengGang'|消息类型|
|seat|int|是|[1,2,3,4]|副露玩家的编号|
|tile| string[] |是|-|副露牌|
|from| int[] |是|-|副露牌的来源玩家编号|
|opt|int| |-|副露类型（2:吃 3:碰 5:明杠）|
|operation| object[] | | |副露的玩家，将会收到切牌信号 详见operation|

## ActionHule 荣和自摸消息
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionHule'|消息类型|
|data| object[] |是|-| 多（单）人的荣和消息队列|
|-|-|-|-|-|
|type| string |是| `['hu','zimo']` |副露牌|
|from| int |是|-|荣和/自摸的玩家编号|
|tile| object[] | |-| [胡了牌，类型（8:自摸 9:荣和）] 详见operation|

## ActionLiuju 流局消息
|字段名|类型|是否必须|可选值|说明|
|-|-|-|-|-|
|type|string|是|'ActionLiuju'|消息类型|
|opt|int|是|-| 流局类型（1:四家立直 2:荒牌流局 3:四杠散了）|
|type| string |是| `['hu','zimo']` |副露牌|
|from| int |是|-|荣和/自摸的玩家编号|
|tile| object[] | |-| [胡了牌，类型（8:自摸 9:荣和）] 详见operation|