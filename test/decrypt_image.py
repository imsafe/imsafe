import random
import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle

encrypted_image_file_name = "results/encrypted_image.png"
decrypted_image_file_name = "results/decrypted_image.png"

password = input("Enter password: ")
random.seed(password)

# Creating sBoxes
shuffle = KnuthShuffle()
sBox = shuffle.create_sBox(random)
inverse_sBox = shuffle.create_inverse_sBox()

# Decrypting image
image_encryption = ImageEncryption()
random_numbers = Util.generate_random_number(encrypted_image_file_name, random)
dec_image = image_encryption.decrypt(sBox, inverse_sBox, random_numbers, encrypted_image_file_name)
dec_image.save(decrypted_image_file_name)
dec_image.show()

# Util.calculate_ssim(image_file_name, decrypted_image_file_name)
