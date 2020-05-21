from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
driver = webdriver.Chrome()
url = "https://photographers.canvera.com/bangalore/wedding-photography"

driver.get(url)
driver.refresh()
delay = 15
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'allDatas')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

total = []
writer = pd.ExcelWriter('{}.xlsx'.format('Canvera'), engine='xlsxwriter')  # pylint: disable=abstract-class-instantiated
def closeBox(driver):
    try:
        driver.find_element_by_class_name('close-modal').click()
        print('Yes')
        return True
    except:
        return False

for i in range(10):
    datas = None
    try:
        datas = driver.find_elements_by_class_name('profile-item')
    except:
        print("Can't find all datas element")
        break
    for data in datas:
        name = location = price = profileTags = rating = numRating = None
        try:
            name = data.find_element_by_class_name('profile-title').text
        except:
            name = None
        try:
            location = data.find_element_by_class_name('profile-location').text
        except:
            location = None
        try:
            price = data.find_element_by_class_name('price-info').text
            if(price == 'Contact for price details'):
                price = None
        except:
            price = None
        try:
            profileTags = data.find_element_by_class_name('profile-tags').text
        except:
            profileTags = None
        try:
            review = data.find_element_by_class_name('no-reviews')
            rating = None
            numRating = None
        except:
            try:
                rating = 0
                rating += len(data.find_elements_by_class_name('icon-star'))
                rating += len(data.find_elements_by_class_name('icon-star-half-alt'))
                numRating = data.find_element_by_class_name('rating-info').text
            except:
                rating = None
                numRating = None
        if(name is not None):
            total.append((name, location, price, profileTags, rating, numRating))
    try:
        closeBox(driver)
        driver.find_element_by_id('next').click()
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'model-content')))
            closeBox(driver)
            print ("Page is ready!")
        except TimeoutException:
            print ("Tricked", i)
    except:
        print('Could not go to next page')
        break

print(total)
df = pd.DataFrame(total, columns = ['NAME','LOCATION','PRICE','TAGS','RATING','NUM-RATINGS'])
df = df.set_index('NAME')
df = df.loc[~df.index.duplicated(keep = 'first')]
df.to_excel(writer,sheet_name = 'Wedding Photography')
writer.save()