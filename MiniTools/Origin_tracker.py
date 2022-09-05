import glob
import os
import shutil

# for (path, dir, files) in os.walk('D:/NIA(2022)/SunkenDebris/Previous/Training/underwater photo'):
#     for item in files:
#         newname = 'Original_' + item
#         os.rename(path +'/' + item, path +'/' + newname)


jsonpath = input('작업자 폴더경로를 입력해주세요. ')
originpath = input('Training_underwater photo_Original 경로를 입력해주세요. ')
move_from_path = input('Training_underwater photo 경로를 입력해주세요. ')
for (path, dir, files) in os.walk(jsonpath):
    for item in files:
        if os.path.isfile(originpath + '/' + item):

            shutil.move(move_from_path + '/Original_' + item, path)
