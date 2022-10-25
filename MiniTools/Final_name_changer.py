import json
import os 
import pandas as pd

running_path = 'C:/Users/Administrator/Desktop/to'
b_or_p = 'Polygon'
new_or_old = '2022'


def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

# Originals 폴더 내 사진 명 일괄 통일 작업
# for (root, dir, files) in os.walk(running_path): 
#     if root.split('\\')[-1].split(' ')[-1] == 'Originals':
#         for item in files:
#             new_name = ''.join(item.split('Original_'))
#             old = root + '/' + item
#             new = root + '/' + new_name
#             os.rename(old, new)

change_log = {}
original = []
new = []
cnt = 7619
for (path, dir, files) in os.walk(running_path): 
    if path.split('\\')[-1] == 'Originals':
        continue
    for item in files:
        if item[-5:] == '.json':
            name = b_or_p + '_' + new_or_old + '_' + str(cnt).zfill(5)
            # name = b_or_p + '_' + str(cnt).zfill(6)
            old_jpg = path + '/' + item[:-5] + '.jpg'
            new_jpg = path + '/' + name + '.jpg'
            old_json = path + '/' + item
            new_json = path + '/' + name + '.json'
            if ''.join(old_jpg.split('_')[2:])[0] in ['0', '1']:
                old_original = path + '/Originals/' + ''.join(old_jpg.split('_')[2:])[:-4] + '.jpg'
            else:
                old_original = path + '/Originals/' + '_'.join(old_jpg.split('_')[2:])[:-4] + '.jpg'
            # old_original = path + '/Originals/' + item[:-5] + '.jpg'
            new_original = path + '/Originals/' + name + '.jpg'
            original += [old_jpg.split('/')[-1]]
            new += [new_jpg.split('/')[-1]]
            os.rename(old_original, new_original)
            os.rename(old_jpg, new_jpg)
            os.rename(old_json, new_json)
            cnt += 1
            objects = getjson(new_json)
            objects['imagePath'] = name + '.jpg'
            with open(new_json, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()

change_log['Old'] = original
change_log['New'] = new

df = pd.DataFrame(change_log)
df.set_index('Old', inplace = True)

df.to_csv(running_path + '/Name_change_log_ready_bbox.csv')