import os
import shutil

path = input('작업자 폴더경로를 입력해주세요. ')
for (path, dir, files) in os.walk(path):
    for item in files:
        if os.path.isfile('D:/NIA(2022)/SunkenDebris/Previous/Training/[Training 라벨링]underwater photo/' + item.split('.')[0] + '.xml'):
            # print(item)
            shutil.copy('D:/NIA(2022)/SunkenDebris/Previous/Training/[Training 라벨링]underwater photo/' + item.split('.')[0] + '.xml', path +'/' + item.split('.')[0] + '.xml')
