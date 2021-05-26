# %matplotlib inline
import string

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def auto_click():
    url = "https://www.woolworths.com.au//"
    browser = webdriver.Chrome()
    browser.get(url)
    item = browser.find_element_by_id('categoryHeaderSmallFormat-browseButton')
    item.click()
    links = browser.find_elements_by_class_name('categoriesNavigation-linkText')
    for link in links:
        link.click()
        browser.back()

if __name__ == "__main__":
    auto_click()

    # str1 = "helo/hi,me:it'sch.aluka sala^for,say"
    # s = re.split(PUNCTUATIONS,str1)
    # print(s)
