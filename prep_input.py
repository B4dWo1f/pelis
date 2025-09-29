#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers, models


encoder = load_model('encoder_model.keras')

fname = '957c982a-0b20-4f53-9cfc-2872ba8fd9aa.csv'
df = pd.read_csv(fname)


# Number of countries
with open('countries.txt', 'r') as f:
   num_countries = len(f.read().strip().splitlines())
embedding_dim = 10   # size of the learned embedding
fname = 'inputs.csv'
X_train, Y_train = [],[]
with open(fname, 'r') as f:
   lines = f.read().strip().splitlines()
   for l in lines:
      ll = l.split(',')
      # Output
      filmID = ll[0]
      entry = df[df['Const'] == filmID]
      myrating = entry['Your Rating'].values[0]
      Y_train.append(myrating)
      # Input
      # ratings
      inps = list(map(float,ll[1:61]))
      inps = np.expand_dims(inps, axis=0)
      # country indices
      indices = np.array(list(map(int,ll[61:66])))
      v = np.zeros(num_countries)
      v[indices] = 1
      v = np.expand_dims(v, axis=0)
      vv = encoder.predict(v)
      X_train.append(np.squeeze(np.concatenate([inps,vv],axis=1)))

X_train = np.array(X_train)
Y_train = np.array(Y_train)
np.save('inputs',X_train)
np.save('outputs',Y_train)
print(X_train.shape)
print(Y_train.shape)

# Build the model
model = models.Sequential([
    layers.Input(shape=(70,)),
    layers.Dense(15, activation="relu"),
    layers.Dense(10, activation="relu"),
    layers.Dense(5, activation="relu"),
    layers.Dense(1, activation="linear")  # regression output
])

model.compile(optimizer='adam',
              loss='mse',
              metrics=['mae'])


model.summary()
history = model.fit(X_train, Y_train, epochs=50, batch_size=32, validation_split=0.1)
# history = model.fit(X_train, Y_train, validation_data=(X_valid,Y_valid),
#                                       epochs=100, verbose=1)
                                      # callbacks=[Stopper])

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(history.history['loss'])
fig.tight_layout()
plt.show()

# y_pred = model.predict(X_test)
model.save('imdb.keras')

