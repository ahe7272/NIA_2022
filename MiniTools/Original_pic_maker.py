import PySimpleGUI as sg
import os
import json
import shutil
import io
from PIL import Image, ImageFilter
import base64
import cv2
import numpy as np

class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')
        layout = [
                  [sg.Text('POSTPROCESS', font =("Arial", 30, 'bold'), text_color = 'Skyblue')], 
                  [sg.Text(' PATH', font =("Arial", 15)), sg.InputText( font =("Arial", 15, 'bold'), size=(20, 1), key='Path'), sg.FolderBrowse('SELECT', font =("Arial", 10, 'bold'), size=(8, 1))],
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
    try :
        exist = objects['Origin_img']
    except:
        return objects

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
            print(path + '/' + jsonfile)
            return objects

m = MakeGUI()
window = m.makegui()


try:
    while True:    
        event, values = window.read()    
        progress_bar = window.find_element('progress')
        if event == 'Run':
            cnt = 0
            file_length = 0
            originals_path = values['Path'] + '/Originals/'
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

                    objects = handlejson(jsonfile=jsonfile, option='get')
                    objects['imageData'] = None
                    objects['Latitude'] = round(objects['Latitude'],2)
                    objects['Longitude'] = round(objects['Longitude'],2)
                    objects = restore_img(originals_path, path, objects, j)
                    
                    handlejson(jsonfile=jsonfile, option='save', objects=objects)
                    if shape_flag:
                        cnt += 1
                        continue
                    else:
                        cnt += 1
                    progress_bar.UpdateBar(cnt, file_length)
                if cnt == file_length:
                    progress_bar.UpdateBar(cnt+2, file_length)
                    sg.Popup('Postprocess 완료^^!', font =("Arial", 13), keep_on_top=True)
                    break
        if event in (None, 'Exit'):
            break
except Exception as e:
    print(e)
    window.close()

