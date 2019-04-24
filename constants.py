##### Japanese Mahjong constants
# list actions can be taken not in self turn
class JP_OUT_TURN_ACTION_LIST:
  CANCEL = 0
  CHI = 1
  PON = 2
  KAN_OUT = 3
  RON = 4
  
# list actions can be taken in self turn
class JP_TURN_ACTION_LIST:
  CANCEL = 0
  DISCARD = 1
  KAN = 2
  RICHI = 3 # 立直 = 切牌 ?
  TSUMO = 4
  NAGARE = 5 # 流局

# list tiles type in japanese mahjong
JP_TILES_TYPE = ['P', 'M', 'S', 'Z']
# list tiles code in japanese mahjong
JP_TILES_CODE = [
  "1m","2m","3m","4m","5m","6m","7m","8m","9m",
  "1p","2p","3p","4p","5p","6p","7p","8p","9p",
  "1s","2s","3s","4s","5s","6s","7s","8s","9s",
  "1z","2z","3z","4z","5z","6z","7z"
]
# list tiles display for debug
JP_TILES_DISPLAY = [
  "一","二","三","四","五","六","七","八","九",
  "①","②","③","④","⑤","⑥","⑦","⑧","⑨",
  "１","２","３","４","５","６","７","８","９",
  "東","南","西","北",
  "白","發","中"
]

# english terms reference:
# https://www.mahjongsets.co.uk/glossary-mahjong.html
# DISCARD = 切牌 切る
# CHI = 吃　チー 
# PON = 碰　ポン
# KAN = 杠　カン
# RON = 荣和　ロン
# TSUMO = 自摸　ツモ
# RIICHI = 立直　リーチ
# PASS = 放弃切牌以外权利 切る以外やめる
JP_ACTION_LIST = ['CHI', 'PON', 'KAN', 'RON', 'TSUMO', 'PASS', 'RIICHI', 'DISCARD']

# list tiles in japanese mahjong
# p = 筒 circle
# m = 万 character
# s = 条 bamboo
# ESWN = 风牌 Wind
# R = 中 Center
# G = 发 Green
# _ = 白 White
JP_TILES_DICT = {
    '1p': 4, '2p': 4, '3p': 4, '4p': 4, '5p': 4, '6p': 4, '7p': 4, '8p': 4, '9p': 4,
    '1m': 4, '2m': 4, '3m': 4, '4m': 4, '5m': 4, '6m': 4, '7m': 4, '8m': 4, '9m': 4,
    '1s': 4, '2s': 4, '3s': 4, '4s': 4, '5s': 4, '6s': 4, '7s': 4, '8s': 4, '9s': 4,
    'E': 4, 'S': 4, 'W': 4, 'N': 4, 
    'R': 4, 'G': 4, '_': 4
}

# list of scoring
# Refer to:
# https://en.wikipedia.org/wiki/Japanese_Mahjong_yaku
# key  : value
# name : (hanValue, hanValueNotMenzen) 
# name : (番数, 非门清番数)
# 
# notice if not MENZEN and substituted han value == 0, then it is a MENZENCHIN nomi yaku
JP_SCORE_YAKU_DICT = {
    # special yaku
    'RIICHI_YAKU':              (1, 0),                      # 立直 リチ
    'CHIITOI':                  (2, 0),                      # 七对子 七対子
    'NAGASH_MANKAN':            ('MANKAN', 'MANKAN'),        # 流局满贯 流し満貫
    # luck yaku
    'MENZEN_TSUMO':             (1, 0),                      # 门清自摸 門前ツモ 
    'IPPATSU':                  (1, 0),                      # 一发 一発
    'HAITEI':                   (1, 1),                      # 海底捞月 海底摸月 
    'HOUTEI':                   (1, 1),                      # 河底捞鱼 河底撈魚
    'RINSHAN':                  (1, 1),                      # 岭上开花 嶺上開花
    'CHANKAN':                  (1, 1),                      # 抢杠 槍槓
    'W_RIICHI':                 (2, 0),                      # 两立直 ダブルリーチ
    # sequence yaku
    'PINFU':                    (1, 0),                      # 平和
    'IIPPEIKOU':                (1, 0),                      # 一杯口
    'SANSHOKU_DOUJUN':          (2, 1),                      # 三色同顺
    'ITTSUU':                   (2, 1),                      # 一气通贯
    'RYANPEIKOU':               (3, 0),                      # 两杯口
    # triples yaku
    'TOITOI':                   (2, 2),                      # 对对胡
    'SAN_ANKO':                 (2, 2),                      # 三暗刻
    'SANSHOKU_DOUKO':           (2, 2),                      # 三色同刻
    'SAN_KANTSU':               (2, 2),                      # 三杠子
    # terminal/honor tiles yaku
    'TANYAO':                   (1, 1),                      # 断幺
    'YAKUHAI':                  (1, 1),                      # 役牌
    'CHANTA':                   (2, 1),                      # 带幺九
    'JUNCHAN':                  (3, 2),                      # 纯全带幺九
    'HONROU':                   (2, 2),                      # 混老头
    'SHOU_SANGEN':              (2, 2),                      # 小三元
    # suit based yaku
    'HONIISOU':                 (3, 2),                      # 混一色
    'CHINIISOU':                (6, 5),                      # 清一色
    # yakuman
    'KOKUSHI_MUSOU':            ('YAKUMAN', 0),              # 国士无双
    'KOKUSHI_MUSOU_13':         ('D_YAKUMAN', 0),            # 国士无双十三面
    'SI_ANKO':                  ('YAKUMAN', 0),              # 四暗刻
    'SI_ANKO_TANKI':            ('D_YAKUMAN',0),             # 四暗刻单骑
    'DAI_SANGEN':               ('YAKUMAN', 'YAKUMAN'),      # 大三元
    'SHOU_SUUSHII':             ('YAKUMAN', 'YAKUMAN'),      # 小四喜
    'DAI_SUSSHII':              ('D_YAKUMAN', 'D_YAKUMAN'),  # 大四喜
    'TSUUIISOU':                ('YAKUMAN', 'YAKUMAN'),      # 字一色
    'CHINROUTOU':               ('YAKUMAN', 'YAKUMAN'),      # 清老头
    'RYUUIISOU':                ('YAKUMAN', 'YAKUMAN'),      # 绿一色
    'CHUUREN_POUTOU':           ('YAKUMAN', 0),              # 九莲宝灯
    'JUNSEI_CHUUREN_POUTOU':    ('D_YAKUMAN', 0),            # 纯正九莲宝灯
    'SUU_KANTSU':               ('YAKUMAN', 'YAKUMAN'),      # 四杠子
    'TENHOU':                   ('YAKUMAN', 0),              # 天和
    "CHIIHOU":                  ('YAKUMAN', 0),              # 地和
    #'RENHOU':                   'YAKUMAN',              # 人和
}

##### End Japanese Mahjong