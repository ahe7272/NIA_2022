from PIL import Image
import glob
size = (100, 100)
def get_resize_image(image, name):
    image = Image.open(image)
    image = image.resize(size)
    image.save(name)

array = ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope','Rubber_etc', 'Rubber_tire', 'ETC']
# for a in array:
#     name =  a + '.png'
#     image = a + '.jpg'
#     get_resize_image(image, name)


for a in array:
    name = a + '.png'
    get_resize_image(name, name)

