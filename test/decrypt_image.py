import random
import time
import cv2

from util import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle

image_file_name = '../img/test_middle.png'
encrypted_image_file_name = '../results/encrypted_image.png'
decrypted_image_file_name = "../results/decrypted_image.png"

en_img = cv2.imread(encrypted_image_file_name)

height = int(len(en_img))
width = int(len(en_img[0]))

random.seed(123)

# Creating sBoxes
shuffle = KnuthShuffle()
sBox = shuffle.create_sBox(random)
inverse_sBox = shuffle.create_inverse_sBox()

# Decrypting image
image_encryption = ImageEncryption()
random_numbers = Util.generate_random_number(random, height, width)

start = time.perf_counter()
decrypted_image = image_encryption.decrypt(sBox, inverse_sBox, random_numbers, en_img)
finish = time.perf_counter()

print('Finished in {} second(s)'.format(finish - start))

cv2.imwrite(decrypted_image_file_name, decrypted_image)

Util.calculate_ssim(image_file_name, decrypted_image_file_name)
