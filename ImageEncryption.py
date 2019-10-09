import random
import numpy as np
from PIL import Image

def convertDecToHex(decimalNumber):
    if decimalNumber <= 15:
        return "0" + np.base_repr(decimalNumber, 16)
    else:
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

im = Image.open('watch.png')
rgb_im = im.convert('RGB')
pixels = im.load()
print(im.size)

for i in range(im.size[0]):
    for j in range(im.size[1]):
        r, g, b = rgb_im.getpixel((i, j))

        hexR = convertDecToHex(r)
        hexG = convertDecToHex(g)
        hexB = convertDecToHex(b)

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

im.save("watchEncrypted.png")
im.show()