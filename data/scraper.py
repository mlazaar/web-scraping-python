import pandas as pd
import requests

from bs4 import BeautifulSoup as bs

class Scraper:

    def __init__(self):
        super().__init__()

    def scrapUrl(self, url):
        html = requests.get(url)  
        soup = bs(html.text,'html.parser')  
        return soup
