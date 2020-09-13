#Import Necessary Libraries
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import base64
import requests
import shutil

#Function to extract image from it's base64 byte code
def extract_images(dirname, links,dish):
    length = len(links)
    for index, link in enumerate(links):
        suffix = index
        link = link.encode()
        print('extracting {0} of {1} images'.format(index + 1, length))
        fh = open('{dirname}/{dish}_img_{suffix}.png'.format(dirname=dirname,dish =dish,  suffix=suffix), 'wb')
        fh.write(base64.decodebytes(link))
        fh.close()

#Function to download the image from specified URL
def download_images(dirname, links,name):
    length = len(links)
    for index, link in enumerate(links):
        print('Downloading {0} of {1} images'.format(index + 1, length))
        url = link
        response = requests.get(url, stream=True)
        save_image_to_file(response, dirname, index,name)
        del response

#Saving downloaded images to mentioned Destination
def save_image_to_file(image, dirname, suffix,name):
    with open('{dirname}/{name}_image_{suffix}.jpg'.format(dirname=dirname,name = name, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

#Taking a keyword to be searched in google search for getting Images
key_to_search = input("Enter keyword to be serached for image data:- ")

#Create instance of chrome webdriver
driver = webdriver.Chrome(r"C:\Users\GAURI TOSHNIWAL\Documents\cosylab\scraping_code\chromedriver.exe")  #replace your chromedriver path
driver.get("https://www.google.com/search")#navigate to page given by URL
time.sleep(3)#add delay to program so that page loads

#Input the keyword into search box present
search = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')#Xpath to google search bar
search.send_keys(key_to_search)
time.sleep(2)

#Click on search button to get the results
button = driver.find_element_by_class_name('gNO89b')
button.click()
time.sleep(2)

#Locating Images and clicking on images to reach appropriate page
buttons = []
buttons = driver.find_elements_by_class_name('q.qs')
for button2 in buttons:
    check = button2.get_attribute("data-sc")
    print(check)
    if check == 'I':
        final_button = button2
        break
final_button.click()
time.sleep(2)

#select only those images which are labeled for reuse
tool_button = driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div/div')
tool_button.click()
time.sleep(1)

usage_button = driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/c-wiz[1]/div/div/div[1]/div/div[5]/div/div[1]')
usage_button.click()
time.sleep(1)

reuse_button = driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/c-wiz[1]/div/div/div[3]/div/a[1]/div/span')
reuse_button.click()
time.sleep(1)

#intializing lists
lst1 = list()
lst2 = list()

#reach to bottom of page(it is observed 400 images are covered till we reach show more results and 5 scrolls are required)
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

#Click on show more button to load more images
try:
    button3 = driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input')
    button3.click()
    time.sleep(2)

    #Again scrolling to the bottom
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
except:
    print("Looks like you have reached the end")

#Extracing all the sources of images by using class name
img_link = driver.find_elements_by_class_name('rg_i.Q4LuWd')
print("Total image sources fteched are:",len(img_link))

#Downloading/Decoding Images
cnt = 0
for img in img_link:
    link = img.get_attribute("src")#For every image get the src attribute
    if link != None: #If it returns somthing
        if link[0] == 'd': #Check if src is in form of bas64 bytes
            enimg = link.split(',')
            lst1.append(enimg[1]) #add the bytes code of image to list 1
        elif link[0] == 'h': #check if the source is a URL
            lst2.append(link) #add the link to list 2
    else:
        cnt = cnt+1 #if extracting source results in None keep a count

time.sleep(2)
driver.close()

print("Total sources which resulted into None",cnt)

#Calling extract_images function
extract_images(r'C:\Users\GAURI TOSHNIWAL\Documents\cosylab\scraping_code\google_images',lst1,key_to_search)#replace destination where you want to store images

#Calling download images function
download_images(r'C:\Users\GAURI TOSHNIWAL\Documents\cosylab\scraping_code\google_images',lst2,key_to_search)#replace destination where you want to store images
