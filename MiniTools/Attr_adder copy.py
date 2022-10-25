import json
import datetime
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

video_list_path = 'D:/Original/김정훈/Geoje/2-4'
video_list = []
for (path, dir, files) in os.walk(video_list_path): 
    video_list += ['.'.join([Mp4.split('.')[0], 'mp4']) for Mp4 in files if Mp4.lower().endswith('.mp4')]

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/ROV_latlon'): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            if objects['Source_video'] in video_list:
                # objects['Temperature'] = 21.4
                # objects['Salinity'] = 33.21
                # objects['DO'] = 6.81
                # objects['pH'] = 8.51
                objects['Latitude'] = 34.820106
                objects['Longitude'] = 128.752092
                # objects['Depth'] = 10
                # objects['Weather'] = 1
                # objects['Transparency'] = 4.8
                objects['Date_created'] = "2022-06-22"
                with open(path + '/' + item, 'w') as j:
                    json.dump(objects, j, indent='\t')
                    j.close()

