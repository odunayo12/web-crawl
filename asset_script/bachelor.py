# %%
# pyright: reportUnboundVariable=false

import os
import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import datetime
from urllib.parse import urlparse
import time
import re
from dateutil.parser import ParserError
import pandas as pd
import csv
from bs4 import BeautifulSoup
import urllib.request
import urllib
#from script.scrap_daad import make_tasty_soup
import sys
sys.path.append(
    r"C:\Users\rotim\OneDrive - bwedu\Web Developmnet\data-analysis\my-study-exp\script")
#from .scrap_daad import make_tasty_soup, split_url_by_value
#import make_tasty_soup
#import urllib3


# %%
def make_tasty_soup(url):
    """
    takes url and makes a tasty soup from it.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    return soup


sys.modules[__name__] = make_tasty_soup


def split_url_by_value(url, iter_rator):
    split_url = url.rsplit("&display", 1)
    parsed_url = f"{split_url[0]}{str(iter_rator)}&display{split_url[1]}"
    return parsed_url  # %%


# %%
# Bachelors
bachelor_page_range = list(range(0, 220, 10))
bachelor_souped_page = []
bachelor_url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&degree%5B%5D=1&langDeAvailable=&langEnAvailable=&lang%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&dur%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list&fee=&bgn%5B%5D="

for pages in bachelor_page_range:
    parsed_url = split_url_by_value(bachelor_url, pages)
    print(f"Scrapping: page {int(pages/10 + 1)}")
    # print(parsed_url)
    watery_soup = make_tasty_soup(parsed_url)
    bachelor_souped_page.append(watery_soup)
# %%
csv_data = {}
item_no = 0
for masters_soup in bachelor_souped_page:
    for d in masters_soup.findAll("div", {"class": "c-result-list__content c-masonry js-result-list-content"}):
        for soup in d.findAll("div", {"class": "c-ad-carousel c-masonry__item c-masonry__item--result-list mb-5"}):
            course_type = soup.find(
                "p", {"class": "c-ad-carousel__course m-0"}).text
            course_name = soup.find(
                "span", {"class": "js-course-title d-none d-sm-block"}).text
            slug_ = "https://www2.daad.de"
            course_link = slug_ + soup.find(
                "a", {"class": "list-inline-item mr-0 js-course-detail-link"})['href']
            uni_name = soup.find("span", {
                "class": "c-ad-carousel__subtitle c-ad-carousel__subtitle--small js-course-academy"}).text
            uni_name = re.compile(r"•").sub("", uni_name)
            uni_city = soup.find("span", {
                "class": "c-ad-carousel__subtitle c-ad-carousel__subtitle--location c-ad-carousel__subtitle--small"}).text

            # variables
            ul = soup.find("ul", {
                "class": "c-ad-carousel__data-list c-ad-carousel__data-list--not-colored p-0"})
            relevant_span = ("span", {
                "class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"})
            online_course = soup.find(
                "p", {"class": "c-badge c-badge--bottom"})

            if bool(online_course) == False and len(ul.findAll("li")) == 4:
                online_course_elemen = ""
                online_subject_el = ""
                oline_e_learning_type = ""
                tution_fee = ul.findAll("li")[0].find(relevant_span).text
                lang_of = [lang for lang in ul.findAll(
                    "li")[1].findAll(relevant_span)]
                lang_of_instr = ", ".join([lang.text for lang in lang_of])
                semester_beg = [beg for beg in ul.findAll(
                    "li")[2].findAll(relevant_span)]
                semester_beginning = ", ".join(
                    [be.text for be in semester_beg])
                dura_of_study = ul.findAll("li")[3].find(relevant_span).text
            elif bool(online_course) == True and len(ul.findAll("li")) == 4:
                online_course_elemen = online_course.text.strip()
                online_subject_el = ""
                oline_e_learning_type = ""
                tution_fee = ul.findAll("li")[0].find(relevant_span).text
                lang_of = [lang for lang in ul.findAll(
                    "li")[1].findAll(relevant_span)]
                lang_of_instr = ", ".join([lang.text for lang in lang_of])
                semester_beg = [beg for beg in ul.findAll(
                    "li")[2].findAll(relevant_span)]
                semester_beginning = ", ".join(
                    [be.text for be in semester_beg])
                dura_of_study = ul.findAll("li")[3].find(relevant_span).text
            # elif bool(online_course) == True and len(ul.findAll("li")) == 3:
            #     online_course_elemen = online_course.text.strip()
            #     online_subject_el = ""
            #     oline_e_learning_type = ""
            #     tution_fee = ""
            #     lang_of = [lang for lang in ul.findAll(
            #         "li")[1].findAll(relevant_span)]
            #     lang_of_instr = ", ".join([lang.text for lang in lang_of])
            #     lang_of_instr = ul.findAll("li")[0].find(relevant_span).text
            #     semester_beg = [beg for beg in ul.findAll(
            #         "li")[1].findAll(relevant_span)]
            #     semester_beginning = ", ".join(
            #         [be.text for be in semester_beg])
            #     dura_of_study = ul.findAll("li")[2].find(relevant_span).text
            else:
                online_course_elemen = ""
                online_subject_el = ""
                oline_e_learning_type = ""
                tution_fee = ""
                lang_of = [lang for lang in ul.findAll(
                    "li")[0].findAll(relevant_span)]
                lang_of_instr = ", ".join([lang.text for lang in lang_of])
                semester_beg = [beg for beg in ul.findAll(
                    "li")[1].findAll(relevant_span)]
                semester_beginning = ", ".join(
                    [be.text for be in semester_beg])
                dura_of_study = ul.findAll("li")[2].find(relevant_span).text

            item_no += 1

            csv_data[item_no] = [course_type,
                                 course_name,
                                 course_link,
                                 uni_name,
                                 uni_city,
                                 tution_fee,
                                 lang_of_instr,
                                 dura_of_study,
                                 semester_beginning,
                                 online_course_elemen,
                                 online_subject_el,
                                 oline_e_learning_type]


print(json.dumps(csv_data, indent=2))
bachelor_csv_df = pd.DataFrame.from_dict(csv_data, orient='index',
                                         columns=["course_type",
                                                  "course_name",
                                                  "course_link",
                                                  "uni_name",
                                                  "uni_city",
                                                  "tution_fee",
                                                  "lang_of_instr",
                                                  "dura_of_study",
                                                  "semester_beginning",
                                                  "online_course_elemen",
                                                  "online_subject_el",
                                                  "oline_e_learning_type"])
# %%
bachelor_csv_df.to_csv(r"../data/bachelor_csv_df.csv")
