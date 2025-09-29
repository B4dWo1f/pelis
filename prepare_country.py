#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright



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
      html = page.content()
      soup = BeautifulSoup(html, "html.parser")
      filters = soup.find('div', {'class':'histogram-filter-chipgroup ipc-chip-group'})
      buttons = filters.find_all('button')
      countries = [b.text for b in buttons]

      browser.close()
      with open('countries.txt', 'r') as f:
         lines = f.read().strip().splitlines()
         lines = [x.split(',')[0] for x in lines]
         n = len(lines)
         countries_n = [lines.index(c) for c in countries]
   return countries_n
   # return np.array(countries_n)


films = os.popen('cat test.csv | cut -d "," -f 1').read().strip().split()
print('filmID,country1,country2,country3,country4,country5')
for filmID in films[1:3]:
   url = f'https://www.imdb.com/title/{filmID}'
   countries = get_ratings(f'{url}/ratings')
   countries = [filmID] + [str(x) for x in countries]
   print(','.join(countries))
