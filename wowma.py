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
def scrap_from_url(args, driver,url=None, load_page=True):

    links = []
    number_page = 1
    number_candidate = 0

    names = driver.find_elements_by_tag_name("a")
    for name in names:
        link = name.get_attribute('href')
        if '/bep/m/prom90?id=656' in link:
            if link not in links:
                links.append(link)

    number_page += 1


    extracted_infos = []
    count=0
    for link in links:
        count += 1
        print(count)
        # if count > 10:
        #     break
        driver.get(link)
        # time.sleep(1)
        url = driver.current_url
        if('error') in url:
            continue
        url_splt = url.split('/')
        user_id = url_splt[url_splt.index('user') + 1]
        template1 = 'https://plus.wowma.jp/bep/m/kmem?user='
        template2 = '&amp;spe_id=item_shopinfo'
        info_page = template1 + user_id + template2

        driver.get(info_page)
        if('error') in driver.current_url:
            continue
        # time.sleep(1)
        info1 = driver.find_element_by_id('shopInfo1').text.split()
        info2 = driver.find_element_by_id('shopInfo2').text.split()
        person_profile = {}
        shop_name = ' '.join(info1[info1.index('お店の名前') + 1:\
                          info1.index('お店の会員番号')])
        company_name = info1[info1.index('販売事業者名') + 1]
        manager_name = info1[info1.index('通信販売業務責任者') + 1]
        address = info2[info2.index('住所') + 1]
        phone_num = info2[info2.index('電話番号') + 1]
        try:
            fax_num = info2[info2.index('FAX番号') + 1]
        except:
            fax_num = ''
        email = info2[info2.index('メールアドレス') + 1]

        person_profile['SHOP NAME'] = shop_name
        person_profile['COMPANY NAME'] = company_name
        person_profile['MANAGER'] = manager_name
        person_profile['ADDRESS'] = address
        person_profile['PHONE'] = phone_num
        person_profile['FAX'] = fax_num
        person_profile['EMAIL'] = email
        extracted_infos.append(person_profile)
        # time.sleep(3)

    with open('results.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=extracted_infos[0].keys())
        fc.writeheader()
        fc.writerows(extracted_infos)
    # df = pd.DataFrame(np.array(tab))
    # df.to_excel(r'{}/Linkedin_Scrap.xlsx'.format(path), index=False, header=True)
    print('DONE')
    return extracted_infos

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
    driver.get('https://wowma.jp/search/shopSearch.html')
    # driver.execute_script("driver.stop();")
    # driver.maximize_window()
    scrap_from_url(args, driver, args.url, load_page=False)







