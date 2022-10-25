import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import pandas as pd
import copy
import shutil

path = input("지역별 구분을 위한 폴더 경로를 입력하세요.\n")

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

# 이미지내 객체 비율
def site_of_file(jsonfile, objects, name):
    lat = objects['Latitude']
    lon = objects['Longitude']
    West_sea = [34.364395, 37.71018, 124.6, 126.787022] 
    East_sea = [35.057934, 38.61811, 128.385259, 131.87]
    South_sea = [33.925710, 35.057934, 126.0884, 129.376183]
    Jeju_sea = [33.08692, 33.925710, 125.999, 127.3037]
    os.makedirs(path +'/West', exist_ok=True)
    os.makedirs(path +'/East', exist_ok=True)
    os.makedirs(path +'/South', exist_ok=True)
    os.makedirs(path +'/Jeju', exist_ok=True)
    os.makedirs(path +'/Undecided', exist_ok=True)

    if (lat <= West_sea[1]) and (lat >= West_sea[0]) and (lon <= West_sea[3]) and (lon >= West_sea[2]):
        shutil.move(jsonfile, path +'/West/' + name)
        return 'West'
    elif (lat <= East_sea[1]) and (lat >= East_sea[0]) and (lon <= East_sea[3]) and (lon >= East_sea[2]):
        shutil.move(jsonfile, path +'/East/' + name)
        return 'East'    
    elif (lat <= South_sea[1]) and (lat >= South_sea[0]) and (lon <= South_sea[3]) and (lon >= South_sea[2]):
        shutil.move(jsonfile, path +'/South/' + name)
        return 'South'
    elif (lat <= Jeju_sea[1]) and (lat >= Jeju_sea[0]) and (lon <= Jeju_sea[3]) and (lon >= Jeju_sea[2]):
        shutil.move(jsonfile, path +'/Jeju/' + name)
        return 'Jeju'
    else:
        print(jsonfile)
        shutil.move(jsonfile, path +'/Undecided/' + name)
        return 'Undecided'

for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        if len(objects['shapes']) == 0:
            print(Json)
            continue   
        site = site_of_file(jsonfile, objects, name+'.json')