import PySimpleGUI as sg
import os
import json
import shutil
import numpy as np

class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')
        layout = [
                  [sg.Text('POSTPROCESS', font =("Arial", 30, 'bold'), text_color = 'Skyblue')], 
                  [sg.Text(' PATH', font =("Arial", 15)), sg.InputText( font =("Arial", 15, 'bold'), size=(20, 1), key='Path'), sg.FolderBrowse('SELECT', font =("Arial", 10, 'bold'), size=(8, 1))],
                  [sg.Text(' LABEL TYPE', font =("Arial", 15)), sg.Checkbox('POLYGON', font =("Arial", 10, 'bold'), size=(8, 1), key='Polygon'), sg.Checkbox('BBOX', font =("Arial", 10, 'bold'), size=(8, 1), key='Bbox'), sg.Button('RUN', font =("Arial", 10, 'bold'), size=(8, 1), key='Run')],
                  [sg.ProgressBar(1, orientation='h', size=(40, 20), key='progress')]
                  ]
        window = sg.Window('After AllbigDat', layout, grab_anywhere = True).Finalize()
        return window

def handlejson(jsonfile, option, objects=''):
    if option == 'get':
        with open(jsonfile) as j:
            objects = json.load(j)        
        return objects
    elif option == 'save':
        with open(jsonfile, 'w') as j:
            json.dump(objects, j, indent='\t')

m = MakeGUI()
window = m.makegui()
duplicates = []
latlon_error = []
attr_error = []
polygon_in_bbox = []
bbox_in_polygon = []
file_list = []
empty_label = []
wrong_label = [] 

