#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from time import sleep
import numpy as np
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_genres(url, debug=False):
   with sync_playwright() as p:
      if debug: browser = p.firefox.launch(headless=False)
      else: browser = p.firefox.launch(headless=True)
      page = browser.new_page()
      page.goto(url)

      html = page.content()
      soup = BeautifulSoup(html, "html.parser")
      genres_bar = soup.find('div',{'data-testid':'interests'})
      genres_list = genres_bar.find('div', {'class': 'ipc-chip-list__scroller'})
      genres = []
      for a in genres_list.find_all('a'):
         genres.append(a.text)
      browser.close()
   return genres



def extract_ratings(page):
   """
   extract the percentage of votes form the active histogram
   """
   html = page.content()
   soup = BeautifulSoup(html, "html.parser")
   graph = soup.find('div',{'class':'VictoryContainer'})
   hist = graph.find_all('g')[-1]
   ratings = []
   for p in hist.find_all('path'):
      pct = p['aria-label'].split()[2]
      pct = pct.replace('%','')
      ratings.append(float(pct))
   #print(np.average(range(1,11), weights=ratings))
   return ratings


def get_ratings(url, debug=False):
   """
   scraps imdb's rating site for disagregate data
   returns a 6x10 matrix where each row is the percentage of votes for
   [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] rating
   1st row is all the data disagregated, I think
   the rest of the rows are the 5 top countries with most votes
   an array with the number of more voted countries is returned, the index
   is the order in list: 'countries.txt'
   """
   # debug = True
   RATINGS = []
   with sync_playwright() as p:
      if debug: browser = p.firefox.launch(headless=False)
      else: browser = p.firefox.launch(headless=True)
      page = browser.new_page()
      page.goto(url)
      # if debug: page.pause()

      # Close cookies
      try: page.get_by_test_id("reject-button").click()
      except: pass

      # General ratings
      ratings = extract_ratings(page)
      RATINGS.append(ratings)
      # print('General:',ratings)
      html = page.content()
      soup = BeautifulSoup(html, "html.parser")
      filters = soup.find('div', {'class':'histogram-filter-chipgroup ipc-chip-group'})
      buttons = filters.find_all('button')
      countries = [b.text for b in buttons]

      for country in countries:
         page.get_by_role("button", name=f"Select {country} filter").click()
         sleep(1)
         ratings = extract_ratings(page)
         RATINGS.append(ratings)
         # print(f'{country}: {ratings}')
      browser.close()
      with open('countries.txt', 'r') as f:
         lines = f.read().strip().splitlines()
         lines = [x.split(',')[0] for x in lines]
         n = len(lines)
         countries_n = [lines.index(c) for c in countries]
   return np.array(RATINGS), np.array(countries_n)


filmID = 'tt30645201' # honey dont
# filmID = 'tt31036941' # Jurasic world
from random import choice,shuffle
import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
films = os.popen('cat test.csv | cut -d "," -f 1').read().strip().split()
# shuffle(films)


from tqdm import tqdm
ff = open('inputs.csv','a')
fdone = open('done.csv','a')

all_genres = []
i = 1
for filmID in tqdm(films[i:]):
   # filmID = choice(films)

   done = os.popen(f'grep {filmID} done.csv').read().strip()
   if len(done) > 0: 
      print(f'{filmID} already done')
      continue
   url = f'https://www.imdb.com/title/{filmID}'
   # print(url)
   R,c = get_ratings(f'{url}/ratings')
   # print(R)
   # print(R.flatten())
   # print(c)
   # print(R)
   # print(c)
   # print('')
   genres = get_genres(f'{url}')
   # print(genres)
   inps = [filmID]
   inps += [str(r) for r in R.flatten()]
   inps += [str(x) for x in c]
   inps += genres
   txt = ','.join(inps)
   ff.write(txt+'\n')
   ff.flush()
   fdone.write(filmID+'\n')
   # all_genres += genres
   i += 1
   if os.path.isfile('STOP'): break
ff.close()
fdone.close()

# for g in sorted(set(all_genres)):
#    print(g)
# print(f'Next: {i}')
