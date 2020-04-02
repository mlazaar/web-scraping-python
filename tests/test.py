import unittest

from utils.utils import Utils
from data.scraper import Scraper
from data.extractor import Extractor
from data.extractor2 import Extractor2

class Tests(unittest.TestCase):

    # Test la fonction qui converti un String en Int 
    def test_convertStringToInt (self):
    # GIVEN
        n = "2"
        util = Utils()
    # WHEN
        r = util.convertStringToInt(n)
    # THEN
        self.assertEqual (2, r, "doit etre 2")

    # Test la fonction qui scrap une page en web, on lui donne un url en paramètre et elle nous renvoi un code html
    def test_ScrapUrl (self):
    # GIVEN
        url = 'https://en.wikipedia.org/wiki/Python'
        scrap = Scraper()
    # WHEN
        r = scrap.scrapUrl(url).find('h1').getText()
    # THEN
        self.assertEqual ('Python', r, "doit etre Python")

    # Test de la fonction qui va extraire l'url de la page où sont affiché tous les téléphones d'une marque sur le premier site (lesmobiles.com)
    def test_getAllBrandsUrlsExtractor1(self):
    # GIVEN
        url = 'https://www.lesmobiles.com/telephones/'
        scrap = Scraper()
        extrac = Extractor("https://www.lesmobiles.com")
        result = ['https://www.lesmobiles.com/telephones/mobiles_apple.html','https://www.lesmobiles.com/telephones/mobiles_google.html']
    # WHEN
        html = scrap.scrapUrl(url)
        r = extrac.getAllBrandsUrls(html)
    # THEN
        self.assertEqual (result, r)

    # Test de la fonction qui va extraire l'url de la page où sont affiché tous les téléphones d'une marque sur le deuxième site (kimovil.com)
    def test_getAllBrandsUrlsExtractor2(self):
    # GIVEN
        url = 'https://www.kimovil.com/fr/toutes-les-marques-de-mobiles'
        scrap = Scraper()
        extrac = Extractor2("https://www.kimovil.com/fr/")
        result = ['https://www.kimovil.com/fr/prix-telephones-apple','https://www.kimovil.com/fr/prix-telephones-google']
    # WHEN
        html = scrap.scrapUrl(url)
        r = extrac.getAllBrandsUrls(html)
    # THEN
        self.assertEqual (result, r)

    # Test de la fonction qui va extraire l'url de chaque téléphone d'une marque sur le premier site (lesmobiles.com)
    def test_getUrlsSmarphonesModelsOfABrandExtractor1(self):
    # GIVEN
        url = 'https://www.lesmobiles.com/telephones/mobiles_yota.html'
        scrap = Scraper()
        extrac = Extractor("https://www.lesmobiles.com")
        result = ['https://www.lesmobiles.com/telephones/yota-yotaphone-2.html']
    # WHEN
        html = scrap.scrapUrl(url)
        r = extrac.getUrlsSmarphonesModelsOfABrand(html)
    # THEN
        self.assertEqual (result, r)

    # Test de la fonction qui va extraire l'url de chaque téléphone d'une marque sur le premier site (lesmobiles.com)
    def test_getUrlsSmarphonesModelsOfABrandExtractor2(self):
    # GIVEN
        url = 'https://www.kimovil.com/fr/prix-telephones-aermoo'
        scrap = Scraper()
        extrac = Extractor2("https://www.kimovil.com/fr/")
        result = ['https://www.kimovil.com/fr/ou-acheter-aermoo-m1']
    # WHEN
        html = scrap.scrapUrl(url)
        r = extrac.getUrlsSmarphonesModelsOfABrand(html)
    # THEN
        self.assertEqual (result, r)

        # Test de la fonction qui va extraire les informations d'une page web contenant les informations d'un téléphone 
    # sur le premier site (lesmobiles.com)
    def test_getDataFromExtractor1(self):
    # GIVEN
        url = 'https://www.lesmobiles.com/telephones/motorola-one-macro,fiche-technique.html'
        scrap = Scraper()
        extrac = Extractor("https://www.lesmobiles.com")
        result = {'Nom': 'Motorola One Macro', 'Marque': 'Motorola', 'Taille Ecran(en pouces)': '6.2 ', 'Dimensions': '149,5 x 72 x 8,1 ', 'Poids(en g)': '160 ', 'OS': 'Android 9.0 Pie', 'Processeur': 'MediaTek Helio P70 - 2.1 GHz', 'Prix(prix en euros)': 229, 'RAM': '4', 'Mémoire': '64 ', 'Appareil photo': '13'}
    # WHEN
        html = scrap.scrapUrl(url)
        r = extrac.getDataFromTechnicalReviewPage(html)
    # THEN
        self.assertEqual (result, r)

    # Test de la fonction qui va extraire les informations d'une page web contenant les informations d'un téléphone 
    # sur le deuxième site (kimovil.com)
    def test_getDataFromExtractor2(self):
    # GIVEN
        url = 'https://www.kimovil.com/fr/ou-acheter-xiaomi-redmi-note-8-pro'
        scrap = Scraper()
        extrac = Extractor2("https://www.kimovil.com/fr/")
        result = {'Nom': '  Redmi Note 8 Pro\n', 'Marque': 'Xiaomi', 'Taille Ecran(en pouces)': '\n6.53\n', 'Dimensions': '\n76,4  x 161,3  x 8,8 \n', 'Poids(en g)': '\n199 \n','OS': 'MIUI V11 (Android 9 P)', 'Processeur': '\nMediaTek Helio G90T\n', 'Prix(prix en euros)': '178.54', 'RAM': '\n6', 'Mémoire': '\n64', 'Appareil photo': '\n64'}
    # WHEN
        html = scrap.scrapUrl(url)
        r = extrac.getDataFromTechnicalReviewPage(html)
    # THEN
        self.assertEqual (result, r)

unittest.main()

