#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models


try: filmID = sys.argv[1]
except: filmID = None

if filmID == None:
   print(f'Training model')
   X_train = np.load('inputs.npy')
   Y_train = np.load('outputs.npy')
   try: model = models.load_model('imdb.keras')
   except NameError: model = None
   if model == None:
      print('*'*80)
      print('Creating new model')
      print('*'*80)
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
   history = model.fit(X_train, Y_train, epochs=200, batch_size=32, validation_split=0.1)
# history = model.fit(X_train, Y_train, validation_data=(X_valid,Y_valid),
#                                       epochs=100, verbose=1)
                                         # callbacks=[Stopper])

   import matplotlib.pyplot as plt
   fig, ax = plt.subplots()
   ax.plot(history.history['loss'])
   fig.tight_layout()
   plt.show()

   model.save('imdb.keras')


   ################################
   filmID = 'tt2584384'
   print(f'Downloading data for {filmID}')
   import tools
   data = tools.generate_input(filmID)
   import process_data
   line = ','.join(data)
   X_test = process_data.data2vec(line)
   X_test = np.expand_dims(X_test, axis=0)
   y_pred = model.predict(X_test)
   print(f'Expected rating: {y_pred[0,0]}')
else:
   model = models.load_model('imdb.keras')
   print(f'Predicting rating for {filmID}')
   print(f'Downloading data for {filmID}')
   import tools
   data = tools.generate_input(filmID)
   import process_data
   line = ','.join(data)
   X_test = process_data.data2vec(line)
   X_test = np.expand_dims(X_test, axis=0)
   y_pred = model.predict(X_test)
   print(f'Expected rating: {y_pred[0,0]}')
