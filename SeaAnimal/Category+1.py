import json
import os

running_path = input('경로: ')

def handlejson(jsonfile, option, objects=''):
    if option == 'get':
        with open(jsonfile) as j:
            objects = json.load(j)        
        return objects
    elif option == 'save':
        with open(jsonfile, 'w') as j:
            json.dump(objects, j, indent='\t')

for (path, dir, files) in os.walk(running_path):
    for file in files:
        if file.lower().endswith('.json'):
            objects = handlejson(jsonfile = path + '/' + file, option = 'get')
            for id in objects['categories']:
                id['id'] = id['id'] + 1
            for annotation in objects['annotations']:
                annotation['category_id'] = annotation['category_id'] + 1
            handlejson(jsonfile = path + '/'+ file, option='save', objects = objects)