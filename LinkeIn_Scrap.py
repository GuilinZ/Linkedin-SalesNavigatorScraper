from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import os
import openpyxl
from tkinter import Tk
import argparse


def scrap_from_url(url=None):
    url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=12&geoIncluded=103644278&industryIncluded=4&logHistory=true&page=1&rsLogId=967882860&searchSessionId=2KtadMyDTh6HsrXXvjHlIQ%3D%3D&seniorityIncluded=6%2C7%2C8'
    driver.get(url)
#################################### INSERT URL ####################################
    time.sleep(3)
    links = []
    tab = []
    number_page = 1
    number_candidate = 1
    path = "/Users/romainmeunier/Desktop"
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
        next_button = driver.find_element_by_class_name("search-results__pagination-next-button")
        next_button.click()
        print(links)
        print(len(links))

    extracted_infos = []
    for link in links:
        driver.get(link)
        time.sleep(3)
        person_profile = {}
        ## Implement BeautifulSoup for html parser## TODO
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        # name
        full_name = soup.title.text.split('|')[0]

        # position and company name
        pos_and_company = soup.find(class_='profile-topcard__current-positions flex mt3').text.split()
        index_at = pos_and_company.index('at')
        position = ' '.join(pos_and_company[:index_at])
        company = pos_and_company[index_at + 1]

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
        ##---------------------------------------##
        number_candidate += 1
        print("{} /".format(number_candidate) + " {}".format(len(links)))
        person_profile['NAME'] = full_name
        person_profile['POSITION'] = position
        person_profile['COMPANY'] = company
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
    done = True
def scrap_from_keywords(keywords=None):
    filter_page_url = 'https://www.linkedin.com/sales/search/people?page=1&rsLogId=969614316&searchSessionId=1qpyQattToCh2lFvET1Cwg%3D%3D'
    driver.get(filter_page_url)
    pass
#filter page

####################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', default=None)

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










