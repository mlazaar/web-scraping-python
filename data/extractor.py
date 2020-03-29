
from data.scraper import Scraper
from utils.utils import Utils
import pandas as pd


# Constantes
# brands = ['Apple iPhone','Google','Asus','BlackBerry']
brands = ['Apple iPhone','Google']

columns = ['Nom','Marque','Taille Ecran(en pouces)','Dimensions','Poids(en g)','OS','Processeur','Prix(prix en euros)', 'Mémoire', 'RAM', 'Appareil photo']

scraper = Scraper()
util = Utils()

class Extractor:

    
    def __init__(self, basic_url):
        self.basic_url = basic_url
        super().__init__()

    def getRAM(self, html):
       return html.findAll('table', class_ ='data-table')[4].findAll('td')[1].text.split('Go, ')[1].replace(' Go RAM', '')
        
    def getStorage(self,html):
       return html.findAll('table', class_ ='data-table')[4].findAll('td')[1].text.split('Go, ')[0]

    def getPixelPhotos(self,html):
       return html.findAll('table', class_ ='data-table')[3].findAll('td')[0].text.split(' ')[0]

    def getSmartphoneName(self,html):
        return html.find('div', class_ ='header-phone clearfix').find("h1").text[len('Fiche technique '):]

    def getSmartphoneScreenSize(self,html):
        screenSize = html.findAll('table', class_ ='data-table')[1].findAll('td')[0].text
        screenSize = screenSize.replace('pouces', '').replace(',', '.')
        return screenSize

    def getSmartphoneDimensions(self,html):
        dimension= html.find('table', class_ ='data-table').findAll('td')[1].text
        dimension=dimension.replace("mm","")
        return dimension

    def getSmartphoneAutonomy(self,html):
        autonomy = html.find('table', class_ ='data-table').findAll('td')[3].text
        autonomy = autonomy[:autonomy.index("h")]
        autonomy = autonomy.strip()
        return autonomy

    def getSmartphoneWeight(self,html):
        weight =html.find('table', class_ ='data-table').findAll('td')[2].text
        weight = weight.replace('grammes', '')
        return weight

    def getSmartphoneaOs(self,html):
        return html.find('table', class_ ='data-table').findAll('td')[5].text

    def getSmartphoneProcessor(self,html):
        processor = html.find('table', class_ ='data-table').findAll('td')[6].text
        return processor

    def getSmartphonePrices(self,html):
        return (html.find('table', class_ ='data-table').findAll('td')[8].text).split('€')[0]

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
            phone_infos['Prix(prix en euros)'] = util.convertStringToInt(self.getSmartphonePrices(html))
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
            phones_infos_link = self.getUrlsSmartphoneTechnicalReview(phones_link)

            for var in phones_infos_link:
                data.append(self.getDataFromTechnicalReviewPage(scraper.scrapUrl(var)))
                dataframe = pd.DataFrame(data, columns=columns)
                tab = pd.concat([dataF,dataframe])
        return tab