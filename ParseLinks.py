from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

date = []
caption = []
author = []
n_comments = []
n_likes = []
hashtags = []
curr_links = []

browser = webdriver.Chrome('/home/annette/usr/chromedriver')
links = pd.read_csv('./links.csv')

def parseHashtag(string):
    clean_string = string.replace('&#', ' ')
    if '#' in clean_string:
        start = clean_string.find('#')
        length = clean_string[start:].find(' ')
        end = start + length
        hashtag = clean_string[start:end]
        try:
            if len(hashtag) <= 20:
                return hashtag, clean_string[end:]
            else:
                return hashtag.split('","created_at')[0]
        except:
            return
    else:
        return


for i in range(1851,len(links)):

    date_temp = []
    caption_temp = []
    author_temp = []
    n_comments_temp = []
    n_likes_temp = []
    hashtags_temp = []

    browser.get(links['link'][i])
    source = browser.page_source
    data = bs(source, 'html.parser')
    script = data.findAll('script')

    hashtags_temp = []

    for which_script in script:

        if 'uploadDate' in which_script.text:
            try:
                date_temp = which_script.text.split('uploadDate":"')[1].split('T')[0]
            except:
                pass
            
            try:
                caption_temp = which_script.text.replace('\n', ' ').split('caption":"')[1].split('","')[0]
            except:
                pass

            try:
                author_temp = which_script.text.split('alternateName":"')[1].split('","')[0]
            except:
                pass

            try:
                n_comments_temp = which_script.text.split('commentCount":"')[1].split('","')[0]
            except:
                pass

            try:
                n_likes_temp = which_script.text.split('userInteractionCount":"')[1].split('"}')[0]
            except:
                pass

    description = data.find_all('meta')
    
    for tag in description:
        # if tag.get('property', None) == 'instapp:hashtags':
        #     hashtags_temp.append(tag.get('content'))
        if tag.get('property', None) == 'og:description':
            n_likes_temp = tag.get('content').split(' Likes')[0]
            n_comments_temp = tag.get('content').split('Likes, ')[1].split(' Comments')[0]


    # if hashtags_temp  == []:

    for which_script in script:
        if which_script.text.startswith('window._sharedData'):
            next_string = which_script.text
            while next_string:
                try:
                    hashtag, next_string = parseHashtag(next_string) 
                    hashtags_temp.append(hashtag)
                except:
                    next_string = False

    if date_temp == []:

        try:

            date_temp = browser.find_element_by_class_name('c-Yi7').find_element_by_xpath('.//*').get_attribute('title')
            caption_temp = browser.find_element_by_class_name('C4VMK').find_element_by_css_selector('span').text.replace('\n', ' ')
            author_temp = browser.find_element_by_class_name('_6lAjh ').find_element_by_xpath('.//*').text

        except:
            pass

    curr_links.append(links['link'][i])
    date.append(date_temp)
    caption.append(caption_temp)
    author.append(author_temp)
    n_comments.append(n_comments_temp)
    n_likes.append(n_likes_temp)
    hashtags.append(hashtags_temp)

    print(links['link'][i], date_temp, caption_temp, author_temp, n_comments_temp, n_likes_temp, hashtags_temp)

    if i % 50 == 0:

        df = pd.DataFrame(data={'link': curr_links, 'date': date, 'author': author, 'n_comments': n_comments, 'n_likes': n_likes, 'hashtags': hashtags, 'caption': caption})
        df.to_csv('./results{0}.csv'.format(i//50), sep=',',index=False)
        del df

df = pd.DataFrame(data={'link': curr_links, 'date': date, 'author': author, 'n_comments': n_comments, 'n_likes': n_likes, 'hashtags': hashtags, 'caption': caption})
df.to_csv('./results.csv', sep=',',index=False)