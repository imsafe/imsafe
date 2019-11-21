import random
import Utility as Util
from ImageEncryption import ImageEncryption
from KnuthShuffle import KnuthShuffle

if __name__ == '__main__':
    image_file_name = "img/test.png"
    encrypted_image_file_name = "img/encrypted_image.png"
    decrypted_image_file_name = "img/decrypted_image.png"

    random.seed(123)

    shuffle = KnuthShuffle()
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    # random_state = random.getstate()

    image_encryption = ImageEncryption()

    random_numbers = Util.generate_random_number(image_file_name, random)

    en_image = image_encryption.encrypt(sBox, random_numbers, image_file_name)
    en_image.show()
    en_image.save(encrypted_image_file_name)

    # random.setstate(random_state)

    dec_image = image_encryption.decrypt(sBox, inverse_sBox, random_numbers, encrypted_image_file_name)
    dec_image.save(decrypted_image_file_name)
    dec_image.show()

    Util.calculate_ssim(image_file_name, decrypted_image_file_name)
