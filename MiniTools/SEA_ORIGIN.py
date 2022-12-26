import json
import os 
import shutil

original_path = 'D:/12th/Originals'
match_path = 'D:/12th/Bbox'
save_path = 'D:/12th/Bbox Originals'
no_video = []

for (path, dir, files) in os.walk(match_path): 
    if path.split('\\')[-1] == 'Originals':
        continue
    for item in files:
        if item[-4:] == '.jpg':
           
            if os.path.isfile(original_path + '/' + '_'.join(item.split('_')[2:])):
                shutil.move(original_path + '/' + '_'.join(item.split('_')[2:]), save_path + '/' + '_'.join(item.split('_')[2:]))                
            else:
                if '_'.join(item.split('_')[2:5]) not in no_video:
                    no_video += ['_'.join(item.split('_')[2:-1])]

print(no_video)