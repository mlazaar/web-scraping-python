import pandas as pd
import json

from data.scraper import Scraper
from utils.utils import Utils
from decorator import Decorator2

# Constantes
# brands = ['Apple','Google','Asus','BlackBerry']
brands = ['Apple','Google']

columns = ['Nom','Marque','Taille Ecran(en pouces)','Dimensions','Poids(en g)','OS','Processeur','Prix(prix en euros)', 'Mémoire', 'RAM', 'Appareil photo']
scraper = Scraper()
util = Utils()
decorator = Decorator2()

class Extractor2:

    
    def __init__(self, basic_url):
        self.basic_url = basic_url
        super().__init__()

    @decorator.cleanDataRam
    def getRAM(self, html):
        ram = html.find('section', class_ ='kc-container white container-sheet-hardware').findAll('dl', class_ ='k-dl')[2].findAll('dd')[0].text
        try:
            return ram
        except:
            return None

    @decorator.cleanDataStorage
    def getStorage(self,html):
        storage = html.find('section', class_ ='kc-container white container-sheet-hardware').findAll('dl', class_ ='k-dl')[4].findAll('dd')[0].text
        try:
            return storage
        except:
            return None

    @decorator.cleanDataPixelPhotos
    def getPixelPhotos(self,html):
        px = html.find('section', class_ ='kc-container dark black-isometric container-sheet-camera').findAll('dl', class_ ='k-dl')[0].findAll('dd')[1].text
        try:
            return px
        except:
            return None

    def getSmartphoneName(self,html):
        return html.find('div', class_ ='title-group').find("h1").getText()[len('Prix et caractéristiques du '):]

    @decorator.cleanDataBrand
    def getSmartphoneBrand(self,html):
        brand = html.find('section', class_ ='kc-container white container-sheet-intro').findAll('dl', class_ ='k-dl')[0].findAll('dd')[0].text
        try:
            return brand
        except:
            return None

    @decorator.cleanDataScreenSize
    def getSmartphoneScreenSize(self,html):
        screen = html.find('section', class_ ='kc-container white container-sheet-design').findAll('dl', class_ ='k-dl')[1].findAll('dd')[0].text
        try: 
            return screen
        except:
            return None

    @decorator.cleanDataDimensions
    def getSmartphoneDimensions(self,html):
        dimensions = html.find('section', class_ ='kc-container white container-sheet-design').findAll('dl', class_ ='k-dl')[0].findAll('dd')[0].text
        try:
            return dimensions
        except:
            return None

    @decorator.cleanDataWeight
    def getSmartphoneWeight(self,html):
        weight = html.find('section', class_ ='kc-container white container-sheet-design').findAll('dl', class_ ='k-dl')[0].findAll('dd')[1].text
        try:   
            return weight
        except:
            return None

    def getSmartphoneaOs(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-software').find('dl', class_ ='k-dl').find('div').text

    def getSmartphoneProcessor(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-hardware').findAll('dl', class_ ='k-dl')[0].findAll('dd')[0].text

    def getSmartphonePrices(self,html):
        data = html.select("[type='application/ld+json']")[0]
        oJson = json.loads(data.text)
        try:
            return oJson['offers']['lowPrice']
        except:
            return None

    def getAllBrandsUrls(self,html):
        brand_urls = []
        for element in html.find('div', class_ ='kc-container lightgray').findAll('li', class_ ='item'):
            if((element.find('h3').getText()) in brands):
                brand_urls.append(element.find('a').get('href'))
        return brand_urls

    def getUrlsSmarphonesModelsOfABrand(self,html):
        phones_url = []
        for element in html.find('ul', class_ ='simple-device-list').findAll('li'):
            phones_url.append(element.find('a').get('href'))
        return phones_url

    def getDataFromTechnicalReviewPage(self,html):
        phone_infos = {}
        phone_infos['Nom'] = self.getSmartphoneName(html)
        phone_infos['Marque'] = self.getSmartphoneBrand(html)
        phone_infos['Taille Ecran(en pouces)'] = self.getSmartphoneScreenSize(html)
        phone_infos['Dimensions'] = self.getSmartphoneDimensions(html)
        phone_infos['Poids(en g)'] = self.getSmartphoneWeight(html)
        phone_infos['OS'] = self.getSmartphoneaOs(html)
        phone_infos['Processeur'] = self.getSmartphoneProcessor(html)
        phone_infos['Prix(prix en euros)'] = self.getSmartphonePrices(html)
        phone_infos['RAM'] = self.getRAM(html)
        phone_infos['Mémoire'] = self.getStorage(html)
        phone_infos['Appareil photo'] = self.getPixelPhotos(html)

        print(phone_infos)

        return phone_infos

    def build(self, html, dataF):
        brandLinks = self.getAllBrandsUrls(html)
        data = []

        for element in brandLinks:
            new_html_soup = scraper.scrapUrl(element)
            phones_link = self.getUrlsSmarphonesModelsOfABrand(new_html_soup)

            for var in phones_link:
                data.append(self.getDataFromTechnicalReviewPage(scraper.scrapUrl(var)))
                dataframe = pd.DataFrame(data, columns=columns)
                tab = pd.concat([dataF,dataframe])
        return tab