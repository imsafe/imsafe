from PIL import Image
import numpy as np


class ImageEncryption:

    def convertDecToHex(self, decimalNumber):
        if decimalNumber <= 15:
            return "0" + np.base_repr(decimalNumber, 16)
        else:
            return np.base_repr(decimalNumber, 16)

    def encrypt(self, sBox, random, image):
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        pixels = im.load()
        # print(im.size)

        for i in range(im.size[0]):
            for j in range(im.size[1]):
                r, g, b = rgb_im.getpixel((i, j))

                hexR = self.convertDecToHex(r)
                hexG = self.convertDecToHex(g)
                hexB = self.convertDecToHex(b)

                rowR = int(hexR[0], 16)
                columnR = int(hexR[1], 16)

                rowG = int(hexG[0], 16)
                columnG = int(hexG[1], 16)

                rowB = int(hexB[0], 16)
                columnB = int(hexB[1], 16)

                newR = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(sBox[rowR, columnR], 16)
                newG = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(sBox[rowG, columnG], 16)
                newB = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(sBox[rowB, columnB], 16)

                pixels[i, j] = newR, newG, newB

        im.save("encrypted_image.png")
        im.show()

        return im

    def decrypt(self, sBox, inverseSBox, random, image):
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        pixels = im.load()
        print(im.size)

        for i in range(im.size[0]):
            for j in range(im.size[1]):
                r, g, b = rgb_im.getpixel((i, j))

                hexR = self.convertDecToHex(r)
                hexG = self.convertDecToHex(g)
                hexB = self.convertDecToHex(b)

                newR = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexR, 16)
                newG = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexG, 16)
                newB = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexB, 16)

                newR = self.convertDecToHex(newR)
                newG = self.convertDecToHex(newG)
                newB = self.convertDecToHex(newB)

                pixels[i, j] = int(inverseSBox[int(newR[0], 16), int(newR[1], 16)], 16), int(
                    inverseSBox[int(newG[0], 16), int(newG[1], 16)], 16), int(
                    inverseSBox[int(newB[0], 16), int(newB[1], 16)],
                    16)

        im.save("decrypted_image.png")
        im.show()

        return  im

