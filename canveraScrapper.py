from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
driver = webdriver.Chrome()

def closeBox(driver):
    try:
        driver.find_element_by_class_name('close-modal').click()
        print('Yes')
        return True
    except:
        return False
pagesToExtract = 30
types = ['wedding']
writer = pd.ExcelWriter('{}.xlsx'.format('Canvera'), engine='xlsxwriter')  # pylint: disable=abstract-class-instantiated
total = []
for category in types:
    url = "https://photographers.canvera.com/bangalore/" + category + "-photography"
    driver.get(url)
    driver.refresh()
    delay = 0
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'allDatas')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
    i = 0
    while i < pagesToExtract:
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
                    rating += len(data.find_elements_by_class_name('icon-star-half-alt')) * 0.5
                    numRating = data.find_element_by_class_name('rating-info').text
                except:
                    rating = None
                    numRating = None
            if(name is not None):
                total.append((name, location, price, profileTags, rating, numRating))
        try:
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'model-content')))
                closeBox(driver)
                print ("Page is ready!")
            except TimeoutException:
                print ("Completed Page No.", i+1, "for Category ", category)
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'next')))
                closeBox(driver)
                print ("Page is ready for Next")
            except TimeoutException:
                print ("Completed Page No.", i+1, "for Category ", category)
            closeBox(driver)
            action = webdriver.common.action_chains.ActionChains(driver)
            action.click()
            driver.find_element_by_id('next').click()
            i += 1
        except:
            print('Could not go to next page')

df = pd.DataFrame(total, columns = ['NAME','LOCATION','PRICE','TAGS','RATING','NUM-RATINGS'])
df = df.set_index('NAME')
df = df.loc[~df.index.duplicated(keep = 'first')]
df.to_excel(writer)
    # print(total)
writer.save()