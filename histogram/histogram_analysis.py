from PIL import Image
from util import Utility as Util

im = Image.open('encrypted_image.png')
Util.image_histogram('decrypted_image.png')

r,g,b = im.split()

r.save('img/red.png')
g.save('img/green.png')
b.save('img/blue.png')

Util.image_histogram('img/red.png')
Util.image_histogram('img/green.png')
Util.image_histogram('img/blue.png')
