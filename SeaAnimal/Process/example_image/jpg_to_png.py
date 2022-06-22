import os
from PIL import Image, ImageTk
size = (150, 150)
def get_resize_image(image, name):
    image = Image.open(image)
    image = image.resize(size)
    image.save(name)

array = ['Asterias Amurensis', 'Asterina Pectinifera', 'Conch', 'EckloniaCava', 'Heliocidaris Crassispina','Hemicentrotus','Sargassum',  'SeaHare', 'Turbo Cornutus']
for a in array:
    name = a + '.png'
    image = a + '.jpg'
    get_resize_image(image, name)
