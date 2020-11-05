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
print(datetime.now() - startTime)


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
# %%


# %%
daad__soup_bowl = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=1&degree%5B%5D=2&degree%5B%5D=3&degree%5B%5D=7&degree%5B%5D=5&degree%5B%5D=6&lang%5B%5D=2&lang%5B%5D=4&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dur%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list"

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
# %%


def delicious_soup(page_range, url):
    """
    souped_page is an empty array
    """
    for target_list in page_range:
        split_url = url.rsplit("&display", 1)
        # +"{"+"}"+"&display"+
        parsed_url = f"{split_url[0]}{str(target_list)}&display{split_url[1]}"
        #parsed_url = f"" + (split_url[0] + "{" + str(target_list)+"}" + "&display" + split_url[1])
        print(f"Scrapping: page {int(target_list/10 + 1)}")
        print(parsed_url)

# %%


# %%
# https://www.youtube.com/watch?v=ODa8KCMdc-g&ab_channel=GoTrained
q = [10, 20, 30]
for target_list in q:
    url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=1&degree%5B%5D=2&degree%5B%5D=3&degree%5B%5D=7&degree%5B%5D=5&degree%5B%5D=6&lang%5B%5D=2&lang%5B%5D=4&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dur%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list"
    split_url = url.rsplit("&display", 1)
    parsed_url = f"" + \
        split_url[0] + "{" + str(target_list)+"}" + \
        "&display" + split_url[1]
    print(parsed_url)
# %%
q = [10, 20, 30]
url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=1&degree%5B%5D=2&degree%5B%5D=3&degree%5B%5D=7&degree%5B%5D=5&degree%5B%5D=6&lang%5B%5D=2&lang%5B%5D=4&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dur%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list"
test_soup = delicious_soup(q, url=url)

# %%
csv_data = {}
item_no = 0
for test in test_soup.findAll("div", {"class": "c-result-list__content c-masonry js-result-list-content"}):
    for soup in test.findAll("div", {"class": "c-ad-carousel c-masonry__item c-masonry__item--result-list mb-5"}):
        course_type = soup.find(
            "p", {"class": "c-ad-carousel__course m-0"}).text.strip()
        course_name = soup.find(
            "span", {"class": "js-course-title d-none d-sm-block"}).text
        course_link = soup.find(
            "a", {"class": "list-inline-item mr-0 js-course-detail-link"})['href']
        slug_ = "https://www2.daad.de"
        item_no += 1
        course_link = slug_+course_link
        csv_data[item_no] = [course_type, course_name, course_link]
    print(csv_data)
    # test_wirte_csv.writerow(
    #     [course_type, course_name, course_link])
# test_wirte_csv_df = pd.DataFrame.from_dict(csv_data, orient='index',
#                                            columns=["course_type", "course_name", "course_link"])
# %%
# Masters degree

masters_page_range = list(range(0, 21, 10))
masters_souped_page = []
#target_list = ""
masters_url = f"https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=2&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lang%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dur%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list"

for pages in masters_page_range:
    split_url = masters_url.rsplit("&display", 1)
    parsed_url = f"{split_url[0]}{str(pages)}&display{split_url[1]}"
    print(f"Scrapping: page {int(pages/10 + 1)}")
    print(parsed_url)
    watery_soup = make_tasty_soup(parsed_url)
    masters_souped_page.append(watery_soup)
# masters_soup = delicious_soup(
#     masters_page_range, masters_url)

#print(datetime.now() - startTime)

