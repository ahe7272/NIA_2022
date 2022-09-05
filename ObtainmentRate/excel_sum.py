import pandas as pd
from glob import glob

excellist = glob('NIA_2022\ObtainmentRate\Rate_excels\*.xlsx')
print(excellist)
test_df = pd.read_excel(excellist[0])

# 근, 중, 원, 합계
dist0 = pd.Series([0 for i in range(len(test_df))])
dist1 = pd.Series([0 for i in range(len(test_df))])
dist2 = pd.Series([0 for i in range(len(test_df))])
dist3 = pd.Series([0 for i in range(len(test_df))])

for excel in excellist:
    df = pd.read_excel(excel)
    dist0 += df['Near']
    dist1 += df['Mid']
    dist2 += df['Far']
    dist3 += df['Total']

# classname = pd.Series(['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope','Rubber_etc',  'Rubber_tire', 'Etc'])
classname = pd.Series(['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus'])

df = pd.concat([classname, dist0, dist1, dist2, dist3], axis=1)
df = df.rename({0 : 'classname', 1 : 'Near', 2 : 'Mid', 3 : 'Far', 4 : 'Total'}, axis=1)
df.to_excel('Obtainment_rate.xlsx')


