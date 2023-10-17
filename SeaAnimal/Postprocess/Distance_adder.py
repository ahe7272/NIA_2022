"""
데이터셋 유지보수를 위한 리펙토링 버전

1) 조건문의 구조 간결화를 통한 가독성 개선
2) 함수명을 Camel CAse로 변경
3) 데이터를 딕셔너리로 관리하여 코드 중복 개선
"""

import json
import numpy as np
from classes import seaAnimalDict

def loadJson(jsonFile):
    with open(jsonFile, 'r') as j:
        return json.load(j)

classesDict = seaAnimalDict()

def calculateRatio(objects):
    imageArea = objects['imageHeight'] * objects['imageWidth']
    maxRatio = 0
    labelWithRatio = []

    for shape in objects['shapes']:
        points = np.array(shape['points'])

        if shape['shape_type'] == 'rectangle':
            objectWidth = abs(points[0, 0] - points[1, 0])
            objectHeight = abs(points[0, 1] - points[1, 1])
        else:  # polygon
            y = points[:, 0]
            x = points[:, 1]
            objectHeight = max(y) - min(y)
            objectWidth = max(x) - min(x)

        objectRatio = (objectHeight * objectWidth) / imageArea * 100
        maxRatio = max(maxRatio, objectRatio)
        labelWithRatio.append((shape['label'], objectRatio))

    return maxRatio, labelWithRatio

def classifyDistanceForDebris(maxRatio):
    if maxRatio <= 20:
        return 'Far'
    elif maxRatio <= 60:
        return 'Mid'
    return 'Near'

def classifyDistanceForSeaAnimal(maxRatio, maxLabel):
    animalRatios = {
        'Asterias_amurensis': (0.9, 8.09),
        'Asterina_pectinifera': (0.38, 3.39),
        'Conch': (0.06, 0.5),
        'Ecklonia_cava': (0, 0),
        'Heliocidaris_crassispina': (0.2, 1.78),
        'Hemicentrotus': (0.7, 0.6),
        'Sargassum': (0, 0),
        'Sea_hare': (0.84, 7.53),
        'Turbo_cornutus': (0.27, 2.43)
    }

    farRatio, nearRatio = animalRatios.get(maxLabel, (0, 0))

    if maxRatio <= farRatio:
        return 'Far'
    elif maxRatio <= nearRatio:
        return 'Mid'
    return 'Near'
