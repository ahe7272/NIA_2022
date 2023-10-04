"""
Dataset 유지보수를 위한 코드 리펙토링

1. 조식동물별 거리 데이터 관리 방식 변경(하드코딩 -> 딕셔너리)
2. 반복문 구조 간소화
3. 유지보수 및 재사용성 강화를 위한 함수 목록 재구성
"""

import json
import os
import numpy as np
import shutil

SEA_ANIMALS = {
    'Asterias_amurensis': {'far': 5.0938, 'near': 20.3752},
    'Asterina_pectinifera': {'far': 1.7, 'near': 6.8},
    'Conch': {'far': 0.3692, 'near': 1.4769},
    'Ecklonia_cava': {'far': 0, 'near': 0},
    'Heliocidaris_crassispina': {'far': 1.3, 'near': 5.1},
    'Hemicentrotus': {'far': 0.6, 'near': 2.4},
    'Sargassum': {'far': 0, 'near': 0},
    'Sea_hare': {'far': 3.6, 'near': 14.6},
    'Turbo_cornutus': {'far': 1.5, 'near': 5.9}
}

SAVE_PATH = 'C:/Users/Administrator/Desktop/test'


def get_json(jsonfile):
    with open(jsonfile) as j:
        return json.load(j)


def calculate_object_size(points, shape_type):
    if shape_type == 'rectangle':
        object_width = abs(points[0][0] - points[1][0])
        object_height = abs(points[0][1] - points[1][1])
    else:
        y = [point[0] for point in points]
        x = [point[1] for point in points]
        object_height = max(y) - min(y)
        object_width = max(x) - min(x)
    return object_height * object_width


def ratio_of_objects(objects):
    image_size = objects['imageHeight'] * objects['imageWidth']
    max_ratio = 0
    label_with_ratio = []

    for shape in objects['shapes']:
        if shape['label'] == 'Etc':
            continue

        object_size = calculate_object_size(shape['points'], shape['shape_type'])
        ratio = (object_size / image_size) * 100
        max_ratio = max(max_ratio, ratio)
        label_with_ratio.append((shape['label'], ratio))

    return max_ratio, label_with_ratio


def classify_distance_4_sea_animal(max_ratio, max_label):
    animal_data = SEA_ANIMALS.get(max_label, {})
    if max_ratio <= animal_data.get('far', 0):
        return 'Far'
    elif animal_data.get('far', 0) < max_ratio <= animal_data.get('near', 0):
        return 'Mid'
    else:
        return 'Near'


def process_files(path):
    for root, _, files in os.walk(path):
        json_files = [f for f in files if f.lower().endswith('json')]

        for json_file in json_files:
            json_path = os.path.join(root, json_file)
            objects = get_json(json_path)

            if not objects['shapes']:
                continue

            max_ratio, label_with_ratio = ratio_of_objects(objects)
            max_label = max(label_with_ratio, key=lambda x: x[1])[0]

            distance_flag = classify_distance_4_sea_animal(max_ratio, max_label)

            if max_label == 'Heliocidaris_crassispina' and distance_flag in ['Mid', 'Far']:
                shutil.copy(json_path, os.path.join(SAVE_PATH, f'{distance_flag}{json_file}'))
                shutil.copy(json_path[:-4] + 'jpg', os.path.join(SAVE_PATH, f'{distance_flag}{json_file[:-4]}jpg'))
            elif max_label == 'Asterina_pectinifera' and objects['Distance'] in [0.5, 1.0]:
                distance = 'Near' if objects['Distance'] == 0.5 else 'Mid'
                shutil.copy(json_path, os.path.join(SAVE_PATH, f'{distance}{json_file}'))
                shutil.copy(json_path[:-4] + 'jpg', os.path.join(SAVE_PATH, f'{distance}{json_file[:-4]}jpg'))


if __name__ == "__main__":
    input_path = input("말똥성게를 찾을 폴더 경로를 입력하세요.\n")
    process_files(input_path)
