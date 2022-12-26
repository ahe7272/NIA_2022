import fiftyone as fo
import os
import json
import numpy as np
import cv2 


def handlejson(jsonfile, option, objects=''):
    if option == 'get':
        with open(jsonfile) as j:
            objects = json.load(j)        
        return objects
    elif option == 'save':
        with open(jsonfile, 'w') as j:
            json.dump(objects, j, indent='\t')

def getMask(shape):
    imgH = 2160
    imgW = 3840

    mask = np.zeros((imgH, imgW, 1))
    point = shape['points']
    point = np.array(point, np.int32)
    mask = cv2.fillConvexPoly(mask, point, 255)
    return mask

dataset = fo.Dataset()
dataset.default_classes = ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']
dataset.save()
labels = ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']
all_path = input('경로 : ')

samples = []

for (path, dir, files) in os.walk(all_path):
    for file in files:
        if file.lower().endswith('.json'):
            objects = handlejson(jsonfile=path + '/'+file, option='get')
            sample = fo.Sample(filepath=path + '/' + file[:-5] + '.jpg')
            detections = []
            for shape in objects['shapes']:
                labelidx = labels.index(shape['label'])
                label = dataset.default_classes[labelidx]
                if shape['shape_type'] == 'rectangle':
                    box_width = abs(shape['points'][0][0] - shape['points'][1][0])
                    box_height = abs(shape['points'][0][1] - shape['points'][1][1])
                    left_top_x = min(shape['points'][0][0], shape['points'][1][0])
                    left_top_y = min(shape['points'][0][1], shape['points'][1][1])
                    bounding_box = [left_top_x, left_top_y, box_width, box_height]
                    # Meta = {"Size": 0, "Weight": 0, "points": []}
                    Meta = {"Size": shape['Size'], "Weight": shape['Weight'], "points": []}
                    detections.append(fo.Detection(label=label, bounding_box=bounding_box, **Meta))

                elif shape['shape_type'] == 'polygon':
                    xlist = np.array(shape['points'])[:,0]
                    ylist = np.array(shape['points'])[:,1]
                    left_top_x = abs(min(xlist))
                    left_top_y = abs(min(ylist))
                    box_width = abs(max(xlist) - left_top_x)
                    box_height = abs(max(ylist) - left_top_y)
                    bounding_box = [left_top_x, left_top_y, box_width, box_height]
                    # mask = getMask(shape)
                    Meta = {"Size": 0, "Weight": 0, "points":  [sum(shape['points'][:],[])]}
                    detections.append(fo.Detection(label=label, bounding_box=bounding_box, mask=np.array( [sum(shape['points'][:],[])]), **Meta))
                # print(fo.Detection(label=label, bounding_box=bounding_box, mask=mask, **Meta))
                else:
                    print('label_type 확인 필요.' + '\n' + path + '/' + file)
                    break

            sample["Detection"] = fo.Detections(detections=detections)
    
            samples.append(sample)
# Create dataset
print('add_samples...')
dataset.add_samples(samples)
dataset.save()  # must save after edits

print('export...')
# Export the datasetB

dataset.export(
    export_dir= all_path,
    dataset_type=fo.types.COCODetectionDataset,
    label_field="Detection",
    extra_attrs = {'Size', 'Weight', 'points'}
)
objects = handlejson(jsonfile=all_path + '/labels.json', option='get')
for anno in objects['annotations']:
    try:
        anno.pop('segmentation')
        anno['segmentation'] = anno['points']
        anno.pop('points')
    except:
        anno['segmentation'] = []
        anno.pop('points')
handlejson(jsonfile=all_path + '/labels.json', option='save', objects= objects)
