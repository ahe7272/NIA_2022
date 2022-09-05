import os 
import shutil

dup_path = 'C:/Users/Administrator/Desktop/NEW_7.3_sunken/Polygon2/Duplicated/'
filename_list = []
for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/NEW_7.3_sunken/Polygon2'):
    for file in files:
        if file[-4:] == '.jpg':
            if file in filename_list:
                shutil.move(path + '/' + file, dup_path + file)
                shutil.move(path + '/' + file[:-4] + '.json', dup_path + file[:-4] + '.json')
            else:
                filename_list += [file]
            
# Original finder
# ori_path = 'C:/Users/Administrator/Desktop/NEW_7.3_sunken/Polygon/Originals/'
# filename_list = []
# for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/NEW_7.3_sunken/Polygon'):
#     for file in files:
#         if file[-4:] == '.jpg':
#             if file[:8] == 'Original':
#                 shutil.move(path + '/' + file, ori_path + file)

            