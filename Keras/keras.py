import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os

CSV_PATH = 'E:/MAJ/tenhou/state/'

def build_model():
    """基本网络结构.
    """
    inputs = layers.Input(shape=(186,3,1,))
    x = layers.Conv2D(filters=16, kernel_size=3, strides=1, padding="same", activation='relu')(inputs)
    x = layers.Conv2D(filters=16, kernel_size=3, strides=1, padding="valid", activation='relu')(x)
    # x = layers.Flatten()(x)
    x = layers.MaxPooling2D(pool_size=(2,1), strides=None, padding="valid")(x)
    x = layers.Conv2D(filters=16, kernel_size=(3,1), strides=1, padding="same", activation='relu')(x)
    x = layers.Conv2D(filters=16, kernel_size=(3,1), strides=1, padding="valid", activation='relu')(x)
    x = layers.MaxPooling2D(pool_size=(2,1), strides=None, padding="valid")(x)
    x = layers.Conv2D(filters=32, kernel_size=(3,1), strides=1, padding="same", activation='relu')(x)
    x = layers.Conv2D(filters=32, kernel_size=(3,1), strides=1, padding="valid", activation='relu')(x)
    x = layers.GlobalMaxPooling2D()(x)
    predictions = layers.Dense(41, activation="relu")(x)

    model = Model(inputs=inputs, outputs=predictions)

    return model

def loadData_o():
    data = pd.DataFrame(columns=range(186), dtype=np.int)
    label = pd.DataFrame(columns=[186], dtype=np.int)
    n = 0
    for file in os.listdir(CSV_PATH):
        n += 1
        if(n > 10):
            break
        print(file)
        raw_data = pd.read_csv(CSV_PATH+file, sep=',', names=range(187), header=0)
        d = raw_data.iloc[:,:-1]
        data = data.append(d,ignore_index=True)
        l = raw_data.iloc[:,186:]
        label = label.append(l,ignore_index=True)

    return data,label

def loadData(N=None):
    data = pd.DataFrame(columns=range(187), dtype=np.float)
    n = 0
    for file in os.listdir(CSV_PATH):
        n += 1
        if(N and n > N):
            break
        print(file)
        raw_data = pd.read_csv(CSV_PATH+file, sep=',', names=range(187), header=0)
        data = data.append(raw_data,ignore_index=True)
    return data

data = loadData(100)
print(len(data))
train = data.sample(frac=0.8)
print( 'train:{}'.format(len(train)) )
train_data = train.iloc[:,:-1]
train_labels = train.iloc[:,186:]
test = data.sample(frac=0.2)
print( 'test:{}'.format(len(test)) )
test_data = test.iloc[:,:-1]
test_labels = test.iloc[:,186:]
# print(train_data)
# print(train_labels)

# model = build_model()
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(186,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),    
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(42, activation='softmax')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_data, train_labels, epochs=500)

test_loss, test_acc = model.evaluate(test_data,  test_labels, verbose=2)