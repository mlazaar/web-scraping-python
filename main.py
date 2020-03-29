from data.scraper import Scraper
from data.extractor import Extractor
from data.extractor2 import Extractor2
from services.analyzer import Analyzer
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

import json

# Récupération données JSON
with open('./config.json') as f:
  config = json.load(f)

lm_basic_url = config["lesmobiles"]["basic_url"]
lm_my_url = config["lesmobiles"]["my_url"]

km_basic_url = config["kimovil"]["basic_url"]
km_my_url = config["kimovil"]["my_url"]

# Initialisation dataframe & options panda
pd.set_option("display.precision", 2)
dataframe = pd.DataFrame()

def main():
    scrap_lm = Scraper()
    scrap_km = Scraper()
   
    extractor_lm = Extractor(lm_basic_url)
    extractor_km = Extractor2(km_basic_url)

    # Scrap du site internet choisi
    html_lm = scrap_lm.scrapUrl(lm_my_url)
    html_km = scrap_km.scrapUrl(km_my_url)

    # Récupération des données scrapées dans un dataframe
    dataF = extractor_lm.build(html_lm,dataframe)
    dataF = extractor_km.build(html_km,dataF)
    # Analyse du dataframe
    analyzer = Analyzer(dataF)
    analyzer.build()

    df = pd.read_csv('Phone.csv')

    # Corrélation
    plt.figure(figsize=(15,10))
    sns.heatmap(df.corr(), annot=True, cmap='Reds_r')
    plt.title("Matrice de corrélation\n", fontsize=18, color='#FF0000')
    plt.savefig('./output/correlation.pdf')  

    # Moyenne 
    df2 = df[['Prix(prix en euros)','Marque']].groupby('Marque').mean().round().sort_values(by='Prix(prix en euros)', ascending=False)
    df2.reset_index(0, inplace=True)
    plt.figure(figsize=(15,10))
    sns.barplot(x=df2['Marque'], y=df2['Prix(prix en euros)'], palette="Blues_r")
    plt.xlabel('Marque', fontsize=15, color='#2980b9')
    plt.ylabel("Prix moyen (en euros) du Smartphone\n", fontsize=15, color='#2980b9')
    plt.title("En moyenne le smartphone le plus cher est  :  \n", fontsize=18, color='#3742fa')
    plt.xticks(rotation= 45)
    plt.tight_layout()
    plt.savefig('./output/mean.pdf') 
    
    # Boxplot
    df.plot.box()
    plt.savefig('./output/boxplot.pdf') 

main()