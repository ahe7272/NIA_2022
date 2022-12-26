import json
import os 
import shutil
import os 
import shutil

search_path = input('존재 여부 확인 폴더: ')
match_path = input('검색 폴더: ')

# item_list = []
# for (path, dir, files) in os.walk(search_path): 
#     for file in files:
#         item_list += [path + '/' + file]

# for (path, dir, files) in os.walk(match_path): 
#     if len(path.split('_used')) > 1 :
#         continue
#     for item in files:
#         if item[-5:] == '.json':
#             if item in item_list:
#                 os.makedirs(path +'_used', exist_ok=True)
#                 shutil.move(path + '/' + item, path +'_used/' + item)  
#                 shutil.move(path + '/' + item[:-4] + 'jpg', path + '_used/' + item[:-4] + 'jpg') 
                


item_list = []
for (path, dir, files) in os.walk(match_path):
    print(path)
    item_list += files
for (path, dir, files) in os.walk(search_path): 
    if len(path.split('_used')) > 1 :
        continue
    for item in files:
        if item[-5:] == '.json':
            if item in item_list:
                os.makedirs(path +'_used', exist_ok=True)
                shutil.move(path + '/' + item, path +'_used/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '_used/' + item[:-4] + 'jpg') 
                