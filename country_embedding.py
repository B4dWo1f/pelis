#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np

# Number of countries
with open('countries.txt', 'r') as f:
   num_countries = len(f.read().strip().splitlines())
embedding_dim = 10   # size of the learned embedding



fname = 'inputs.csv'
# df = pd.read_csv(fname, header=None)
X_train = []
with open(fname, 'r') as f:
   lines = f.read().strip().splitlines()
   for l in lines:
      # print(l)
      ll = l.split(',')
      indices = np.array(list(map(int,ll[61:66])))
      v = np.zeros(num_countries)
      v[indices] = 1
      X_train.append(v)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
import tensorflow as tf
from tensorflow.keras import layers, models




# Encoder
input_layer = layers.Input(shape=(num_countries,))
encoded = layers.Dense(embedding_dim, activation="relu")(input_layer)

# Decoder
decoded = layers.Dense(num_countries, activation="sigmoid")(encoded)

# Autoencoder model
autoencoder = models.Model(input_layer, decoded)

# Encoder model (to extract embeddings later)
encoder = models.Model(input_layer, encoded)

# Compile
autoencoder.compile(optimizer="adam", loss="binary_crossentropy")

X_train = np.array(X_train)
print(X_train.shape)
# Example: X_train is a (num_samples, num_countries) binary 5-hot matrix
# Each row has exactly 5 ones (the countries that voted most for that film)
# Fit the autoencoder
history = autoencoder.fit(X_train, X_train, epochs=5000,
                                            batch_size=32,
                                            validation_split=0.1)

err = history.history['loss']
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(err)
fig.tight_layout()
plt.show()

# After training, get embeddings
# embeddings = encoder.predict(X_train)
encoder.save('encoder_model.keras')
# print(embeddings)

