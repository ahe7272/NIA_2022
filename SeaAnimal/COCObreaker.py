import json
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

running_COCO = input('COCO 제이슨 파일 경로 : ') +'\\labels.json'
objects = getjson(running_COCO)

for image in objects['images']:
    coco = objects.copy()
    coco['images'] = image
    annotations = []
    cnt = 1
    for annotation in objects['annotations']:
        if annotation['image_id'] == image['id']:
            annotation['id'] = cnt
            annotation['image_id'] = 1
            annotations.append(annotation)
            cnt += 1
    coco['annotations'] = annotations
    coco['images']['id'] = 1
    with open('/'.join(running_COCO.split('\\')[:-1]) + '/' + image['file_name'][:-4] + '.json', 'w') as j:
        json.dump(coco, j, indent='\t')
        j.close()
    