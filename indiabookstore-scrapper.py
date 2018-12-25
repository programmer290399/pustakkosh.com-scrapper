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

# category_links = open('kick_start_categories.txt','r',encoding='utf-8')
# out_file = open('indiabookstore_book_links.json','w+' , encoding='utf-8')
# product_links = list()

# next_btn_Xpath = '//li[@class="arrow"][contains(text(),"Next »")]'
# book_links_Xpath = '//div[@class="col-md-3 col-xs-6 text-center "]//child::a[@class="bookPageLink"]'

# for link in category_links :
#     print('Working on :' ,link.split('/')[-1])
#     try:
#                 browser.get(link)
                

#     except Exception as err:
#                 print(err))
#                 break
#     else:
#                 print('Successfully Accessed:',link)
#                 print('Please be patient it may take several minutes .....')
#     while True :
#         try :
#             element = browser.find_element_by_xpath(next_btn_Xpath)
#         except NoSuchElementException:
#             time.sleep(1)
            
#             anchor_tags = browser.find_elements_by_xpath(book_links_Xpath) 
            
                
#             for tag in anchor_tags :
#                 product_links.append(tag.get_attribute("href"))
                    
#             break 
#         time.sleep(1)
#         element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
#                         .until(expected_conditions.presence_of_element_located((By.XPATH, next_btn_Xpath)))
#         try :
#             if element.is_displayed() :
#                 time.sleep(1)
#                 anchor_tags = browser.find_elements_by_xpath(book_links_Xpath) 
                
                
#                 for tag in anchor_tags :
#                     product_links.append(tag.get_attribute("href"))
                
#                 browser.execute_script("arguments[0].click();", element)
#                 time.sleep(1)
#             else :
#                 time.sleep(1)
#                 anchor_tags = browser.find_elements_by_xpath(book_links_Xpath) 
            
                
#                 for tag in anchor_tags :
#                     product_links.append(tag.get_attribute("href"))
                
#                 break 

#         except exceptions.StaleElementReferenceException:  
#             pass
    
#     print('writing links to file .... ')
#     out_file.seek(0)
#     out_file.truncate()
#     json.dump({'links':list(set(product_links))},out_file)
#     print('File successfully updated.....')
#     #! Remove before commit 
#     break


# out_file.close()
# print('All data saved successfully !!')


# Here we scrape book data 

print('Getting book data now .....')
links = json.loads(open('indiabookstore_book_links.json','r' , encoding='ANSI').read())['links']
out_file =  open('indiabookstore_data.json','w+' , encoding='utf-8')
book_data = dict()
for link in links :

    try:
                browser.get(link)
                

    except Exception as err:
                print(str(err))
                break
    else:
                print('Successfully Accessed:',link)
                print('Please be patient it may take several minutes .....')

    try : 
        book_name = re.sub('\s+', '' , browser.find_element_by_xpath('//h1[@class="bookMainTitle"]').text )
        book_data[book_name] = dict()
        book_data[book_name]['ISBN-13'] = link.split('/')[-1]
    except :
        pass 
    try :
        Author = browser.find_element_by_xpath('//div[@itemprop="author"]').text.split(':')[1]
        book_data[book_name]['Author'] = Author
    except :
        pass
    try:
        Publisher = browser.find_element_by_xpath('//div[@itemprop="author"]//following-sibling::div').text.split(':')[1]
        book_data[book_name]['Publisher'] = Publisher
    except :
        pass
    try :
        rating = re.findall("\d+\.\d+", browser.find_element_by_xpath('//div[@itemprop="ratingValue"]').text)[0]
        book_data[book_name]['Rating'] = rating
    except :
        pass 
    try :
        isbn_10 = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"ISBN-10")]//following-sibling::td[@itemprop="isbn"]').text
        book_data[book_name]['ISBN-10'] = isbn_10
    except :
        pass 
    try :
        number_of_pages = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Number of pages")]//following-sibling::td[@itemprop="numberOfPages"]').text.split()[0]
        book_data[book_name]['Number of pages'] = number_of_pages
    except:
        pass 
    try :
        language = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Language")]//following-sibling::td[@itemprop="inLanguage"]').text
        book_data[book_name]['Language'] = language
    except :
        pass 
    try :
        edition = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Edition")]//following-sibling::td').text
        book_data[book_name]['Edition'] = edition
    except :
        pass
    try :
        dimensions = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Dimension")]//following-sibling::td').text
        book_data[book_name]['Dimensions'] = re.sub('\s+', '' , dimensions )
    except :
        pass 
    try :
        description = browser.find_element_by_xpath('//span[@itemprop="description"]').text
        book_data[book_name]['Book Description'] = description
    except :
        pass 
    try :
        image_URL = browser.find_element_by_xpath('//img[@class="bookMainImage"]').get_attribute('src')
        book_data[book_name]['Image_URL'] = image_URL 
    except :
        pass 
    try :
        prices = list()
        price_tags = browser.find_elements_by_xpath('//div[@class="card"]//child::a')[:-1]
        for price_tag in price_tags :
            text_data = price_tag.get_attribute('textContent')
            if '@' in text_data : prices.append(text_data)
        book_data[book_name]['Prices'] = prices
    except :
        pass
    print('Writing to file')
    out_file.seek(0)
    out_file.truncate()
    json.dump(book_data,out_file)

out_file.seek(0)
out_file.truncate()
json.dump(book_data,out_file)
print('All data scrapped Successfullly !!!')
out_file.close()
browser.close()
        
