"""
다른 프로젝트를 위해 코드 리펙토링

1. 중복코드 제거
2. 유지보수 및 재사용을 위한 코드 가독성 개선
3. 인지적 리펙토링 기법 적용
4. 함수 및 변수명 일부 수정
"""

import fiftyone as fo
import os
import json
import numpy as np
import cv2

def load_or_save_json(json_path, mode, data=None):
    if mode == 'load':
        with open(json_path, 'r') as file:
            return json.load(file)
    elif mode == 'save':
        with open(json_path, 'w') as file:
            json.dump(data, file, indent='\t')

def compute_bounding_box(points):
    x_coords, y_coords = zip(*points)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    return [min_x, min_y, max_x - min_x, max_y - min_y]

def create_dataset_from_json(json_path, image_path, labels):
    objects = load_or_save_json(json_path, 'load')
    sample = fo.Sample(filepath=image_path)
    detections = []

    for shape in objects['shapes']:
        label = labels[shape['label']]
        bounding_box = compute_bounding_box(shape['points'])
        meta = {"Size": shape.get('Size', 0), "Weight": shape.get('Weight', 0), "points": shape['points']}
        
        if shape['shape_type'] == 'rectangle':
            detections.append(fo.Detection(label=label, bounding_box=bounding_box, **meta))
        elif shape['shape_type'] == 'polygon':
            detections.append(fo.Detection(label=label, bounding_box=bounding_box, mask=np.array(shape['points']), **meta))
        else:
            print(f'Unknown label_type in {json_path}')
            break

    sample["Detection"] = fo.Detections(detections=detections)
    return sample

def main():
    dataset = fo.Dataset()
    labels = ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']
    label_map = {label: label for label in labels}
    dataset.default_classes = labels
    dataset.save()

    root_path = input('경로 : ')
    samples = []

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.lower().endswith('.json'):
                json_path = os.path.join(dirpath, filename)
                image_path = os.path.join(dirpath, filename[:-5] + '.jpg')
                samples.append(create_dataset_from_json(json_path, image_path, label_map))

    dataset.add_samples(samples)
    dataset.save()

    dataset.export(
        export_dir=root_path,
        dataset_type=fo.types.COCODetectionDataset,
        label_field="Detection",
        extra_attrs={'Size', 'Weight', 'points'}
    )

    annotations_path = os.path.join(root_path, 'labels.json')
    annotations = load_or_save_json(annotations_path, 'load')
    for anno in annotations['annotations']:
        anno['segmentation'] = anno.pop('points', [])
    load_or_save_json(annotations_path, 'save', annotations)

if __name__ == "__main__":
    main()
