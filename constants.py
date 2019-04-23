## Japanese Mahjong constants
# list actions can be taken not in self turn
#JP_OUT_TURN_ACTION_LIST = ['CHI', 'PON', 'KAN_OUT', 'RON', 'CANCEL']
class JP_OUT_TURN_ACTION_LIST:
  CANCEL = 0
  CHI = 1
  PON = 2
  KAN_OUT = 3
  RON = 4

# list actions can be taken in self turn

#JP_TURN_ACTION_LIST = ['RICHI', 'TSUMO', 'KAN', 'CANCEL', 'KIRU', 'RICHI_KIRU']
class JP_TURN_ACTION_LIST:
  CANCEL = 0
  KIRU = 1
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
## End Japanese Mahjong
