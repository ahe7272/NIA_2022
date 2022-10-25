import PySimpleGUI as sg
import pyperclip
from glob import glob
import os
from integrity_check import check
import subprocess
import sys
import json
import numpy as np
import requests
from io import BytesIO
import pickle
from PIL.ExifTags import TAGS
from PIL import Image
from glob import glob
import piexif
import getpass

# 전체 공유 주소: https://ifh.cc/v-8x5yaf.oCrngF.yR4Rzq.TvAS0x.F4Bj7d.65Gdtp.Z6gSOf.PW0b0s.9tHWQf

Fish_net = BytesIO(requests.get('https://ifh.cc/g/20hWHP.png').content).read()
Fish_trap = BytesIO(requests.get('https://ifh.cc/g/zCfW0G.png').content).read()
Glass = BytesIO(requests.get('https://ifh.cc/g/StQFZf.png').content).read()
Metal = BytesIO(requests.get('https://ifh.cc/g/xbZ14P.png').content).read()
Plastic = BytesIO(requests.get('https://ifh.cc/g/aNmDb2.png').content).read()
Wood = BytesIO(requests.get('https://ifh.cc/g/hM0P3O.png').content).read()
Rope = BytesIO(requests.get('https://ifh.cc/g/wX73Lo.png').content).read()
Rubber_etc = BytesIO(requests.get('https://ifh.cc/g/Yndasq.png').content).read()
Rubber_tire = BytesIO(requests.get('https://ifh.cc/g/Jsm9Zs.png').content).read()
Etc = BytesIO(requests.get('https://ifh.cc/g/3rLS6h.png').content).read()


class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')
        Step1 = [
                  [sg.Text('ANNOTATION', font =("Arial", 30, 'bold'), text_color = 'Skyblue')],
                  [sg.Text(' PATH', font =("Arial", 15)), sg.InputText(key='Path', font =("Arial", 15), size = (22,1)), sg.FolderBrowse('SELECT',font =("Arial", 15, 'bold') , size=(12, 1), key='Select_Folder')],
                  [sg.Text('  ID  ', font =("Arial", 15)), sg.InputText(key='userID', font =("Arial", 15), size = (23,1)), sg.Button('Labelme', font =("Arial", 15, 'bold'), size=(12, 1))],
                  [sg.Text(' Fish_net ', font =("Arial", 15, 'bold')), sg.Text('  Fish_trap  ', font =("Arial",  15, 'bold')), sg.Text('   Glass   ',font =("Arial",  15, 'bold')), sg.Text('   Metal   ', font =("Arial",  15, 'bold')), sg.Text('    Plastic    ', font =("Arial",  15, 'bold'))], 
                  [
                    sg.Button('', image_data=Fish_net, key='Fish_net'),
                    sg.Button('', image_data=Fish_trap, key='Fish_trap'),
                    sg.Button('', image_data=Glass, key='Glass'),
                    sg.Button('', image_data=Metal, key='Metal'),
                    sg.Button('', image_data=Plastic, key='Plastic')
                  ],
                  [sg.Text('   Wood   ', font =("Arial",  15, 'bold')), sg.Text('     Rope    ', font =("Arial",  15, 'bold')), sg.Text(' Rubber_etc', font =("Arial",  13, 'bold')), sg.Text(' Rubber_tire ', font =("Arial",  13, 'bold')), sg.Text('     Etc', font =("Arial",  15, 'bold'))],
                  [
                    
                    sg.Button('', image_data=Wood, key='Wood'),
                    sg.Button('', image_data=Rope, key='Rope'),
                    sg.Button('', image_data=Rubber_etc, key='Rubber_etc'),
                    sg.Button('', image_data=Rubber_tire, key='Rubber_tire'),
                    sg.Button('', image_data=Etc, key='Etc')
                  ]
                ]
        Step2 = [
                  [sg.Text('INTEGRITY CHECK', font =("Arial", 30, 'bold'), text_color = 'Skyblue')],
                  [sg.Text('에러 메세지를 확인하여 해당 파일을 수정해 주세요.', font =("Arial", 15, 'bold'))],
                  [sg.Text(' - Annotation 이름 에러: Labelme 재실행 및 annotation 이름 수정', font =("Arial", 13))],
                  [sg.Text(' - 속성 개수 에러: json 파일 확인 및 담당 PM과 소통', font =("Arial", 13))],
                  [sg.Text(' - ID 에러: STEP1에 ID 입력 후 다시 Metadata 입력', font =("Arial", 13))],
                  [sg.Button('무결성 검사', font=("Arial", 15, 'bold'), size=(45, 4), key='integrity')], 
                  [sg.Text('', font =("Arial", 5))],
                  [sg.Button('Exit', font=("Arial", 15, 'bold'),size=(45, 4))]
                ]
        tab_group = [
                     [sg.TabGroup(
                            [[
                            sg.Tab('STEP1', Step1),
                            sg.Tab('STEP2', Step2)
                            ]], 
                            tab_location='centertop',
                            font = ("Arial", 20),
                            tab_border_width = 2,               
                            selected_background_color='White',
                            selected_title_color='Black',
                            border_width=10)]        
                    ]
        window = sg.Window('Process_09.27', tab_group, resizable=True, grab_anywhere = True, element_justification='c') 
        return window
        
