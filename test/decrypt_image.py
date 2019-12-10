import time

import cv2
import numpy as np

from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle
from util import Utility as Util

image_file_name = '../img/test_middle.png'
encrypted_image_file_name = '../results/encrypted_image.png'
decrypted_image_file_name = "../results/decrypted_image.png"

en_img = cv2.imread(encrypted_image_file_name)

height = int(len(en_img))
width = int(len(en_img[0]))

np.random.seed(123)

shuffle = KnuthShuffle()
s_box = shuffle.create_s_box(np.random)
inverse_s_box = shuffle.create_inverse_s_box()

random_numbers = np.random.randint(0, 16, (height, width, 6))

image_encryption = ImageEncryption()

start = time.perf_counter()
decrypted_image = image_encryption.decrypt(s_box, inverse_s_box, random_numbers, en_img)
finish = time.perf_counter()

print('Finished in {} second(s)'.format(finish - start))

cv2.imwrite(decrypted_image_file_name, decrypted_image)

Util.calculate_ssim(image_file_name, decrypted_image_file_name)
