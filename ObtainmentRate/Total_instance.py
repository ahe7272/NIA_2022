import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import pandas as pd
import copy

path = input("달성도 excel 파일 생성을 위한 주차 작업물 폴더 경로를 입력하세요.\n")
D_or_S = input("침적 데이터면 D, 조식동물이면 S를 입력해주세요. ")
if D_or_S == 'D':
    savepath = 'C:/Users/Administrator/Documents/Github/NIA_2022/ObtainmentRate/Rate_excels/SunkenDebris'
    classes_dict= debris_dict()
elif D_or_S == 'S':
    savepath = 'C:/Users/Administrator/Documents/Github/NIA_2022/ObtainmentRate/Rate_excels/SeaAnimals'
    classes_dict= sea_animal_dict()
else:
    exit()

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

dict_total = copy.deepcopy(classes_dict)
for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        if len(objects['shapes']) == 0:
            print(Json)
            continue   
        labeldict = copy.deepcopy(classes_dict)
        for label in objects['shapes']:
            labeldict[label['label']] += 1
        for k, v in labeldict.items():
            dict_total[k] += v
         

        # df_single = pd.DataFrame(list(labeldict.values()), columns=[Json]).transpose()    
        # df_stat = pd.concat([df_stat, df_single])
print(dict_total)

# df_stat.to_excel(savepath + '/Area.xlsx')

# # 해역별 존재 전체 해역별 출현 횟수 산출
# Sea_list = {}
# for root, dirs, files in os.walk(path):
#     jsonarr = [Json for Json in files if Json.lower().endswith('json')]
#     for Json in jsonarr:
#         name = os.path.splitext(Json)[0]
#         jsonfile = os.path.join(root, name + '.json')
#         objects = getjson(jsonfile)
#         if objects['Site_']
#         for label in objects['shapes']:
#             labeldict[label['label']] += 1
#         for k, v in labeldict.items():
#             dict_total[k] += v