# %%
csv_data = {}
item_no = 0
for masters_soup in masters_souped_page:
    for d in masters_soup.findAll("div", {"class": "c-result-list__content c-masonry js-result-list-content"}):
        for soup in d.findAll("div", {"class": "c-ad-carousel c-masonry__item c-masonry__item--result-list mb-5"}):
            course_type = soup.find(
                "p", {"class": "c-ad-carousel__course m-0"}).text
            course_name = soup.find(
                "span", {"class": "js-course-title d-none d-sm-block"}).text
            # course_link = soup.find(
            #     "a", {"class": "list-inline-item mr-0 js-course-detail-link"})['href']
            # uni_name = soup.find("span", {
            #                         "class": "c-ad-carousel__subtitle c-ad-carousel__subtitle--small js-course-academy"}).text
            # uni_city = soup.find("span", {
            #                         "class": "c-ad-carousel__subtitle c-ad-carousel__subtitle--location c-ad-carousel__subtitle--small"}).text
            # ul = soup.find("ul", {
            #                 "class": "c-ad-carousel__data-list c-ad-carousel__data-list--not-colored p-0"})
            # # contains Short for shortcourse, Phd for Phd and Mas for Masters
            # relevant_span = ("span", {
            #                     "class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"})
            # course_type_sereies = str(course_type)
            # tution_fee = ul.findAll("li")[0].find(relevant_span).text
            # lang_of_instr = ul.findAll("li")[1].find(relevant_span).text
            # dura_of_study = ul.findAll("li")[3].find(relevant_span).text
            slug_ = "https://www2.daad.de"
            item_no += 1
            #course_link = slug_+course_link
            #course_name, course_link
            csv_data[item_no] = [course_type, course_name]
        print(csv_data)
        # print(course_type)
        # if re.findall(r'Short', course_type_sereies):
        #     tution_fee = ul.findAll("li")[0].find(relevant_span).text
        # elif re.findall(r'Ph', course_type_sereies):
        #     tution_fee = ""
        # elif re.findall(r'Mas|Bach', course_type_sereies):
        #     tution_fee = ul.findAll("li")[0].find(relevant_span).text

        # # Language of Instruction
        # if re.findall(r'Short', course_type_sereies):
        #     lang_of_instr = ul.findAll("li")[1].find(relevant_span).text
        # elif re.findall(r'Ph', course_type_sereies):
        #     lang_of_instr = ul.findAll("li")[0].find(relevant_span).text
        # elif re.findall(r'Mas|Bach', course_type_sereies):
        #     lang_of_instr = ul.findAll("li")[1].find(relevant_span).text

        # # Duration of study
        # if re.findall(r'Short', course_type_sereies):
        #     dura_of_study = ul.findAll("li")[3].find(relevant_span).text
        # elif re.findall(r'Ph', course_type_sereies):
        #     dura_of_study = ul.findAll("li")[2].find(relevant_span).text
        # elif (re.findall(r'Mas|Bach', course_type_sereies)):
        #     print(max([len(ul.findAll("li"))]))
# %%
# Bachelors
bachelor_page_range = list(range(0, 211, 10))
bachelor_url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&degree%5B%5D=1&langDeAvailable=&langEnAvailable=&lang%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&dur%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list&fee=&bgn%5B%5D="
bachelor_soup = delicious_soup(bachelor_page_range, bachelor_url)
# %%
phd_page_range = list(range(0, 241, 10))
# %%
for s in bachelor_soup.findAll("div", {"class": "c-result-list__content c-masonry js-result-list-content"}):
    for soup in s.findAll("div", {"class": "c-ad-carousel c-masonry__item c-masonry__item--result-list mb-5"}):
        course_type = soup.find(
            "p", {"class": "c-ad-carousel__course m-0"}).text
        print(len(course_type))
# %%
start = time.time()
e = list(range(0, 1250, 10))
souped_page = []

for each_e in e:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(
        f"https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=1&degree%5B%5D=2&degree%5B%5D=3&degree%5B%5D=7&degree%5B%5D=5&degree%5B%5D=6&lang%5B%5D=2&lang%5B%5D=4&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dur%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset={each_e}&display=list")
    time.sleep(15)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    souped_page.append(soup)

end = time.time()
print(end - start)
# %%
for b in range(1, 3):
    b += 1
    print(b)
