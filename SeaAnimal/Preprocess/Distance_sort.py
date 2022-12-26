import PySimpleGUI as sg
from glob import glob
import os
import subprocess
import sys
import openpyxl
from datetime import date
import pandas as pd 
import shutil
import json

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')
        integrity = [
                  [sg.Text('SORT DATA', font =("Arial", 30, 'bold'), text_color = 'Skyblue')],
                  [sg.Text('PATH', font =("Arial", 15)), sg.InputText(key='Path', font =("Arial", 15), size = (10,1)), sg.FolderBrowse('SELECT',font =("Arial", 15, 'bold') , size=(10, 1))],
                  [sg.Text('', font =("Arial", 10, 'bold'))],
                  [sg.Button('RUN', font =("Arial", 15, 'bold'), size=(25, 1))]
                    ]

        window = sg.Window('SORT DATA', integrity, resizable=True, grab_anywhere = True, element_justification='c') 
        return window

    
try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

m = MakeGUI()
window = m.makegui()

try:
    flag_cnt = 0
    while True:    
        event, values = window.read()    
        if event == 'RUN':
            Datapath = values['Path']
            for path, dirs, files in os.walk(Datapath):
                for item in files:
                    if item[-5:] == '.json':
                        objects = getjson(path + '/' + item)
                        os.makedirs(path +'/Near' , exist_ok=True)
                        os.makedirs(path +'/Mid' , exist_ok=True)
                        os.makedirs(path +'/Far' , exist_ok=True)
                        if objects['Distance'] == 0.5:
                            shutil.move(path + '/' + item, path +'/Near/' + item)  
                            shutil.move(path + '/' + item[:-4] + 'jpg', path +'/Near/' + item[:-4] + 'jpg') 
                            continue
                        elif objects['Distance'] == 1.0:
                            shutil.move(path + '/' + item, path +'/Mid/' + item)  
                            shutil.move(path + '/' + item[:-4] + 'jpg', path +'/Mid/' + item[:-4] + 'jpg') 
                            continue 
                        elif objects['Distance'] == 1.5:
                            shutil.move(path + '/' + item, path +'/Far/' + item)  
                            shutil.move(path + '/' + item[:-4] + 'jpg', path +'/Far/'+ item[:-4] + 'jpg') 


            sg.Popup("완료.", font =("Arial", 15), keep_on_top=True)   
                
        if event == sg.WIN_CLOSED or event in (None, 'Exit'):
            break
        if event in (None, 'Exit'):
            break

except Exception as e:
    print(e)
window.close()