import PySimpleGUI as sg
import os
import json
import shutil
import random
from classes import debris_dict, sea_animal_dict


class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')

        layout = [
                  [sg.Text('데이터의 경로(폴더)',font =("Arial", 13, 'bold'), size=(40, 1))],
                  [sg.InputText('Data Folder', font =("Arial", 13), size = (30,1), key='DataPath'), sg.FolderBrowse('SELECT', font =("Arial", 13, 'bold'), size=(10, 1))],
                  [sg.InputText('Save Folder', font =("Arial", 13), size = (30,1), key='SavePath'), sg.FolderBrowse('SELECT', font =("Arial", 13, 'bold'), size=(10, 1))],
                  [sg.Text('Project : ', font =("Arial", 15)), sg.Checkbox('Sea', font =("Arial", 10, 'bold'), size=(8, 1), key='Sea'), sg.Checkbox('Sunken', font =("Arial", 10, 'bold'), size=(8, 1), key='Sunken'), sg.Button('RUN', font =("Arial", 10, 'bold'), size=(8, 1), key='Run')],
                  [sg.ProgressBar(1, orientation='h', size=(40,20), key='progress')]
                 ]

        window = sg.Window('Best_label_extracter', layout, element_justification='c', grab_anywhere = True).Finalize()
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

temp = []

while True:    
    event, values = window.read()     
    progress_bar = window['progress']
    if event == 'Run':
        file_length = 0
        if values['Sea']:
            class_dict = sea_animal_dict()
        elif values['Sunken']:
            class_dict = debris_dict()
        for (path, dir, files) in os.walk(values['DataPath']):
            file_length += len([Json for Json in files if Json.lower().endswith('.json')])
            progress_bar.UpdateBar(0, file_length)
        for (path, dir, files) in os.walk(values['DataPath']):
            for file in files:
                ind = random.randint(0, len(files)-1)
                example = files[ind]
                cnt = 1
                progress_bar.UpdateBar(cnt, file_length)
                if example[-5:] == '.json':
                    jsonfile = path + '/' + example
                    objects = handlejson(jsonfile=jsonfile, option='get')
                    if class_dict[objects['shapes'][0]['label']] < 6:
                        temp += [file]
                        class_dict[objects['shapes'][0]['label']] += 1
                        shutil.copy(path + '/' + example , values['SavePath'] + '/' + example) 
                        shutil.copy(path + '/' + example[:-5] + '.jpg' , values['SavePath'] + '/' + example[:-5] + '.jpg')  
                    else:
                        continue
        cnt = 1
        progress_bar.UpdateBar(cnt, file_length)

        if cnt == file_length +1 :
            sg.Popup('정제 완료^^!', font =("Arial", 13), keep_on_top=True)
            break
        
    if event in (None, 'Exit'):
        break

