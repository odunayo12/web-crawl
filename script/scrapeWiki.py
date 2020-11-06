# %%
# pyright: reportUnboundVariable=false
import urllib
import urllib.request
#import urllib3
from bs4 import BeautifulSoup
import csv
import pandas as pd
from dateutil.parser import ParserError
import re
import time
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# %%
startTime = datetime.now()


def make_soup(url):
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data


# %%
make_soup_bowl = make_soup(
    "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Germany")

# %%
for made_soup in make_soup_bowl.find("div", {"class": "mw-parser-output"}).finAll("table"):
    for every_recipe in made_soup.finAll("li"):
        print(every_recipe)
# %%
for each_li in make_soup_bowl:
    state_text = each_li.text
    print(state_text)

# %%
recipee_mall = make_soup_bowl.find("div", {"class": "mw-parser-output"})

# %%
recipee_table = recipee_mall.findAll('table')[0:25]
# %%
tasty_dish = []
for recipee_list in recipee_table:
    for spice_list in recipee_list.findAll("li"):
        tasty_soup = spice_list.text
        tasty_dish.append(tasty_soup)

# %%
pd.DataFrame(tasty_dish).to_csv(r"../data/german_towns.csv")
print(datetime.now() - startTime)
