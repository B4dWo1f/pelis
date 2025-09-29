#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import pandas as pd

df = pd.read_csv('957c982a-0b20-4f53-9cfc-2872ba8fd9aa.csv')

fname = '../myIMDb/inputs.csv'
with open(fname,'r') as f:
   lines = f.read().strip().splitlines()

fname = 'movies.csv'
with open(fname,'w') as f:
   for l in lines:
      ll = l.split(',')
      filmID = ll[0]
      print(filmID)
      myrating = df[df['Const']==filmID]['Your Rating'].values[0]
      f.write(','.join(ll+[str(myrating)])+'\n')
      f.flush()
