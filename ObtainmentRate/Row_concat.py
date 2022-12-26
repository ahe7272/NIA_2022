import pandas as pd
import os 

total = pd.Series(['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus'])

excels = input('경로: ')
for root, dirs, files in os.walk(excels):
    excellist = [Json for Json in files if Json.lower().endswith('xlsx')]
    for excel in excellist:
        df = pd.read_excel(root + '/' + excel)
        total = pd.concat([total, df], axis=0)
    total.to_excel('D:/Sea_total.xlsx')