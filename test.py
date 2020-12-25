# import numpy as np
# import pandas as pd
# columns=list(range(20))
# q_table = pd.DataFrame(columns=columns,dtype=np.float64)
# print(q_table)
# state = 'aaa'
# if state not in q_table.index:
#     # append new state to q table
#     q_table = q_table.append(
#         pd.Series(
#             [0]*len(columns),
#             index=q_table.columns,
#             name=state,
#         )
#     )
# state_action = q_table.loc[state, :]
# dd = state_action[state_action == np.max(state_action)]

# print(dd)

from tool import PaiMaker
from tool import PtJudger
from tool import TingJudger
from tool import MianziMaker
handStack = ['0s']
fuluStack = ['s55-!', 'p777=', 'm67-8', 's234-', 'p111-']
mopai = '5s-'
handStack.append(mopai)
#print(PaiMaker.GetSortPai(handStack))
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
ptres = PtJudger.GetFen(handStack,fuluStack,mopai,param)
print(ptres)