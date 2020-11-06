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
import json
import sys

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


#sys.modules[__name__] = make_tasty_soup


def split_url_by_value(url, iter_rator):
    split_url = url.rsplit("&display", 1)
    parsed_url = f"{split_url[0]}{str(iter_rator)}&display{split_url[1]}"
    return parsed_url

# %%
# phd degree


phd_page_range = list(range(0, 231, 10))
phd_souped_page = []
phd_url = f"https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&degree%5B%5D=3&langDeAvailable=&langEnAvailable=&lang%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&dur%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list&fee=&bgn%5B%5D=&dat%5B%5D="

for pages in phd_page_range:
    parsed_url = split_url_by_value(phd_url, pages)
    print(f"Scrapping: page {int(pages/10 + 1)}")
    # print(parsed_url)
    watery_soup = make_tasty_soup(parsed_url)
    phd_souped_page.append(watery_soup)


# %%
startTime = datetime.now()
csv_data = {}
item_no = 0
for phd_soup in phd_souped_page:
    for d in phd_soup.findAll("div", {"class": "c-result-list__content c-masonry js-result-list-content"}):
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
            relevant_h3 = (
                "h3", {"class": "c-ad-carousel__highlight u-fs-default mb-0 mt-3"})

            if len(ul.findAll("li")) != 4 and "Fin" in ul.findAll("li")[0].find(relevant_h3):
                finan_support = ul.findAll("li")[0].find(relevant_span).text
                lang_of_instr = ""
                superv_type = ul.findAll("li")[1].find(relevant_h3).text
                semester_beginning = "inquire"
                dura_of_study = ""
            elif len(ul.findAll("li")) > 3 and "Fin" not in ul.findAll("li")[0].find(relevant_h3):
                finan_support = "inquire"
                lang_of = [lang for lang in ul.findAll(
                    "li")[0].findAll(relevant_span)]
                lang_of_instr = ", ".join([lang.text for lang in lang_of])
                semester_beg = [beg for beg in ul.findAll(
                    "li")[1].findAll(relevant_span)]
                semester_beginning = ", ".join(
                    [be.text for be in semester_beg])
                dura_of_study = ul.findAll("li")[2].find(relevant_span).text
                superv_type = "Structured research and supervision"

            item_no += 1

            csv_data[item_no] = [course_type,
                                 course_name,
                                 course_link,
                                 uni_name,
                                 uni_city,
                                 finan_support,
                                 lang_of_instr,
                                 dura_of_study,
                                 semester_beginning,
                                 superv_type]


print(json.dumps(csv_data, indent=2))
# %%
phd_csv_df = pd.DataFrame.from_dict(csv_data, orient='index',
                                    columns=["course_type",
                                             "course_name",
                                             "course_link",
                                             "uni_name",
                                             "uni_city",
                                             "finan_support",
                                             "lang_of_instr",
                                             "dura_of_study",
                                             "semester_beginning",
                                             "superv_type"])

phd_csv_df.to_csv(r"../data/phd_csv_df.csv")
print(datetime.now() - startTime)
# %%
