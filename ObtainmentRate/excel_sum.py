import pandas as pd
from glob import glob

excellist = glob('NIA_2022\ObtainmentRate\Rate_excels\SunkenDebris\*.xlsx')
test_df = pd.read_excel(excellist[0])

# 근, 중, 원, 합계
Near_Total = pd.Series([0 for i in range(len(test_df))])
Mid_Total = pd.Series([0 for i in range(len(test_df))])
Far_Total = pd.Series([0 for i in range(len(test_df))])
Total = pd.Series([0 for i in range(len(test_df))])

for excel in excellist:
    df = pd.read_excel(excel)
    Near_Total += df['Near']
    Mid_Total += df['Mid']
    Far_Total += df['Far']
    Total += df['Total']

classname = pd.Series(['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope','Rubber_etc',  'Rubber_tire', 'Etc'])
# classname = pd.Series(['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus'])

df = pd.concat([classname, Near_Total, Mid_Total, Far_Total, Total], axis=1)
df = df.rename({0 : 'classname', 1 : 'Near', 2 : 'Mid', 3 : 'Far', 4 : 'Total'}, axis=1)
df.to_excel('NIA_2022\ObtainmentRate\Rate_excels\Obtainment_rate.xlsx')


