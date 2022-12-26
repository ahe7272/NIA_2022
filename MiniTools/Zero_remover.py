import os 

running_path = input('경로: ')

for (path, dir, files) in os.walk(running_path): 
    for item in files:
        if item[-4:] == '.jpg':
            no = int(item.split('_')[-1].split('.')[0])
            print(no)
            new_name = path + '/' + '_'.join(item.split('_')[:-1]) + '_' + str(no) + '.jpg'
            os.rename(path + '/' + item, new_name)
