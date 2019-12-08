import random
from util import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle

image_file_name = input('Enter image path: ')
encrypted_image_file_name = "results/encrypted_image.png"

password = input("Enter password: ")
random.seed(password)

# Creating sBoxes
shuffle = KnuthShuffle()
sBox = shuffle.create_sBox(random)
inverse_sBox = shuffle.create_inverse_sBox()

# Encrypting image
image_encryption = ImageEncryption()
random_numbers = Util.generate_random_number(image_file_name, random)
en_image = image_encryption.encrypt(sBox, random_numbers, image_file_name)
en_image.show()
en_image.save(encrypted_image_file_name)
