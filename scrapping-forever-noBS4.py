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



# Here we scrap the links of every single book 
category_links = open('start_links.txt','r',encoding='utf-8')
out_file = open('book_links.json','w+' , encoding='utf-8')
product_links = list()

next_button_Xpath = '//*[@id="my-store-741189"]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div[2]/a[2]/span[1]'

for link in category_links :
    print('Working on :' ,link.split('/')[-1][:-4])
    try:
                browser.get(link)
                

    except Exception as err:
                print(str(err))
                break
    else:
                print('Successfully Accessed:',link)
                print('Please be patient it may take several minutes .....')


    while True :
        time.sleep(20)
        try :
            
            element = browser.find_element_by_xpath(next_button_Xpath)
        except NoSuchElementException:
            

            #div_tags = soup.find_all('div', attrs={"class":"grid-product__wrap-inner"})
            div_tags = browser.find_elements_by_xpath('//div[@class="grid-product__wrap-inner"]')
            for tag in div_tags :
                #anchor = tag.findChild('a',attrs={'class':'grid-product__title'})
                anchor = tag.find_element_by_tag_name("a")
                product_links.append(anchor.get_attribute("href"))
                    
            break 
        
        element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, next_button_Xpath)))
        try :
            if element.is_displayed() :
                

                div_tags = browser.find_elements_by_xpath('//div[@class="grid-product__wrap-inner"]')
                
                for tag in div_tags :
                    anchor = tag.find_element_by_tag_name("a")
                    product_links.append( anchor.get_attribute("href"))
                        
                browser.execute_script("arguments[0].click();", element)
                time.sleep(10)
            else :
                time.sleep(10)

                div_tags = browser.find_elements_by_xpath('//div[@class="grid-product__wrap-inner"]')
                
                for tag in div_tags :
                    anchor = tag.find_element_by_tag_name("a")
                    product_links.append( anchor.get_attribute("href"))
                    
                break 

        except exceptions.StaleElementReferenceException:  
            pass
    
    print('writing links to file .... ')
    out_file.seek(0)
    out_file.truncate()
    json.dump({'links':list(set(product_links))},out_file)
    print('File successfully updated.....')



out_file.close()
print('All data saved successfully !!')

# Here we scrap book details

links = json.loads(open('book_links.json', 'r' , encoding='utf-8').read())["links"]
out_file = open('book_Data.json','w+' , encoding='utf-8')
book_data = dict()

for link in links :
    
    try:
                browser.get(link)
                time.sleep(15)
                # html_text = browser.page_source

    except Exception as err:
                print(str(err))
                break
    else:
                print('Successfully Accessed:',link)
    time.sleep(15)


    # book_name = soup.find('h1', attrs={'class':'product-details__product-title'})
    try :    
        book_name = browser.find_element_by_xpath('//h1[@class="product-details__product-title"]')
        book_data[book_name.text] = dict()
    except NoSuchElementException :
        pass
    #book_price = soup.find('span',attrs={'class':'details-product-price__value notranslate'})
    try :
        book_price = browser.find_element_by_xpath('//span[@class="details-product-price__value notranslate"]')
        book_data[book_name.text]['Price'] = book_price.text
    except NoSuchElementException :
        pass
    # book_description = soup.find('div',attrs={'id':'productDescription'})
    try:
        book_description = browser.find_element_by_xpath('//div[@id="productDescription"]')
        description_cleaned   = book_description.find_element_by_tag_name("div").text.replace('Available for Rent or Used, Second Hand at Best Prices on  www.pustakkosh.com','')
        book_data[book_name.text]['Decription'] = description_cleaned  
    except NoSuchElementException :
        pass
    
    #img_div = soup.find('div',attrs={'class':'details-gallery__image-wrapper-inner'})
    try :
        img_div = browser.find_element_by_xpath('//div[@class="details-gallery__image-wrapper-inner"]')
        book_data[book_name.text]['Image_URL'] = img_div.find_element_by_tag_name('img').get_attribute("src")
    except NoSuchElementException :
        pass
    print('writing data to file .... ')
    out_file.seek(0)
    out_file.truncate()
    json.dump(book_data,out_file)
    print('File successfully updated.....')    

out_file.seek(0)
out_file.truncate()
json.dump(book_data,out_file)
out_file.close()
print('All Data saved successfully ....!!')
browser.close()
