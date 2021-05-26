


__author__ = "Chaluka Salgado"
__copyright__ = "Copyright 2021 @ Kamikaze"
__email__ = "chaluka.salgado@gmail.com"
__date__ = "25-Apr-2021"
__updated__ = "25-Apr-2021"
__version__ = "1.0"

import requests
from bs4 import BeautifulSoup
import string

class ColesProductSearch:

    URL = "https://shop.coles.com.au/a/chadstone/everything/browse"

    def __init__(self):
        self.url = None


    def __get_html_parser(self, url: str):
        """
            Return the html parser object for a given URL
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def extract_data(self, url:str):
        soup = self.__get_html_parser(url)
        print(soup)
        jobs = soup.find_all('li', class_='cat-nav-item')

        print(jobs)


if __name__=="__main__":
    coles = ColesProductSearch()
    coles.extract_data(ColesProductSearch.URL)

