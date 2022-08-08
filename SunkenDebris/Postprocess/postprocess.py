import PySimpleGUI as sg
import os
import geopandas
import shapefile
from shapely.geometry import Point, LineString
from pyproj import Proj, transform
import json
import io
from PIL import Image, ImageFilter
import base64
import cv2
import numpy as np
import shutil

pre_gdf = geopandas.read_file('NIA_2022/SunkenDebris/Postprocess/coastline.geojson')

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

def change_coordinate(point):
    epsg32652 = Proj(init='epsg:32652')
    wgs84 = Proj(init='epsg:4326')
    # epsg32652는 m 단위
    X1, Y1 = transform(wgs84, epsg32652, point[0], point[1])
    return (X1, Y1)

def makekoreacoastline():
    # epsg32652로 바꾼 shape파일
    shape = shapefile.Reader('coast/Z_NGII_N3L_E0080000_utm.shp')
    gdf = geopandas.GeoSeries([LineString([]) for i in range(len(shape))])
    for s in range(len(shape.shapeRecords())):
        feature = shape.shapeRecords()[s]
        first = feature.shape.__geo_interface__  
        coordinates = first['coordinates']
        gdf[s] = LineString(coordinates)  
    gdf.crs = 32652
    gdf.to_file('coastline.geojson', driver='GeoJSON')
    return gdf

def restore_img(originals_path, path, objects, jsonfile):
    try:
        Databin = objects['Origin_img'].encode('utf-8')
        f = io.BytesIO()
        f.write(base64.b64decode(Databin))
        img = np.array(Image.open(f))
        objects.pop('Origin_img')
        cv2.imwrite(originals_path + 'Original_'+ jsonfile[:-5] + '.jpg', img)
        return objects
    except:
        try:
            if os.path.isfile(originals_path + 'Original_' + jsonfile[:-5] + '.jpg'):
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

                name = 'Original_' + jsonfile[:-5] + '.jpg'
                blured.save(originals_path + name)
                objects.pop('Origin_img')
                return objects
        except:
            print(path + '/' + jsonfile)
            return objects

m = MakeGUI()
window = m.makegui()
attr_error = []
duplicates = []
polygon_in_bbox = []
bbox_in_polygon = []
file_list = []

try:
    while True:    
        event, values = window.read()    
        progress_bar = window.find_element('progress')
        if event == 'Run':
            cnt = 0
            file_length = 0
            dup_path = values['Path'] + '/Duplicates/'
            attr_error_path = values['Path'] + '/Attr_errors/'
            originals_path = values['Path'] + '/Originals/'
            polygon_in_bbox_path = values['Path'] + '/Polygon_in_bbox/'
            bbox_in_polygon_path = values['Path'] + '/Bbox_in_polygon/'
            os.makedirs(originals_path, exist_ok=True)

            for (path, dir, files) in os.walk(values['Path']):
                file_length += len([Json for Json in files if Json.lower().endswith('.json')])
            progress_bar.UpdateBar(0, file_length)
            for (path, dir, files) in os.walk(values['Path']):
                jsonlist = [Json for Json in files if Json.lower().endswith('.json')]
                for j in jsonlist:
                    if j in file_list:
                        duplicates += [path +'/' + j]
                        os.makedirs(dup_path + path.split('\\')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    else:
                        file_list += [j]
                    jsonfile = path + '/' + j
                    objects = handlejson(jsonfile=jsonfile, option='get')
                    objects['imageData'] = None
                    objects = restore_img(originals_path, path, objects, j)
                    if len(objects) != 14:
                        handlejson(jsonfile=jsonfile, option='save', objects=objects)
                        attr_error += [jsonfile]
                        os.makedirs(attr_error_path + path.split('\\')[-1] , exist_ok=True)
                        cnt += 1
                        continue
                    if objects['CDist'] == 0:
                        lat = objects['Latitude']
                        lon = objects['Longitude']
                        point = (lat, lon)
            
                        # flag = true : 해안선 코드 만들기
                        flag = False
                        point = change_coordinate(point)
                        point = Point(point)
                        point.crs = 32652

                        if flag:
                            gdf = makekoreacoastline()
                        else:
                            gdf = pre_gdf
                        distance = gdf.distance(point)

                        # 최소거리 
                        distance = round(distance.min(axis=0), 2)
                        objects['CDist'] = distance

                    handlejson(jsonfile=jsonfile, option='save', objects=objects)
                    cnt += 1

                    for shape in objects['shapes']:
                        if (shape['shape_type'] == 'polygon') and (values['Bbox']):
                            polygon_in_bbox += [jsonfile]
                            os.makedirs(polygon_in_bbox_path + path.split('\\')[-1], exist_ok=True)
                            break
                        elif (shape['shape_type'] == 'rectangle') and (values['Polygon']):
                            bbox_in_polygon += [jsonfile]
                            os.makedirs(bbox_in_polygon_path + path.split('\\')[-1], exist_ok=True)
                            break
                    progress_bar.UpdateBar(cnt, file_length)
                if cnt == file_length:
                    progress_bar.UpdateBar(cnt+2, file_length)
                    for duplicated_file in duplicates:
                        shutil.move(duplicated_file, dup_path + duplicated_file.split('\\')[-1])
                        shutil.move(duplicated_file[:-5] + '.jpg', dup_path + duplicated_file.split('\\')[-1][:-5] + '.jpg')
                        shutil.move(originals_path + 'Original_' + duplicated_file.split('/')[-1][:-5] + '.jpg', dup_path + duplicated_file.split('\\')[-1].split('/')[0] + '/Original_' + duplicated_file.split('/')[-1][:-5] + '.jpg')
                    for attr_error_file in attr_error:
                        shutil.move(attr_error_file, attr_error_path + attr_error_file.split('\\')[-1])
                        shutil.move(attr_error_file[:-5] + '.jpg', attr_error_path + attr_error_file.split('\\')[-1][:-5] + '.jpg')
                    for polygon_file in polygon_in_bbox:
                        shutil.move(polygon_file, polygon_in_bbox_path + polygon_file.split('\\')[-1])
                        shutil.move(polygon_file[:-5] + '.jpg', polygon_in_bbox_path + polygon_file.split('\\')[-1][:-5] + '.jpg')
                    for bbox_file in bbox_in_polygon:
                        shutil.move(bbox_file, bbox_in_polygon_path + bbox_file.split('\\')[-1])
                        shutil.move(bbox_file[:-5] + '.jpg', bbox_in_polygon_path + bbox_file.split('\\')[-1][:-5] + '.jpg')
                    sg.Popup('Postprocess 완료^^!', font =("Arial", 13), keep_on_top=True)
                    break
        if event in (None, 'Exit'):
            break
except Exception as e:
    print(e)
    window.close()

