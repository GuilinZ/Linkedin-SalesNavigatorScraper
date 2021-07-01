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

def scrap_from_url(args, driver,url=None, load_page=True):
    if url == None:
        url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=12&geoIncluded=103644278&industryIncluded=4&logHistory=true&page=1&rsLogId=967882860&searchSessionId=2KtadMyDTh6HsrXXvjHlIQ%3D%3D&seniorityIncluded=6%2C7%2C8'

    if load_page:
        driver.get(url)
        time.sleep(3)
#################################### INSERT URL ####################################

    links = []
    number_page = 1
    number_candidate = 0
    while number_page < 2:
        time.sleep(3)
        height = 0
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while height < driver.execute_script("return document.body.scrollHeight"):
            driver.execute_script("window.scrollTo(0, {});".format(height))
            height += 20
        names = driver.find_elements_by_tag_name("a")
        for name in names:
            link = name.get_attribute('href')
            if 'https://www.linkedin.com/sales/people/' in link:
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
        # if count > 1:
        #     break
        driver.get(link)
        time.sleep(1)
        person_profile = {}
        ## Implement BeautifulSoup for html parser## TODO
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')

        # get full name
        full_name = soup.title.text.split('|')[0]

        # get position and company name
        pos_and_company = soup.find(class_='profile-topcard__current-positions flex mt3').text.split()
        index_at = pos_and_company.index('at')
        position = ' '.join(pos_and_company[:index_at])
        company = pos_and_company[index_at + 1]

        # get connection size
        try:
            connection_size = soup.find(class_='profile-topcard__connections-data type-total inline t-14 t-black--light mr5').text.strip()
        except:
            connection_size = ''


        # company url
        try:
            url_root = 'https://www.linkedin.com'
            company_url = soup.find(class_='profile-topcard__current-positions flex mt3').a.attrs['href']
            company_url = url_root + company_url
        except:
            company_url = ''

        # linkedin profile url
        try:
            trip = driver.find_element_by_css_selector(
                "div[class='artdeco-dropdown artdeco-dropdown--placement-bottom artdeco-dropdown--justification-right ember-view']")
            trip.click()
            cop_button = driver.find_element_by_css_selector("div[data-control-name='copy_linkedin']")
            time.sleep(1)
            cop_button.click()
            time.sleep(1)
            linkedin_url = Tk().clipboard_get()
        except:
            linkedin_url = ''

        # profile description
        try:
            see_more_button = driver.find_element_by_css_selector(
                "button[class='button--unstyled link-without-visited-state inline-block font-size-inherit profile-topcard__summary-expand-link']")
            see_more_button.click()
            src = driver.page_source
            soup = BeautifulSoup(src, 'html.parser')
            profile_summary = soup.find(class_='profile-topcard__summary-modal-content').text.strip()
        except:
            profile_summary = ''


        # get hiring needs
        hiring_needs = 'NO'
        split_profile = profile_summary.split()
        for word in split_profile:
            if word in hiring_keys:
                hiring_needs = 'YES'
        top_card = soup.find(class_='profile-topcard-content-container mr2').text.strip().split()
        for word in top_card:
            if word in hiring_keys:
                hiring_needs = 'YES'
        ##---------------------------------------##
        number_candidate += 1
        print("{} /".format(number_candidate) + " {}".format(len(links)))
        person_profile['NAME'] = full_name
        person_profile['POSITION'] = position
        person_profile['CONNECTION SIZE'] = connection_size
        person_profile['COMPANY'] = company
        person_profile['HIRING NEEDS'] = hiring_needs
        person_profile['LINKEDIN WEBPAGE'] = linkedin_url
        person_profile['COMPANY WEBPAGE'] = company_url
        person_profile['SALE NAVIGATOR URL'] = link
        person_profile['DESCRIPTION'] = profile_summary
        extracted_infos.append(person_profile)
        time.sleep(3)

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

    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com')
    driver.maximize_window()

    username = driver.find_element_by_id('session_key')
    username.send_keys('joycewxyyy@gmail.com')  # Insert your e-mail

    password = driver.find_element_by_id('session_password')
    password.send_keys('Internship2021@')  # Insert your password here

    log_in_button = driver.find_element_by_class_name("sign-in-form__submit-button")
    log_in_button.click()
    time.sleep(1)
    try:
        confirm_button = driver.find_element_by_id('remember-me-prompt__form-secondary')
        confirm_button.click()
    except:
        pass
    time.sleep(1)

    print(args)
    if args.mode == 'url':
        scrap_from_url(args, driver, args.url)
    elif args.mode == 'keywords':
        scrap_from_keywords(args, driver, keywords=args.search_words)
    elif args.mode == 'hugeworks':
        scrap_from_company_list(args, driver, fpath='./company.txt')
    else:
        print('MODE wrongly specified!!!')







