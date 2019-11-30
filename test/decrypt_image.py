import random
import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle
import cv2

encrypted_image_file_name = "../results/son.png"
decrypted_image_file_name = "../results/decrypted_son.png"

# password = input("Enter password: ")
random.seed(123)

# Creating sBoxes
shuffle = KnuthShuffle()
sBox = shuffle.create_sBox(random)
inverse_sBox = shuffle.create_inverse_sBox()

# Decrypting image
image_encryption = ImageEncryption()
random_numbers = Util.generate_random_number(encrypted_image_file_name, random)

en_img = cv2.imread('../results/son.png')
dec_image = image_encryption.decrypt(sBox, inverse_sBox, random_numbers, en_img)
cv2.imwrite('../results/dec_son.png', dec_image)
# dec_image.save(decrypted_image_file_name)
# dec_image.show()

# Util.calculate_ssim(image_file_name, decrypted_image_file_name)
