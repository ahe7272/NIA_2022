import json
import os 


running_path = 'C:\Dataset\ori\Test'
b_or_p = 'Polygon'
new_or_old = '2020'


def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

# Originals 폴더 내 사진 명 일괄 통일 작업
# for (root, dir, files) in os.walk(running_path): 
#     if root.split('\\')[-1].split(' ')[-1] == 'Originals':
#         for item in files:
#             for piece in item.split('_'):

#                 if piece[:2] == 'GX':
#                     new_name = piece + '_' + item.split('_')[-1]
#                     break
#             old = root + '/' + item
#             new = root + '/' + new_name
#             os.rename(old, new)

# cnt = 1
# for (path, dir, files) in os.walk(running_path): 
#     if path.split('\\')[-1] == 'Originals':
#         continue

#     for item in files:
#         if item[-5:] == '.json':
#             name = b_or_p + '_' + new_or_old + '_' + str(cnt).zfill(5)
#             old_jpg = path + '/' + item[:-5] + '.jpg'
#             new_jpg = path + '/' + name + '.jpg'
#             old_json = path + '/' + item
#             new_json = path + '/' + name + '.json'
#             # for piece in item.split('_'):
#             #     if piece[:2] == 'GX':
#             #         new_name = piece + '_' + item.split('_')[-1]
#             #         break
#             new_name = '_'.join(item.split('_')[2:])
#             old_original = path + ' Originals/Original_' + new_name[:-5] + '.jpg'
#             new_original = path + ' Originals/' + name + '_original.jpg'
#             os.rename(old_jpg, new_jpg)
#             os.rename(old_json, new_json)
#             os.rename(old_original, new_original)
#             cnt += 1
#             objects = getjson(new_json)
#             objects['imagePath'] = name + '.jpg'
#             with open(new_json, 'w') as j:
#                 json.dump(objects, j, indent='\t')
#                 j.close()


# Originals 폴더 내 사진 명 일괄 통일 작업
for (root, dir, files) in os.walk('C:/Users/Administrator/Desktop/tofix'): 
    for item in files:
        new_name = '_'.join(item.split('_')[1:])
        print(new_name)
        old = root + '/' + item
        new = root + '/' + new_name
        try:
            os.rename(old, new)
        except:
            continue