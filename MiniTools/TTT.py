import json
import os 
import shutil

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects


for (path, dir, files) in os.walk('D:/11_2_to_fix'): 
    for item in files:
        if item[-5:] == '.json':
            for (dist_path, dist_dir, dist_files) in os.walk('D:/22차 정제완료(근중원용)'): 
                if os.path.isfile(dist_path + '/' + item):
                    print(dist_path + '/' + item)
                    objects = getjson(path + '/' + item)
                    if dist_path.split('\\')[-1] == 'Far':
                        objects['Distance'] = 1.5
                    elif dist_path.split('\\')[-1] == 'Mid':
                        objects['Distance'] = 1.0
                    elif dist_path.split('\\')[-1] == 'Near':
                        objects['Distance'] = 0.5
                    with open(path + '/' + item, 'w') as j:
                        json.dump(objects, j, indent='\t')
                        j.close()
                    break

# for (path, dir, files) in os.walk('D:/11_2_sea'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             if objects['Distance'] == 0:
#                 # print(item)
#                 os.makedirs('D:/11_2_to_fix/' +path.split('\\')[-1], exist_ok=True) 
#                 shutil.move(path + '/'+ item, 'D:/11_2_to_fix/' +path.split('\\')[-1] +'/' + item)
#                 shutil.move(path + '/'+ item[:-5] + '.jpg', 'D:/11_2_to_fix/' +path.split('\\')[-1] +'/' + item[:-5] + '.jpg')