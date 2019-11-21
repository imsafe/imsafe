import numpy as np
import Utility as Util


class KnuthShuffle:
    def __init__(self):
        self.sBox = 0
        self.inverse_sBox = 0

    def create_sBox(self, random):
        x = np.arange(256)

        for i in range(255, -1, -1):
            j = random.randint(0, 255)
            temp = x[i]
            x[i] = x[j]
            x[j] = temp

        x = np.reshape(x, (16, 16))
        self.sBox = np.empty((16, 16), dtype='object')

        for i in range(0, 16):
            for j in range(0, 16):
                self.sBox[i][j] = Util.convertDecToHex(x[i][j])

        return self.sBox

    def create_inverse_sBox(self):
        self.inverse_sBox = np.empty((16, 16), dtype='object')

        for i in range(0, 16):
            for j in range(0, 16):
                value = self.sBox[i, j]
                row = int(value[0], 16)
                column = int(value[1], 16)
                self.inverse_sBox[row, column] = np.base_repr(i, 16) + np.base_repr(j, 16)

        return self.inverse_sBox
