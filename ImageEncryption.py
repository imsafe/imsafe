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
