#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
This scripts reads the data from the imdb.com downloaded ratings and
downloads the relevant data for each film, saving all the info in
movies.csv
the columns are;
filmID,[%10,%9,%8,%7,%6,%5,%4,%3,%2,%1][%][%][%][%][%][country codes][genres][myrating]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^
        Disaggregated histogram of     ratings histograms
        ratings                        for the 5 top voting
                                       countries
"""

import os
import pandas as pd
import tools

fratings = '957c982a-0b20-4f53-9cfc-2872ba8fd9aa.csv'
df = pd.read_csv(fratings)
df = df[df['Title Type']=='Movie']
done = pd.read_csv('movies.csv', header=None)
done = done[0].values

ff = open('movies.csv','a')
for index,row in df.iterrows():  #['Const'].values:
   filmID = row['Const']
   if filmID in done: continue
   print(filmID)
   myrating = row['Your Rating']
   data = tools.generate_input(filmID)
   data.append(str(myrating))
   ff.write(','.join(data)+'\n')
   ff.flush()
   if os.path.isfile('STOP'): break
ff.close()
