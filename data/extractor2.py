
from data.scraper import Scraper
from utils.utils import Utils
import pandas as pd
import json

# Constantes
# brands = ['Apple','Google','Asus','BlackBerry']
brands = ['Apple','Google']

columns = ['Nom','Marque','Taille Ecran(en pouces)','Dimensions','Poids(en g)','OS','Processeur','Prix(prix en euros)', 'Mémoire', 'RAM', 'Appareil photo']
scraper = Scraper()
util = Utils()

class Extractor2:

    
    def __init__(self, basic_url):
        self.basic_url = basic_url
        super().__init__()


    def getRAM(self, html):
        return html.find('section', class_ ='kc-container white container-sheet-hardware').findAll('dl', class_ ='k-dl')[2].findAll('dd')[0].text.split(' ')[0]

    def getStorage(self,html):
       return html.find('section', class_ ='kc-container white container-sheet-hardware').findAll('dl', class_ ='k-dl')[4].findAll('dd')[0].text.split(' ')[0]

    def getPixelPhotos(self,html):
       return html.find('section', class_ ='kc-container dark black-isometric container-sheet-camera').findAll('dl', class_ ='k-dl')[0].findAll('dd')[1].text.split(' ')[0]

    def getSmartphoneName(self,html):
        return html.find('div', class_ ='title-group').find("h1").getText()[len('Prix et caractéristiques du '):]

    def getSmartphoneBrand(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-intro').findAll('dl', class_ ='k-dl')[0].findAll('dd')[0].text.strip()

    def getSmartphoneScreenSize(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-design').findAll('dl', class_ ='k-dl')[1].findAll('dd')[0].text.replace('"','')

    def getSmartphoneDimensions(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-design').findAll('dl', class_ ='k-dl')[0].findAll('dd')[0].text.replace('mm','').replace('•','x').replace('.',',')

    def getSmartphoneWeight(self,html):
        weight = html.find('section', class_ ='kc-container white container-sheet-design').findAll('dl', class_ ='k-dl')[0].findAll('dd')[1].text
        return weight.replace('g', '')

    def getSmartphoneaOs(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-software').find('dl', class_ ='k-dl').find('div').text

    def getSmartphoneProcessor(self,html):
        return html.find('section', class_ ='kc-container white container-sheet-hardware').findAll('dl', class_ ='k-dl')[0].findAll('dd')[0].text

    def getSmartphonePrices(self,html):
        data = html.select("[type='application/ld+json']")[0]
        oJson = json.loads(data.text)
        return oJson['offers']['lowPrice']

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
        
        try :
            phone_infos['Taille Ecran(en pouces)'] = self.getSmartphoneScreenSize(html)
        except :
            phone_infos['Taille Ecran(en pouces)'] = None

        try :
            phone_infos['Dimensions'] = self.getSmartphoneDimensions(html)
        except :
            phone_infos['Dimensions'] = None
        
        try :
            phone_infos['Poids(en g)'] = self.getSmartphoneWeight(html)
        except :
            phone_infos['Poids(en g)'] = None

        try :     
            phone_infos['OS'] = self.getSmartphoneaOs(html)
        except :
            phone_infos['OS'] = None

        try :
            phone_infos['Processeur'] = self.getSmartphoneProcessor(html)
        except :
            phone_infos['Processeur'] = None

        try : 
            phone_infos['Prix(prix en euros)'] = self.getSmartphonePrices(html)
        except :
            phone_infos['Prix(prix en euros)'] = None
        try : 
            phone_infos['RAM'] = self.getRAM(html)
        except :
            phone_infos['RAM'] = None
        try : 
            phone_infos['Mémoire'] = self.getStorage(html)
        except:
            phone_infos['Mémoire'] = None  
        try : 
            phone_infos['Appareil photo'] = self.getPixelPhotos(html)
        except :
            phone_infos['Appareil photo'] = None
        return phone_infos

    def build(self, html, dataF):
        brandLinks = self.getAllBrandsUrls(html)
        data = []

        for element in brandLinks:
            new_html_soup = scraper.scrapUrl(element)
            phones_link = self.getUrlsSmarphonesModelsOfABrand(new_html_soup)
            # phones_infos_link = self.getUrlsSmartphoneTechnicalReview(phones_link)

            for var in phones_link:
                data.append(self.getDataFromTechnicalReviewPage(scraper.scrapUrl(var)))
                dataframe = pd.DataFrame(data, columns=columns)
                tab = pd.concat([dataF,dataframe])
        return tab