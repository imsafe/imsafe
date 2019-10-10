import random
import numpy as np


class DynamicSBox:
    seed = 0
    sBox = 0
    inverse_sBox = 0
    x = 0

    def __init__(self, seed):
        random.seed(seed)
        print('Seed', seed)

    def convertDecToHex(self, decimalNumber):
        if decimalNumber <= 15:
            return "0" + np.base_repr(decimalNumber, 16)
        else:
            return np.base_repr(decimalNumber, 16)

    def create_sBox(self):
        self.x = np.arange(256)

        for i in range(255, -1, -1):
            j = random.randint(0, 255)
            temp = self.x[i]
            self.x[i] = self.x[j]
            self.x[j] = temp

        self.x = np.reshape(self.x, (16, 16))
        self.sBox = np.empty((16, 16), dtype='object')

        for i in range(0, 16):
            for j in range(0, 16):
                self.sBox[i][j] = self.convertDecToHex(self.x[i][j])

    def create_inverse_sBox(self):
        self.inverse_sBox = np.empty((16, 16), dtype='object')

        for i in range(0, 16):
            for j in range(0, 16):
                value = self.sBox[i, j]
                row = int(value[0], 16)
                column = int(value[1], 16)
                self.inverse_sBox[row, column] = np.base_repr(i, 16) + np.base_repr(j, 16)


sbox = DynamicSBox(123)
sbox.create_sBox()
sbox.create_inverse_sBox()
