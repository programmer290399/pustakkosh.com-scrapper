import json 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions  
import re


# We take control of browser here 
browser = None

try:
    browser = webdriver.Chrome()
except Exception as error:
    print(error)


# Here we scrap product links from thier respective categories 

category_links = open('categories.txt','r',encoding='utf-8')
out_file = open('infibeam_book_links.json','w+' , encoding='utf-8')
product_links = list()

for link in category_links :
    print('Working on :' ,link.split('/')[-1])
    try:
                browser.get(link)
                

    except Exception as err:
                print(str(err))
                break
    else:
                print('Successfully Accessed:',link)
                print('Please be patient it may take several minutes .....')

