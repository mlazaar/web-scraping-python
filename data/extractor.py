import pandas as pd

from data.scraper import Scraper
from utils.utils import Utils
from decorator import Decorator1

# Constantes
# brands = ['Apple iPhone','Google','Asus','BlackBerry']
brands = ['Apple iPhone','Google']

columns = ['Nom','Marque','Taille Ecran(en pouces)','Dimensions','Poids(en g)','OS','Processeur','Prix(prix en euros)', 'Mémoire', 'RAM', 'Appareil photo']

scraper = Scraper()
util = Utils()
decorator = Decorator1()

class Extractor:
    
    def __init__(self, basic_url):
        self.basic_url = basic_url
        super().__init__()

    @decorator.cleanDataRam
    def getRAM(self, html):
        ram = html.findAll('table', class_ ='data-table')[4].findAll('td')[1].text
        try : 
            return ram
        except :
            return None

    @decorator.cleanDataStorage
    def getStorage(self,html):
        storage = html.findAll('table', class_ ='data-table')[4].findAll('td')[1].text
        try : 
            return storage
        except:
            return None  

    @decorator.cleanDataPixelPhotos
    def getPixelPhotos(self,html):
        px = html.findAll('table', class_ ='data-table')[3].findAll('td')[0].text
        try :
            return px
        except :
            return None

    def getSmartphoneName(self,html):
        return html.find('div', class_ ='header-phone clearfix').find("h1").text[len('Fiche technique '):]

    @decorator.cleanDataScreenSize
    def getSmartphoneScreenSize(self,html):
        screenSize = html.findAll('table', class_ ='data-table')[1].findAll('td')[0].text
        try :
            return screenSize
        except :
            return None

    @decorator.cleanDataDimensions
    def getSmartphoneDimensions(self,html):
        dimension= html.find('table', class_ ='data-table').findAll('td')[1].text
        try :
            return dimension
        except :
            return None

    @decorator.cleanDataWeight
    def getSmartphoneWeight(self,html):
        weight =html.find('table', class_ ='data-table').findAll('td')[2].text
        try:
            return weight
        except:
            return None

    def getSmartphoneaOs(self,html):
        os = html.find('table', class_ ='data-table').findAll('td')[5].text
        try:
            return os
        except:
            return None

    def getSmartphoneProcessor(self,html):
        processor = html.find('table', class_ ='data-table').findAll('td')[6].text
        try:
            return processor
        except:
            return None

    @decorator.cleanDataPrice
    def getSmartphonePrices(self,html):
        price = (html.find('table', class_ ='data-table').findAll('td')[8].text)
        try:
            return price
        except:
            return None

    def getAllBrandsUrls(self,html):
        brand_urls = []
        for element in html.find('div', class_ ='push-all-brands').find_all('li'):
            if((element.find('a')['title']) in brands):
                brand_urls.append(self.basic_url + element.find('a').get('href'))
        return brand_urls

    def getUrlsSmarphonesModelsOfABrand(self,html):
        phones_url = []
        for element in html.find('div', class_ ='push-phones-new list-phones list-phones-grid').findAll('article'):
            phones_url.append(self.basic_url + element.find('a').get('href'))
        return phones_url

    def getUrlsSmartphoneTechnicalReview(self, urls):
        phones_info_urls = []
        for element in urls:
            phones_info_urls.append(self.basic_url + scraper.scrapUrl(element).find('div', class_ ='resume').find('a').get('href'))
        return phones_info_urls

    def getDataFromTechnicalReviewPage(self,html):
        phone_infos = {}
        phone_infos['Nom'] = self.getSmartphoneName(html)
        phone_infos['Marque'] = phone_infos['Nom'].split(" ")[0].strip()
        phone_infos['Taille Ecran(en pouces)'] = self.getSmartphoneScreenSize(html)
        phone_infos['Dimensions'] = self.getSmartphoneDimensions(html)
        phone_infos['Poids(en g)'] = self.getSmartphoneWeight(html)
        phone_infos['OS'] = self.getSmartphoneaOs(html)
        phone_infos['Processeur'] = self.getSmartphoneProcessor(html)
        phone_infos['Prix(prix en euros)'] = util.convertStringToInt(self.getSmartphonePrices(html))
        phone_infos['RAM'] = self.getRAM(html)
        phone_infos['Mémoire'] = self.getStorage(html)
        phone_infos['Appareil photo'] = self.getPixelPhotos(html)

        return phone_infos

    def build(self, html, dataF):
    
        brandLinks = self.getAllBrandsUrls(html)
        data = []

        for element in brandLinks:
            new_html_soup = scraper.scrapUrl(element)
            phones_link = self.getUrlsSmarphonesModelsOfABrand(new_html_soup)
            phones_infos_link = self.getUrlsSmartphoneTechnicalReview(phones_link)

            for var in phones_infos_link:
                data.append(self.getDataFromTechnicalReviewPage(scraper.scrapUrl(var)))
                dataframe = pd.DataFrame(data, columns=columns)
                tab = pd.concat([dataF,dataframe])
        return tab