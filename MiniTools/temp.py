import json
import datetime
import os 
import cv2

path_input = input('경로: ')
def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk(path_input): 
    for item in files:
        # img = cv2.imread(path + '/' + item)
        # if img.shape[0] not in [1080, 720]:
        #     print(item, img.shape)
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            # try:
            #     objects.pop('Origin_img')
            # except:
            #     continue
            # lat = objects['Longitude']
            # lon = objects['Latitude'] 
            # if objects['imageHeight'] not in [1080, 720]:
            #     print(objects['imageHeight'], objects['imageWidth'])
            if objects['Source_video'] in ['20220927_ROV02_GX010706.mp4', '20220927_ROV02_GX020706.mp4', '20220927_ROV02_GX030706.mp4', '20220927_ROV02_GX040706.mp4', '20220927_ROV02_GX050706.mp4','20220927_ROV02_GX060706.mp4']:
            # if objects['Source_video'] in ['20220927_ROV01_GX010650.mp4', '20220927_ROV01_GX020650.mp4', '20220927_ROV01_GX030650.mp4', '20220927_ROV01_GX040650.mp4', '20220927_ROV01_GX050650.mp4', '20220927_ROV01_GX060650.mp4']:

                objects['Latitude'] = round((37 + (18/60) + (27.46/3600) + 37 + (18/60) + (27.36/3600))/2,6)
                objects['Longitude'] = round((129 + (18/60) + (1.21/3600) + 129 + (18/60) + (1.54/3600))/2, 6)
            # objects['CDist'] = None
            # objects['Site_Type'] = None   
            # objects['ID'] = 'CW304'
            # objects['imageData'] = None
            # objects['Source_video'] = None
            # objects['Video_time'] = None
            # objects['Frame_no'] = None
            # # Source_video 입력 후 돌리는 수집 방법 구문 
            # if len(objects['Source_video'].split('ROV')) > 1:
            #     objects['Collection_method'] = 'ROV'
            # else:
            #     objects['Collection_method'] = 'Diver'
            # try:
            #     objects.pop('ID')
            #     with open(path + '/' + item, 'w') as j:
            #         json.dump(objects, j, indent='\t')
            #         j.close()
            # except:
            #     pass
            # if len(objects) != 23:
            #     print(item)
            # objects['Distance'] = 0.5
            # objects['Latitude'] = round(float(objects['Latitude']),6)
            # objects['Longitude'] = round(float(objects['Longitude']),6)
            # for label in objects['shapes']:
            #     if (max(label['points'][0] + label['points'][1])) > 3840:
            #         print(item, label)
            # for label in objects['shapes']:
            #     label['Size'] = 0
            #     label['Weight'] = 0
                with open(path + '/' + item, 'w') as j:
                    json.dump(objects, j, indent='\t')
                    j.close()