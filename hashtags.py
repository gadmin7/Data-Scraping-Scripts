from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

print("---------hastags data extractor---------")
key_to_search = input("Enter topic to genrate hashtag data:- ")
driver = webdriver.Chrome(r".\chromedriver.exe")  #replace your chromedriver path
driver.get("https://metahashtags.com/") 
time.sleep(5) 
search = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/input')

search.send_keys(key_to_search)


button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[2]/button')
button.click()



time.sleep(6)

i=1 # iterator variable to iterate over all the list items

all_parse = False #flag to check if all the data is loaded or not

while True:
    try:
        hastag_text                 =     driver.find_element_by_xpath(f'//*[@id="scrollable-{key_to_search}"]/li[{i}]/div/div[1]/div/div/div[1]/button').text  # select and store hastag
        no_of_post                  =     driver.find_element_by_xpath(f'//*[@id="scrollable-{key_to_search}"]/li[{i}]/div/div[1]/div/div/div[2]/span[1]/span[1]/b').text #select and store no of post for hastag
        no_of_post_publish_per_hour =     driver.find_element_by_xpath(f'//*[@id="scrollable-{key_to_search}"]/li[{i}]/div/div[1]/div/div/div[2]/span[1]/span[2]/b').text #selct and store no. of post per hour for hastag
        avg_likes                   =     driver.find_element_by_xpath(f'//*[@id="scrollable-{key_to_search}"]/li[{i}]/div/div[1]/div/div/div[2]/span[2]/span[1]/b').text #select and store avg. likes on a post
        min_likes                   =     driver.find_element_by_xpath(f'//*[@id="scrollable-{key_to_search}"]/li[{i}]/div/div[1]/div/div/div[2]/span[2]/span[2]/b').text #select and store minimum likes on post 
        avg_comment                 =     driver.find_element_by_xpath(f'//*[@id="scrollable-{key_to_search}"]/li[{i}]/div/div[1]/div/div/div[2]/span[3]/span/b').text #select and store no of comments
        i+=1 # increment list element counter
        print(hastag_text," ",no_of_post," ",no_of_post_publish_per_hour," ",avg_likes," ",min_likes," ",avg_comment)
   
   
    except NoSuchElementException:
        '''if exception check for "data-finished" attribute, if it is "yes" then set all_parse flag as true and if it is already true
        break loop else scroll down'''
        if all_parse:
            break
        
        driver.execute_script(f'var elmnt = document.getElementById("scrollable-{key_to_search}");elmnt.scrollIntoView(false);')
        time.sleep(2)

        final_load_disp = driver.find_element_by_xpath(f'//*[@id="loading-{key_to_search}"]')

        if str(final_load_disp.get_attribute("data-finished")) =='yes':
            all_parse = True
    
    time.sleep(1)

driver.close()
