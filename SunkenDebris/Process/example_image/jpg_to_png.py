from PIL import Image
import glob
size = (150, 150)
def get_resize_image(image, name):
    image = Image.open(image)
    image = image.resize(size)
    image.save(name)

# array = ['Fish net', 'Fish trap', 'Glass', 'Metal', 'Plastic', 'Processed wood', 'Rope','Rubber_etc',  'Rubber_tire']
# for a in array:
#     name =  a + '.png'
#     image = a + '.jpg'
#     get_resize_image(image, name)

for img in glob.glob('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Fish net.png'):
    get_resize_image(img, img)
