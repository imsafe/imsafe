import random

import cv2

from util import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle

encrypted_image_file_name = "../results/son.png"
decrypted_image_file_name = "../results/dec_son.png"

en_img = cv2.imread(encrypted_image_file_name)
height = int(len(en_img))
width = int(len(en_img[0]))
# password = input("Enter password: ")
random.seed(123)

# Creating sBoxes
shuffle = KnuthShuffle()
sBox = shuffle.create_sBox(random)
inverse_sBox = shuffle.create_inverse_sBox()

# Decrypting image
image_encryption = ImageEncryption()
random_numbers = Util.generate_random_number(random, height, width)

dec_image = image_encryption.decrypt(sBox, inverse_sBox, random_numbers, en_img)
cv2.imwrite(decrypted_image_file_name, dec_image)
# dec_image.save(decrypted_image_file_name)
# dec_image.show()

# Util.calculate_ssim(encrypted_image_file_name, decrypted_image_file_name)
