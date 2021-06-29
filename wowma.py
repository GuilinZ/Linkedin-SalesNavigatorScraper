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
    # if url == None:
    #     url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=12&geoIncluded=103644278&industryIncluded=4&logHistory=true&page=1&rsLogId=967882860&searchSessionId=2KtadMyDTh6HsrXXvjHlIQ%3D%3D&seniorityIncluded=6%2C7%2C8'
    #
    # if load_page:
    #     driver.get(url)
    #     time.sleep(3)
#################################### INSERT URL ####################################

    links = []
    number_page = 1
    number_candidate = 0
    while number_page < 2:
        # time.sleep(3)
        # height = 0
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # while height < driver.execute_script("return document.body.scrollHeight"):
        #     driver.execute_script("window.scrollTo(0, {});".format(height))
        #     height += 20
        names = driver.find_elements_by_tag_name("a")
        for name in names:
            link = name.get_attribute('href')
            if '/bep/m/prom90?id=656' in link:
                if link not in links:
                    links.append(link)

        number_page += 1
        # next_button = driver.find_element_by_class_name("search-results__pagination-next-button")
        # next_button.click()
        # print(links)
        # print(len(links))

    extracted_infos = []
    hiring_keys = ['hiring','hiring!','Hiring','Hiring!','HIRING','open','Open','position']
    count=0
    for link in links:
        count += 1
        print(count)
        if count > 10:
            break
        driver.get(link)
        # time.sleep(1)
        url = driver.current_url
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
def scrap_from_keywords(args, driver,keywords=None):
    # filter_page_url = 'https://www.linkedin.com/sales/search/people?page=1&rsLogId=969614316&searchSessionId=1qpyQattToCh2lFvET1Cwg%3D%3D'
    filter_page_url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=12&geoIncluded=103644278&logHistory=true&page=1&rsLogId=994102108&searchSessionId=1qpyQattToCh2lFvET1Cwg%3D%3D&seniorityIncluded=6%2C8%2C7'
    # print(filter_page_url)
    driver.get(filter_page_url)
    time.sleep(3)

    kwd_input = driver.find_element_by_id('ember44-input')
    kwd_input.send_keys(keywords)
    kwd_input.send_keys(Keys.ENTER)
    time.sleep(1)
    profiles = scrap_from_url(args, driver, url=driver.current_url, load_page=False)
    return profiles
def scrap_from_company_list(args, driver, fpath=''):
    company_list = read_company_list(fpath)
    rets = []
    for company in company_list:
        profiles = scrap_from_keywords(args, driver,keywords=company)
        rets.extend(profiles)
    with open('all_company.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=rets[0].keys())
        fc.writeheader()
        fc.writerows(rets)
    return rets
def read_company_list(fpath):
    with open(fpath) as f:
        lines = f.readlines()
    f.close()
    lines = [line.strip() for line in lines]
    return lines


####################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_words', default=None)
    parser.add_argument('--url', default=None)
    parser.add_argument('--mode', default='url')
    args = parser.parse_args()

    # driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.101").install())
    driver = webdriver.Chrome()
    driver.get('https://wowma.jp/search/shopSearch.html')
    # driver.maximize_window()
    scrap_from_url(args, driver, args.url, load_page=False)

    # username = driver.find_element_by_id('session_key')
    # username.send_keys('joycewxyyy@gmail.com')  # Insert your e-mail
    #
    # password = driver.find_element_by_id('session_password')
    # password.send_keys('Internship2021@')  # Insert your password here
    #
    # log_in_button = driver.find_element_by_class_name("sign-in-form__submit-button")
    # log_in_button.click()
    # time.sleep(1)
    # try:
    #     confirm_button = driver.find_element_by_id('remember-me-prompt__form-secondary')
    #     confirm_button.click()
    # except:
    #     pass
    # time.sleep(1)
    #
    # print(args)
    # if args.mode == 'url':
    #     scrap_from_url(args, driver, args.url)
    # elif args.mode == 'keywords':
    #     scrap_from_keywords(args, driver, keywords=args.search_words)
    # elif args.mode == 'hugeworks':
    #     scrap_from_company_list(args, driver, fpath='./company.txt')
    # else:
    #     print('MODE wrongly specified!!!')







