#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
This script reads movies.csv and produces inputs.npy and output.npy
"""

import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers, models


encoder = load_model('encoder_model.keras')

# Number of countries
with open('countries.txt', 'r') as f:
   num_countries = len(f.read().strip().splitlines())


def data2vec(line):
   """
   given a row from movies.csv return the numerical vector for NN input
   this step includes embeddings
   """
   ll = line.split(',')
   filmID = ll[0]
   # ratings
   try: inps = list(map(float,ll[1:61]))  # less than 5 counties
   except: raise
   inps = np.expand_dims(inps, axis=0)
   # country indices
   indices = np.array(list(map(int,ll[61:66])))
   v = np.zeros(num_countries)
   v[indices] = 1
   v = np.expand_dims(v, axis=0)
   vv = encoder.predict(v)
   return np.squeeze(np.concatenate([inps,vv],axis=1))



if __name__ == '__main__':
   fname = 'movies.csv'
   X_train, Y_train = [],[]
   with open(fname, 'r') as f:
      lines = f.read().strip().splitlines()
      for l in lines:
         ll = l.split(',')
         filmID = ll[0]
         # Output
         myrating = float(ll[-1])
         # Input
         # ratings
         try: inps = list(map(float,ll[1:61]))  # less than 5 counties
         except: continue
         inps = np.expand_dims(inps, axis=0)
         # country indices
         indices = np.array(list(map(int,ll[61:66])))
         v = np.zeros(num_countries)
         v[indices] = 1
         v = np.expand_dims(v, axis=0)
         vv = encoder.predict(v)
         X_train.append(np.squeeze(np.concatenate([inps,vv],axis=1)))
         Y_train.append(myrating)

   X_train = np.array(X_train)
   Y_train = np.array(Y_train)
   np.save('inputs',X_train)
   np.save('outputs',Y_train)
   print(X_train.shape)
   print(Y_train.shape)
