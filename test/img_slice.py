import time

import cv2
import numpy as np
import random
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle
import Utility as Util

img = cv2.imread('../img/slice_test.png')
height = int(len(img))
width = int(len(img[0]))

x = int(height/2)
y = int(width/2)


top_left = img[:x, :y]
top_right = img[:y, x:width]
bottom_left = img[x:height, :y]
bottom_right = img[x:height, y:width]

# top = np.concatenate((top_left, top_right), 1)
# bottom = np.concatenate((bottom_left, bottom_right), 1)
# son = np.concatenate((top, bottom), 0)
# cv2.imwrite('../results/son.png', son)
#
# cv2.imwrite('../results/top_left.png', top_left)
# cv2.imwrite('../results/top_right.png', top_right)
# cv2.imwrite('../results/bottom_left.png', bottom_left)
# cv2.imwrite('../results/bottom_right.png', bottom_right)

shuffle = KnuthShuffle()
image_encryption = ImageEncryption()


random.seed(123)
shuffle = KnuthShuffle()
sBox = shuffle.create_sBox(random)
inverse_sBox = shuffle.create_inverse_sBox()

random_numbers = Util.generate_random_number('../img/slice_test.png', random)

rand_top_left = random_numbers[:x, :y]
rand_top_right = random_numbers[:y, x:width]
rand_bottom_left = random_numbers[x:height, :y]
rand_bottom_right = random_numbers[x:height, y:width]

en_image_top_left = image_encryption.encrypt(sBox, rand_top_left, top_left)
en_image_top_right = image_encryption.encrypt(sBox, rand_top_right, top_right)
en_image_bottom_left = image_encryption.encrypt(sBox, rand_bottom_left, bottom_left)
en_image_bottom_right = image_encryption.encrypt(sBox, rand_bottom_right, bottom_right)

cv2.imwrite('../results/en_top_left.png', en_image_top_left)
cv2.imwrite('../results/en_top_right.png', en_image_top_right)
cv2.imwrite('../results/en_bottom_left.png', en_image_bottom_left)
cv2.imwrite('../results/en_bottom_right.png', en_image_bottom_right)


top = np.concatenate((en_image_top_left, en_image_top_right), 1)
bottom = np.concatenate((en_image_bottom_left, en_image_bottom_right), 1)
son = np.concatenate((top, bottom), 0)
cv2.imwrite('../results/son.png', son)

cv2.imwrite('../results/top_left.png', top_left)
cv2.imwrite('../results/top_right.png', top_right)
cv2.imwrite('../results/bottom_left.png', bottom_left)
cv2.imwrite('../results/bottom_right.png', bottom_right)




