import time

import cv2
import numpy as np

from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle

image_file_name = '../img/test_middle.png'
encrypted_image_file_name = '../results/encrypted_image.png'

img = cv2.imread(image_file_name)

height = int(len(img))
width = int(len(img[0]))

np.random.seed(123)

shuffle = KnuthShuffle()
sBox = shuffle.create_s_box(np.random)
inverse_sBox = shuffle.create_inverse_s_box()

random_numbers = np.random.randint(0, 16, (height, width, 6))

image_encryption = ImageEncryption()

start = time.perf_counter()
encrypted_image = image_encryption.encrypt(sBox, random_numbers, img)
finish = time.perf_counter()

print('Finished in {} second(s)'.format(finish - start))

cv2.imwrite(encrypted_image_file_name, encrypted_image)
