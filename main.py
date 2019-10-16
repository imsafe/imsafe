from KnuthShuffle import KnuthShuffle
from ImageEncryption import ImageEncryption
import random
import Utility as Util

if __name__ == '__main__':

    random.seed("sdkfjgl_12@")

    shuffle = KnuthShuffle()
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    random_state = random.getstate()

    image_encryption = ImageEncryption()
    en_image = image_encryption.encrypt(sBox, random, "cat.png")
    en_image.show()
    en_image.save("encrypted_image.png")

    random.setstate(random_state)

    dec_image = image_encryption.decrypt(sBox, inverse_sBox, random, "encrypted_image.png")
    dec_image.show()
    dec_image.save('decrypted_image.png')
    Util.imageHistogram('cat.png')
    Util.imageHistogram('encrypted_image.png')
    Util.imageHistogram('decrypted_image.png')
