from KnuthShuffle import KnuthShuffle
from ImageEncryption import ImageEncryption
import random

if __name__ == '__main__':

    random.seed(123)

    shuffle = KnuthShuffle()
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    random_state = random.getstate()

    image_encryption = ImageEncryption()
    image_encryption.encrypt(sBox, random, "cat.png")

    random.setstate(random_state)

    image_encryption.decrypt(sBox, inverse_sBox, random, "encrypted_image.png")
