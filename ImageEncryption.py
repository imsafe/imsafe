from PIL import Image
import Utility as Util



class ImageEncryption:

    def encrypt(self, sBox, random, image):
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        pixels = im.load()

        for i in range(im.size[0]):
            for j in range(im.size[1]):
                r, g, b = rgb_im.getpixel((i, j))

                hexR = Util.convertDecToHex(r)
                hexG = Util.convertDecToHex(g)
                hexB = Util.convertDecToHex(b)

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

        return im

    def decrypt(self, sBox, inverseSBox, random, image):
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        pixels = im.load()

        for i in range(im.size[0]):
            for j in range(im.size[1]):
                r, g, b = rgb_im.getpixel((i, j))

                hexR = Util.convertDecToHex(r)
                hexG = Util.convertDecToHex(g)
                hexB = Util.convertDecToHex(b)

                newR = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexR, 16)
                newG = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexG, 16)
                newB = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexB, 16)

                newR = Util.convertDecToHex(newR)
                newG = Util.convertDecToHex(newG)
                newB = Util.convertDecToHex(newB)

                pixels[i, j] = int(inverseSBox[int(newR[0], 16), int(newR[1], 16)], 16), int(
                    inverseSBox[int(newG[0], 16), int(newG[1], 16)], 16), int(
                    inverseSBox[int(newB[0], 16), int(newB[1], 16)],
                    16)

        return im
