from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import os
import openpyxl
from tkinter import Tk
import argparse
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import re

def scrap_from_url(args, driver,url=None, load_page=True):
    page = 0
    max_page = 55
    extracted_infos = []
    count = 0
    item_num = 1
    user_ids = set()
    while page < max_page:
        links = []
        page += 1
        print('page: ', page)
        names = driver.find_elements_by_tag_name("a")
        for name in names:
            link = name.get_attribute('href')
            if 'https://shopping.yahoo.co.jp/review/item/list?store_id=' in link:
                links.append(link)
        # print('num of link: ', len(links))
        for link in links:
            count += 1
            print(count)
            url=link
            url_splt = re.split('[?.,=_/&]',url)
            user_id = url_splt[url_splt.index('id') + 1]

            if user_id not in user_ids:
                 user_ids.add(user_id)
                 print('Totally', len(user_ids), 'stores have been scanned')
            else:
                continue
            template1 = 'https://store.shopping.yahoo.co.jp/'
            template2 = '/info.html'
            info_page = template1 + user_id + template2

            driver.get(info_page)
            if ('error' in driver.current_url) or ('notfound' in driver.current_url):
                continue
            info = driver.find_element_by_tag_name('body').text.split()
            person_profile = {}
            shop_name = info[info.index('会社名（商号）') + 1]
            address = info[info.index('住所') + 1]
            manager_name = info[info.index('代表者') + 1]
            phone=''
            fax=''
            email=''
            for pos,element in enumerate(info):
                if 'お問い合わせ' == element:
                    phone = info[pos + 1]
                    email = info[pos + 2]
                    break
                if 'お問い合わせ電話番号' == element:
                    phone = info[pos + 1]
                if 'お問い合わせファックス番号' == element:
                    fax = info[pos + 1]
                if 'お問い合わせメールアドレス' == element:
                    email = info[pos + 1]
                    break
            person_profile['SHOP NAME'] = shop_name
            person_profile['MANAGER'] = manager_name
            person_profile['ADDRESS'] = address
            person_profile['PHONE'] = phone
            person_profile['FAX'] = fax
            person_profile['EMAIL'] = email
            extracted_infos.append(person_profile)
        if page % 2 == 0:
            with open('results_yahoo14.csv', 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file, fieldnames=extracted_infos[0].keys())
                fc.writeheader()
                fc.writerows(extracted_infos)
        item_num += 30
        next_page = 'https://shopping.yahoo.co.jp/category/13457/2494/37524/list?X=8&view=list&sc_i=shp_pc_catelist_nrwcgt&b='
        next_page = next_page + str(item_num)
        driver.get(next_page)
    with open('results_yahoo14.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=extracted_infos[0].keys())
        fc.writeheader()
        fc.writerows(extracted_infos)
    print('Done')
####################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_words', default=None)
    parser.add_argument('--url', default=None)
    parser.add_argument('--mode', default='url')
    args = parser.parse_args()

    # driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.101").install())
    driver = webdriver.Chrome()
    # driver.set_page_load_timeout(1)
    driver.get('https://shopping.yahoo.co.jp/category/13457/2494/37524/list?X=8&view=list&sc_i=shp_pc_catelist_nrwcgt&b=1')
    # driver.execute_script("driver.stop();")
    # driver.maximize_window()
    scrap_from_url(args, driver, args.url, load_page=False)
