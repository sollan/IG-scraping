from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
from selenium.webdriver.common.keys import Keys

usernames = [
    'hwainio', 'annette.paints', 'leaem_illustration',
    'poopikat', 'rosannatasker.illustration',
    'hillkurtz', 'laviniadraws', 'mazarat', 'lyana.nikitina', 'dianapedott', 
    'vanessagillings', 'adelinaillustration', 'janicesung', 'thegalshir', 'syertse'
]

links=[]

login_data = {
    'username': 'beautifulsoup6361',
    'password': 'BS4Instagram'
}

for username in usernames:

    browser = webdriver.Chrome('/home/annette/usr/chromedriver')
    browser.get('https://www.instagram.com/'+username+'/?hl=en')

    for i in range(5):
        Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        try:
            elem = browser.find_element_by_name('username')
            elem.clear()
            elem.send_keys(login_data['username'])
            time.sleep(1)
            elem = browser.find_element_by_name('password')
            elem.send_keys(login_data['password'])
            time.sleep(1)
            elem.send_keys(Keys.ENTER)
            time.sleep(7)
        except:
            pass

    browser_height = browser.execute_script("return document.body.scrollHeight")

    notAtPageBottom = True
    while notAtPageBottom:
        Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if browser.execute_script("return document.body.scrollHeight") == browser_height:
            notAtPageBottom = False
        else:
            browser_height = browser.execute_script("return document.body.scrollHeight")
            elements = browser.find_elements_by_class_name('eLAPa')
            for i in range(len(elements)):
                link = elements[i].find_element_by_xpath('..').get_attribute('href')
                if link not in links:
                    links.append(link)
                    print(link)

    elements = browser.find_elements_by_class_name('eLAPa')
    for i in range(len(elements)):
        link = elements[i].find_element_by_xpath('..').get_attribute('href')
        if link not in links:
            links.append(link)
            print(link)


df = pd.DataFrame(data={'link': links})
df.to_csv('./links.csv', sep=',',index=False)