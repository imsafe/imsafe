import random
import numpy as np
from PIL import Image

seed = input("Seed değeri giriniz: ")
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
        if x[i][j] <= 15:
            sBox[i][j] = "0" + np.base_repr(x[i, j], 16)
        else:
            sBox[i][j] = np.base_repr(x[i, j], 16)

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

        if r <= 15:
            hexR = "0" + np.base_repr(r, 16)
        else:
            hexR = np.base_repr(r, 16)

        if g <= 15:
            hexG = "0" + np.base_repr(g, 16)
        else:
            hexG = np.base_repr(g, 16)

        if b <= 15:
            hexB = "0" + np.base_repr(b, 16)
        else:
            hexB = np.base_repr(b, 16)

        newR = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexR, 16)
        newG = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexG, 16)
        newB = int(sBox[random.randint(0, 15), random.randint(0, 15)], 16) ^ int(hexB, 16)

        if newR <= 15:
            newR = "0" + np.base_repr(newR, 16)
        else:
            newR = np.base_repr(newR, 16)

        if newG <= 15:
            newG = "0" + np.base_repr(newG, 16)
        else:
            newG = np.base_repr(newG, 16)

        if newB <= 15:
            newB = "0" + np.base_repr(newB, 16)
        else:
            newB = np.base_repr(newB, 16)

        pixels[i, j] = int(inverseSBox[int(newR[0], 16), int(newR[1], 16)], 16), int(inverseSBox[int(newG[0], 16), int(newG[1], 16)], 16), int(inverseSBox[int(newB[0], 16), int(newB[1], 16)], 16)

im.save("watchDecrypted.png")