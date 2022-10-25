import PySimpleGUI as sg
import os
import json
import shutil
import io
from PIL import Image, ImageFilter
import base64
import cv2
import numpy as np
from Distance_adder import ratio_of_objects, classify_distance_4_seaanimal

class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')
        layout = [
                  [sg.Text('POSTPROCESS', font =("Arial", 30, 'bold'), text_color = 'Skyblue')], 
                  [sg.Text(' PATH', font =("Arial", 15)), sg.InputText( font =("Arial", 15, 'bold'), size=(20, 1), key='Path'), sg.FolderBrowse('SELECT', font =("Arial", 10, 'bold'), size=(8, 1))],
                  [sg.Text(' LABEL TYPE', font =("Arial", 15)), sg.Checkbox('POLYGON', font =("Arial", 10, 'bold'), size=(8, 1), key='Polygon'), sg.Checkbox('BBOX', font =("Arial", 10, 'bold'), size=(8, 1), key='Bbox'), sg.Button('RUN', font =("Arial", 10, 'bold'), size=(8, 1), key='Run')],
                  [sg.ProgressBar(1, orientation='h', size=(40, 20), key='progress')]
                  ]
        window = sg.Window('Postprocess', layout, grab_anywhere = True).Finalize()
        return window

def handlejson(jsonfile, option, objects=''):
    if option == 'get':
        with open(jsonfile) as j:
            objects = json.load(j)        
        return objects
    elif option == 'save':
        with open(jsonfile, 'w') as j:
            json.dump(objects, j, indent='\t')

def restore_img(originals_path, path, objects, jsonfile):
    try:
        Databin = objects['Origin_img'].encode('utf-8')
        f = io.BytesIO()
        f.write(base64.b64decode(Databin))
        img = np.array(Image.open(f))
        objects.pop('Origin_img')
        cv2.imwrite(originals_path + jsonfile[:-5] + '.jpg', img)
        return objects

    except:
        try:
            if os.path.isfile(originals_path + jsonfile[:-5] + '.jpg'):
                return objects
            else:
                src = cv2.imread(path + '/' + jsonfile[:-5] + '.jpg' , cv2.IMREAD_COLOR)
                alpha1 = -0.5 
                alpha2 = -0.3

                b, g, r = cv2.split(src)

                bdst = np.clip((1 + alpha1) * b - 128 * alpha1, 0, 255).astype(np.uint8)
                gdst = np.clip((1 + alpha1) * g - 128 * alpha1, 0, 255).astype(np.uint8)
                rdst = np.clip((1 + alpha1) * r - 128 * alpha2, 0, 255).astype(np.uint8)
                
                img = cv2.merge((rdst, gdst, bdst))
                img = Image.fromarray(img)

                blured = img.filter(ImageFilter.BoxBlur(3))  

                name = jsonfile[:-5] + '.jpg'
                blured.save(originals_path + name)
                objects.pop('Origin_img')
                return objects
        except:
            # print(path + '/' + jsonfile)
            return objects

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
            originals_path = values['Path'] + '/Originals/'
            polygon_in_bbox_path = values['Path'] + '/Polygon_in_bbox/'
            bbox_in_polygon_path = values['Path'] + '/Bbox_in_polygon/'
            empty_label_path = values['Path'] + '/Empty_label/'
            wrong_label_path = values['Path'] + '/Wrong_label/'

            os.makedirs(originals_path, exist_ok=True)

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
                    objects = handlejson(jsonfile=jsonfile, option='get')
                    objects['imageData'] = None
                    objects['Latitude'] = round(objects['Latitude'],6)
                    objects['Longitude'] = round(objects['Longitude'],6)
                    objects = restore_img(originals_path, path, objects, j)
                    
                    handlejson(jsonfile=jsonfile, option='save', objects=objects)
                    if (100 > objects['Longitude']) or (objects['Latitude'] > 50):
                        latlon_error += [jsonfile]
                        os.makedirs(latlon_error_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    if len(objects['shapes']) == 0:
                        empty_label += [jsonfile]
                        os.makedirs(empty_label_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    maxratio, label_with_ratio = ratio_of_objects(objects)
                    if len(label_with_ratio) > 1:
                        for label, ratio in label_with_ratio:
                            if maxratio == ratio:
                                maxlabel = label
                    else:
                        maxlabel = label_with_ratio[0][0]   
                    if (maxlabel not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sea_hare', 'Turbo_cornutus']):
                        print(j)
                    distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)
                    if maxlabel not in ['Ecklonia_cava', 'Sargassum']:
                        if distance_flag == 'Near':
                            objects['Distance'] = 0.5
                        elif distance_flag == 'Mid':
                            objects['Distance'] = 1.0
                        elif distance_flag == 'Far':
                            objects['Distance'] = 1.5
                    if len(objects['Source_video'].split('ROV')) > 1:
                        objects['Collection_method'] = 'ROV'
                    else:
                        objects['Collection_method'] = 'Diver'
                    handlejson(jsonfile=jsonfile, option='save', objects=objects)
                    if len(objects) != 24:
                        attr_error += [jsonfile]
                        os.makedirs(attr_error_path + path.split('/')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    for shape in objects['shapes']:
                        if shape['label'] not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']:
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
                    progress_bar.UpdateBar(cnt+2, file_length)

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

