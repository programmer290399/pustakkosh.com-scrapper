from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
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

browser = None

try:
    browser = webdriver.Chrome()
except Exception as error:
    print(error)


category_links = open('start_links.txt','r',encoding='utf-8')
out_file = open('book_links.json','w+' , encoding='utf-8')
product_links = list()

next_button_Xpath = '//*[@id="my-store-741189"]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div[2]/a[2]/span[1]'


for link in category_links :
    print('Working on :' ,link.split('/')[-1][:-4])
    try:
                browser.get(link)
                html_text = browser.page_source

    except Exception as err:
                print(str(err))
                break
    else:
                print('Successfully Accessed:',link)
                print('Please be patient it may take several minutes .....')

    soup = None
    if html_text is not None:
            soup = BeautifulSoup(html_text, 'lxml')
    
    
    while True :
        time.sleep(10)
        try :
            
            element = browser.find_element_by_xpath(next_button_Xpath)
        except NoSuchElementException:
            
            html_text = browser.page_source
            soup = BeautifulSoup(html_text, 'lxml')
            div_tags = soup.find_all('div', attrs={"class":"grid-product__wrap-inner"})
                
            for tag in div_tags :
                anchor = tag.findChild('a',attrs={'class':'grid-product__title'})
                product_links.append(link + anchor.get('href', None))
                    
            break 
        
        element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, next_button_Xpath)))
        try :
            if element.is_displayed() :
                
                html_text = browser.page_source
                soup = BeautifulSoup(html_text, 'lxml')
                div_tags = soup.find_all('div', attrs={"class":"grid-product__wrap-inner"})
                
                for tag in div_tags :
                    anchor = tag.findChild('a',attrs={'class':'grid-product__title'})
                    product_links.append(link + anchor.get('href', None))
                    
                browser.execute_script("arguments[0].click();", element)
                time.sleep(10)
            else :
                time.sleep(10)
                html_text = browser.page_source
                soup = BeautifulSoup(html_text, 'lxml')
                div_tags = soup.find_all('div', attrs={"class":"grid-product__wrap-inner"})
                
                for tag in div_tags :
                    anchor = tag.findChild('a',attrs={'class':'grid-product__title'})
                    product_links.append(link + anchor.get('href', None))
                    
                break 

        except exceptions.StaleElementReferenceException:  
            pass
    print(len(list(set(product_links))),'Links recived from',link.split('/')[-1][:-4])
    print('writing links to file .... ')
    json.dump({'links':list(set(product_links))},out_file)
    print('File successfully updated.....')


out_file.close()
print('All data saved successfully !!')
