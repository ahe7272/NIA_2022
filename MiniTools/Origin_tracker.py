import os
import shutil

jsonpath = input('작업자 폴더경로를 입력해주세요. ')
originpath = input('Training_underwater photo_Original 경로를 입력해주세요. ')
move_from_path = input('Training_underwater photo 경로를 입력해주세요. ')
for (path, dir, files) in os.walk(jsonpath):
    for item in files:
        if os.path.isfile(originpath + '/' + item):

            shutil.move(move_from_path + '/Original_' + item, path)