def changeexif(imagefile, ID):
    image = Image.open(imagefile)
    exifData = image._getexif()
    
    if exifData is None:
        exifData = {}

    data = pickle.dumps(ID)
    exif_ifd = {piexif.ExifIFD.UserComment: data}
    zeroth_ifd = {piexif.ImageIFD.Artist: ID.encode('ascii')}
    exif_dict = {"0th" : zeroth_ifd, "Exif": exif_ifd}

    exif_dat = piexif.dump(exif_dict)
    image.save(imagefile, exif=exif_dat)

def runLabelme(): 
    conda_dirs = ["c:/Users/users/anaconda3", "d:/Users/users/anaconda3", "c:/Users/User/Anaconda3", "c:/Users/Park/Anaconda3",
                  "c:/Users/Admin/anaconda3", "d:/Users/Admin/anaconda3", "c:/Users/admin/anaconda3", "d:/Users/admin/anaconda3", 
                  "c:/Users/Administrator/anaconda3", "d:/Users/Administrator/anaconda3",
                  "c:/Programdata/anaconda3", "d:/Programdata/anaconda3", 
                  "c:/Users/{}/Anaconda3".format(getpass.getuser()), "d:/Users/{}/Anaconda3".format(getpass.getuser()), 
                  "c:/사용자/{}/Anaconda3".format(getpass.getuser()), "d:/사용자/{}/Anaconda3".format(getpass.getuser()),
                  "c:/anaconda3", "c:/Anaconda3", "d:/anaconda3", "d:/Anaconda3"]

    try:
        for Dir in conda_dirs:
            if os.path.isdir(Dir):
                python_file = Dir + "/envs/nia/pythonw.exe"
                labelme_file =  python_file[:-11] + "Lib/site-packages/labelme/__main__.py"

            if Dir == "no dir":
                sg.Popup("anaconda 경로를 찾지 못했습니다. (conda_dirs내 해당 경로 없음)", font =("Arial", 15), keep_on_top=True)
        
        if np.__version__[:3] == '1.2':
            subprocess.Popen(python_file + ' ' + labelme_file,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    except:
        sg.Popup("anaconda 경로를 찾지 못했습니다. (runLabelme 도중 에러)", font =("Arial", 15), keep_on_top=True)


try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

m = MakeGUI()
window = m.makegui()

object = ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope','Rubber_etc',  'Rubber_tire', 'Etc']
minsize = 1024

try:
    while True:    
        event, values = window.read()    
        Path = values['Path']
        userID = values['userID']
        if event in object:
            pyperclip.copy(event)

        if event == 'Labelme':
            imagelist = glob(values['Path'] + '/*.jpg')
            for image in imagelist:
                jpgfile = os.path.split(image)[-1]
                imagename = os.path.splitext(jpgfile)[0]
                jsonfile = Path + '/' + imagename + '.json'
                imagefile = Path + '/' + imagename + '.jpg'
                changeexif(image, userID)

            runLabelme()

            jsonlist = glob(values['Path'] + '/*.json')
            for each_json in jsonlist:
                with open(each_json) as jsontosave:
                    objects = json.load(jsontosave)
                    objects['ID'] = userID
                with open(each_json, 'w') as jsontosave:
                    json.dump(objects, jsontosave, indent=4)

        if event == 'integrity':
            jsonlist = glob(values['Path'] + '/*.json')
            jsonerrors = ""
            if values['userID'] == "":
                jsonerrors += 'ID 에러!\nID를 정확하게 입력하고 Metadata 입력을 다시 진행해 주세요.\n'
            for Json in jsonlist:
                jsonfile = os.path.split(Json)[-1]
                jsonerrors += check(jsonfile, minsize, Path)
            if len(jsonerrors) > 0:
                sg.Popup(jsonerrors, font =("Arial", 15), keep_on_top=True)
            else:
                sg.Popup("작업완료된 파일이 오늘 날짜 폴더에 저장되었습니다. \n 작업 폴더에 남은 파일이 없는지 확인해주세요.", font =("Arial", 15), keep_on_top=True)
        if event == sg.WIN_CLOSED or event in (None, 'Exit'):
            break
        if event in (None, 'Exit'):
            break

except Exception as e:
   print(e)
window.close()


