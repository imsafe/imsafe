from KnuthShuffle import KnuthShuffle
from ImageEncryption import ImageEncryption
import random

if __name__ == '__main__':

    image_file_name = "cat.png"
    encrypted_image_file_name = "encrypted_image.png"
    decrypted_image_file_name = "decrypted_image.png"

    random.seed(123)

    shuffle = KnuthShuffle()
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    random_state = random.getstate()

    image_encryption = ImageEncryption()
    en_image = image_encryption.encrypt(sBox, random, image_file_name)
    en_image.show()
    en_image.save(encrypted_image_file_name)

    random.setstate(random_state)

    dec_image = image_encryption.decrypt(sBox, inverse_sBox, random, encrypted_image_file_name)
    dec_image.save(decrypted_image_file_name)
    dec_image.show()

    ImageEncryption.calculate_ssim(image_file_name, decrypted_image_file_name)
