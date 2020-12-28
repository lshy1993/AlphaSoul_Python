# from tool import PaiMaker
# from tool import PtJudger
# from tool import TingJudger
# from tool import MianziMaker
# import re


# handStack = ['0s']
# fuluStack = ['p777=', 'm67-8', 's234-', 'p111-']
# mopai = '5s-'
# handStack.append(mopai)

# # handStack = ['5m', '5m', '2p', '3p', '4p', '3s', '5s', '4s=']
# # fuluStack = ['p456-', 's789-']
# # mopai = '4s='
# # handStack.append(mopai)

# # handStack = [ "1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]
# # fuluStack = []
# # mopai = '1z-'
# # handStack.append(mopai)


# #print(PaiMaker.GetSortPai(handStack))
# param = {
#     'zhuangfeng': 0,
#     'menfeng': 0,
#     'baopai': ['1z'],
#     'fubaopai': [],
#     'changbang': 0,
#     'lizhibang': 0,
#     'lizhi':      0,
#     'yifa':       0,
#     'qianggang':  False,
#     'lingshang':  False,
#     'haidi':      0,
#     'tianhu':     0
# }
# ptres = PtJudger.GetFen(handStack,fuluStack,mopai,param)
# print(ptres)

# import tensorflow as tf
# mnist = tf.keras.datasets.mnist

# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0

# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Dense(10, activation='softmax')
# ])

# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# model.fit(x_train, y_train, epochs=5)

# model.evaluate(x_test,  y_test, verbose=2)

import numpy as np
import pandas as pd

import os

CSV_PATH = 'E:/MAJ/tenhou/csv/'

def loadData():
    data = pd.DataFrame(columns=range(186), dtype=np.int8)
    label = []
    for file in os.listdir(CSV_PATH):
        print(file)
        raw_data = pd.read_csv(CSV_PATH+file, sep=',', header=0, index_col=0)
        rows = len(raw_data)
        narray = []
        for k in range(int(rows/10)):
            print(k)
            state = raw_data.iloc[k*10:k*10+10]
            # print(state)
            label.append(state.iloc[0,-1])
            narray.extend(state.iloc[0,:12])
            narray.extend(state.iloc[1,:14])
            for i in range(4):
                narray.extend(state.iloc[2+i*2,:16])
                narray.extend(state.iloc[2+i*2+1,:])
            # print(narray)
            data = data.append(narray,ignore_index=True)
        return data,label
    
data,label = loadData()
print(data)
print(label)