# %%
first_attempt = []
for soupy in souped_page:
    for s in soupy.findAll("div", {"class": "c-result-list__content c-masonry js-result-list-content"}):
        for soup in s.findAll("div", {"class": "c-ad-carousel c-masonry__item c-masonry__item--result-list mb-5"}):
            course_type = soup.find(
                "p", {"class": "c-ad-carousel__course m-0"}).text
            course_name = soup.find(
                "span", {"class": "js-course-title d-none d-sm-block"}).text
            course_link = soup.find(
                "a", {"class": "list-inline-item mr-0 js-course-detail-link"})['href']
            uni_name = soup.find("span", {
                                 "class": "c-ad-carousel__subtitle c-ad-carousel__subtitle--small js-course-academy"}).text
            uni_city = soup.find("span", {
                                 "class": "c-ad-carousel__subtitle c-ad-carousel__subtitle--location c-ad-carousel__subtitle--small"}).text
            ul = soup.find("ul", {
                           "class": "c-ad-carousel__data-list c-ad-carousel__data-list--not-colored p-0"})
            # contains Short for shortcourse, Phd for Phd and Mas for Masters
            relevant_span = ("span", {
                             "class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"})
            course_type_sereies = str(course_type)
            if re.findall(r'Short', course_type_sereies):
                tution_fee = ul.findAll("li")[0].find(relevant_span).text
            elif re.findall(r'Ph', course_type_sereies):
                tution_fee = ""
            elif re.findall(r'Mas|Bach', course_type_sereies):
                tution_fee = ul.findAll("li")[0].find(relevant_span).text

            # Language of Instruction
            if re.findall(r'Short', course_type_sereies):
                lang_of_instr = ul.findAll("li")[1].find(relevant_span).text
            elif re.findall(r'Ph', course_type_sereies):
                lang_of_instr = ul.findAll("li")[0].find(relevant_span).text
            elif re.findall(r'Mas|Bach', course_type_sereies):
                lang_of_instr = ul.findAll("li")[1].find(relevant_span).text

            # Duration of study
            if re.findall(r'Short', course_type_sereies):
                dura_of_study = ul.findAll("li")[3].find(relevant_span).text
            elif re.findall(r'Ph', course_type_sereies):
                dura_of_study = ul.findAll("li")[2].find(relevant_span).text
            elif (re.findall(r'Mas|Bach', course_type_sereies)):
                print(max([len(ul.findAll("li"))]))
            # elif (re.findall(r'Mas|Bach', course_type_sereies)) and len(ul.findAll("li")) > 3:
            #     dura_of_study = ul.findAll("li")[3].find(relevant_span).text

            # #Semester Start
            # if re.findall(r'Short', course_type_sereies):
            #     sem_satrt = ""
            # elif re.findall(r'Ph', course_type_sereies):
            #     sem_satrt = ul.findAll("li")[1].find(relevant_span).text
            # elif (re.findall(r'Bach', course_type_sereies)) and len(ul.findAll("li")) >= 3:
            #     sem_satrt = ul.findAll("li")[3].find(relevant_span).text

            # try:
            #     if re.findall(r'Short', course_type_sereies):
            #         sem_satrt = ""
            #     elif re.findall(r'Ph', course_type_sereies):
            #         sem_satrt = ul.findAll("li")[1].find(relevant_span).text
            #     elif re.findall(r'Mas', course_type_sereies):
            #         sem_satrt = ul.findAll("li")[2].find(relevant_span).text
            # except IndexError as identifier:
            #     if re.findall(r'Short', course_type_sereies):
            #         sem_satrt = ""
            #     elif re.findall(r'Ph', course_type_sereies):
            #         sem_satrt = ul.findAll("li")[1].find(relevant_span).text
            #     elif re.findall(r'Mas', course_type_sereies):
            #         sem_satrt = ul.findAll("li")[2].find(relevant_span).text

            csv_array = [course_type, uni_name,
                         course_name, course_link, uni_city, tution_fee, lang_of_instr, dura_of_study]
            first_attempt.append(csv_array)

            # lang_of_instr = ul.findAll("li")[1].find("span", {"class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"}).text
            # application_semester = ul.findAll("li")[2].find("span", {"class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"}).text
            # study_duration = ul.findAll("li")[3].find("span", {"class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"}).text
            # print(tution_fee)
            # for li in soup.find("ul", {"class": "c-ad-carousel__data-list c-ad-carousel__data-list--not-colored p-0"}).findAll("li"):
            #     tution_fee = li[0].find("span", {"class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"}).text
            # .find("span", {"class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"}).text
            # lang_of_instr = soup.li[2].find("span", {"class": "c-ad-carousel__data-item c-ad-carousel__data-item--single-line"}).text
            # result-list > div > div:nth-child(1) > div > div.c-result-list__content.c-masonry.js-result-list-content > div:nth-child(10) > div > div > div > div > div > div.col-12.c-ad-carousel__content.c-ad-carousel__content > div > ul > li:nth-child(1) > span
            # result-list > div > div:nth-child(1) > div > div.c-result-list__content.c-masonry.js-result-list-content > div:nth-child(10) > div > div > div > div > div > div.col-12.c-ad-carousel__content.c-ad-carousel__content > div > ul > li:nth-child(2) > span
# %%
# first_attempt.to_csv("first_attempt.csv")
with open('first_attempt_1.csv', 'wb') as file:
    writer = csv.writer(file)
    for row in first_attempt:
        writer.writerow(row)
# %%


def __init__(self):
    self.first_attempt = csv.writer(open('first_attempt_1.csv', 'w'))
    self.first_attempt.writerow([first_attempt])


# %%
pd.Series(["sr", "fs"]).str.contains(pat='s[a-z]', regex=True)
# %%
for soup in souped_page:
    s = soup.findAll(
        "div", {"class": "c-result-list__content c-masonry js-result-list-content"})
    print(s)
# %%
# Masters
