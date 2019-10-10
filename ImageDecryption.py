import random
import numpy as np
from PIL import Image


def convertDecToHex(decimalNumber):
    if decimalNumber <= 15:
        return "0" + np.base_repr(decimalNumber, 16)
    return np.base_repr(decimalNumber, 16)

seed = input("Enter a seed value:")
random.seed(seed)

x = np.arange(256)

for i in range(255, -1, -1):
    j = random.randint(0, 255)
    temp = x[i]
    x[i] = x[j]
    x[j] = temp

x = np.reshape(x, (16, 16))

sBox = np.empty((16, 16), dtype='object')

for i in range(0, 16):
    for j in range(0, 16):
        sBox[i][j] = convertDecToHex(x[i][j])

inverseSBox = np.empty((16, 16), dtype='object')

for i in range(0, 16):
    for j in range(0, 16):
        value = sBox[i, j]
        row = int(value[0], 16)
        column = int(value[1], 16)
        inverseSBox[row, column] = np.base_repr(i, 16) + np.base_repr(j, 16)

im = Image.open('watchEncrypted.png')
rgb_im = im.convert('RGB')
pixels = im.load()
print(im.size)

for i in range(im.size[0]):
    for j in range(im.size[1]):
        r, g, b = rgb_im.getpixel((i, j))

        hexR = convertDecToHex(r)
        hexG = convertDecToHex(g)
        hexB = convertDecToHex(b)

        newR = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexR, 16)
        newG = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexG, 16)
        newB = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexB, 16)

        newR = convertDecToHex(newR)
        newG = convertDecToHex(newG)
        newB = convertDecToHex(newB)

        pixels[i, j] = int(inverseSBox[int(newR[0], 16), int(newR[1], 16)], 16), int(
            inverseSBox[int(newG[0], 16), int(newG[1], 16)], 16), int(inverseSBox[int(newB[0], 16), int(newB[1], 16)],
                                                                      16)

im.save("watchDecrypted.png")
im.show()
