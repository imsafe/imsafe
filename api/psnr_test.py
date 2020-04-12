from util import Utility as Util

img1_path = input('Path for image 1: ')
img2_path = input('Path for image 2: ')

print(Util.psnr(img1_path, img2_path))