try:
    while True:    
        event, values = window.read()    
        progress_bar = window.find_element('progress')
        if event == 'Run':
            cnt = 0
            file_length = 0
            dup_path = values['Path'] + '/Duplicates/'
            latlon_error_path = values['Path'] + '/Latlon_errors/'
            attr_error_path = values['Path'] + '/Attr_errors/'
            polygon_in_bbox_path = values['Path'] + '/Polygon_in_bbox/'
            bbox_in_polygon_path = values['Path'] + '/Bbox_in_polygon/'
            empty_label_path = values['Path'] + '/Empty_label/'
            wrong_label_path = values['Path'] + '/Wrong_label/'

            for (path, dir, files) in os.walk(values['Path']):
                file_length += len([Json for Json in files if Json.lower().endswith('.json')])
            progress_bar.UpdateBar(0, file_length)
            for (path, dir, files) in os.walk(values['Path']):
                jsonlist = [Json for Json in files if Json.lower().endswith('.json')]
                path = path.replace('\\', '/')
                for j in jsonlist:
                    shape_flag = False
                    jsonfile = path + '/' + j
                    if j in file_list:
                        duplicates += [jsonfile]
                        os.makedirs(dup_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    else:
                        file_list += [j]
                    jsonfile = path + '/' + j
                    objects = handlejson(jsonfile=jsonfile, option='get')
                    
                    for t in range(len(objects['shapes']) - 1, -1, -1):
                        points = objects['shapes'][t]['points'] 
                        points = np.array(points, np.int32)

                        # boundingbox
                        if objects['shapes'][t]['shape_type'] == 'rectangle':
                            lefttopx, lefttopy = points[0]
                            rightdownx, rightdowny = points[1]

                        #polygon
                        else:
                            x = points[:, 0]
                            y = points[:, 1]
                            lefttopx = min(x)
                            rightdownx = max(x)
                            lefttopy = min(y)
                            rightdowny = max(y)
                        if (max(lefttopx, rightdownx, lefttopy, rightdowny) > 3840) or (min(lefttopx, rightdownx, lefttopy, rightdowny) < 0):
                            print(jsonfile + '에 라벨링 좌표 이상')
                        w = max(lefttopx, rightdownx) - min(lefttopx, rightdownx)
                        h = max(lefttopy, rightdowny) - min(lefttopy, rightdowny)
                        area = w * h 
                        if area <= 1024:
                            del(objects['shapes'][t])   
                    objects['imageData'] = None
                    objects['Latitude'] = round(objects['Latitude'],6)
                    objects['Longitude'] = round(objects['Longitude'],6)

                    handlejson(jsonfile=jsonfile, option='save', objects=objects)

                    if (100 > objects['Longitude']) or (objects['Latitude'] > 50):
                        latlon_error += [jsonfile]
                        os.makedirs(latlon_error_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    if len(objects) != 23:
                        attr_error += [jsonfile]
                        os.makedirs(attr_error_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    if len(objects['shapes']) == 0:
                        empty_label += [jsonfile]
                        os.makedirs(empty_label_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    
                    handlejson(jsonfile=jsonfile, option='save', objects=objects)
                    for shape in objects['shapes']:
                        if shape['label'] not in ['Ecklonia_cava', 'Sargassum', 'Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sea_hare', 'Turbo_cornutus']:
                            wrong_label += [jsonfile]
                            os.makedirs(wrong_label_path + path.split('/')[-1] , exist_ok=True)
                            shape_flag = True
                            break
                        elif (shape['shape_type'] == 'polygon') and (values['Bbox']):
                            polygon_in_bbox += [jsonfile]
                            os.makedirs(polygon_in_bbox_path + path.split('/')[-1], exist_ok=True)
                            shape_flag = True
                            break
                        elif (shape['shape_type'] == 'polygon') and (shape['label'] not in ['Ecklonia_cava', 'Sargassum']):
                            polygon_in_bbox += [jsonfile]
                            os.makedirs(polygon_in_bbox_path + path.split('/')[-1], exist_ok=True)
                            shape_flag = True
                            break
                        elif (shape['shape_type'] == 'rectangle') and (values['Polygon']):
                            bbox_in_polygon += [jsonfile]
                            os.makedirs(bbox_in_polygon_path + path.split('/')[-1], exist_ok=True)
                            shape_flag = True
                            break
                        elif (shape['shape_type'] == 'rectangle') and (shape['label'] in ['Ecklonia_cava', 'Sargassum']):
                            bbox_in_polygon += [jsonfile]
                            os.makedirs(bbox_in_polygon_path + path.split('/')[-1], exist_ok=True)
                            shape_flag = True
                            break
                    if shape_flag:
                        cnt += 1
                        continue
                    else:
                        cnt += 1
                    progress_bar.UpdateBar(cnt, file_length)
                if cnt == file_length:
                    progress_bar.UpdateBar(cnt, file_length)
                    for duplicated_file in duplicates:
                        shutil.move(duplicated_file, dup_path + duplicated_file.split('/')[-2] + '/' + duplicated_file.split('/')[-1])
                        shutil.move(duplicated_file[:-5] + '.jpg', dup_path + duplicated_file.split('/')[-2] + '/' + duplicated_file.split('/')[-1][:-5] + '.jpg')
                    for latlon_error_file in latlon_error:
                        shutil.move(latlon_error_file, latlon_error_path + latlon_error_file.split('/')[-2] + '/' + latlon_error_file.split('/')[-1])
                        shutil.move(latlon_error_file[:-5] + '.jpg', latlon_error_path + latlon_error_file.split('/')[-2] + '/' + latlon_error_file.split('/')[-1][:-5] + '.jpg')
                    for attr_error_file in attr_error:
                        shutil.move(attr_error_file, attr_error_path + attr_error_file.split('/')[-2] + '/' + attr_error_file.split('/')[-1])
                        shutil.move(attr_error_file[:-5] + '.jpg', attr_error_path + attr_error_file.split('/')[-2] + '/' + attr_error_file.split('/')[-1][:-5] + '.jpg')
                    for polygon_file in polygon_in_bbox:
                        shutil.move(polygon_file, polygon_in_bbox_path + polygon_file.split('/')[-2] + '/' + polygon_file.split('/')[-1])
                        shutil.move(polygon_file[:-5] + '.jpg', polygon_in_bbox_path + polygon_file.split('/')[-2] + '/' + polygon_file.split('/')[-1][:-5] + '.jpg')
                    for bbox_file in bbox_in_polygon:
                        shutil.move(bbox_file, bbox_in_polygon_path + bbox_file.split('/')[-2] + '/' + bbox_file.split('/')[-1])
                        shutil.move(bbox_file[:-5] + '.jpg', bbox_in_polygon_path + bbox_file.split('/')[-2] + '/' + bbox_file.split('/')[-1][:-5] + '.jpg')
                    for empty_file in empty_label:
                        shutil.move(empty_file, empty_label_path + empty_file.split('/')[-2] + '/' + empty_file.split('/')[-1])
                        shutil.move(empty_file[:-5] + '.jpg', empty_label_path + empty_file.split('/')[-2] + '/' + empty_file.split('/')[-1][:-5] + '.jpg')
                    for wrong_file in wrong_label:
                        shutil.move(wrong_file, wrong_label_path + wrong_file.split('/')[-2] + '/' + wrong_file.split('/')[-1])
                        shutil.move(wrong_file[:-5] + '.jpg', wrong_label_path + wrong_file.split('/')[-2] + '/' + wrong_file.split('/')[-1][:-5] + '.jpg')
                    sg.Popup('Postprocess 완료^^!', font =("Arial", 13), keep_on_top=True)
                    break
        if event in (None, 'Exit'):
            break
except Exception as e:
    print(e)
    window.close()

