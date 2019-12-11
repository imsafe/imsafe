import cv2
import numpy as np


class BitPlane:
    def __init__(self):
        self.bit_planes = []

    def slice(self, img_path):
        # Read the image in greyscale
        img = cv2.imread(img_path, 0)
        lst = []
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                lst.append(np.binary_repr(img[i][j], width=8))  # width = no. of bits

        for j in range(8):
            plane = (np.array([int(i[7 - j]) for i in lst], dtype=np.uint8) * 2 ** j).reshape(img.shape[0],
                                                                                              img.shape[1])
            self.bit_planes.append(plane)

        return self.bit_planes

    def get_plane(self, plane_number):
        return self.bit_planes[plane_number - 1]

    def get_ms(self, plane_count):
        x = len(self.bit_planes[0])
        y = len(self.bit_planes[0][0])
        sum = np.zeros((x, y))
        for i in range(7, plane_count - 1, -1):
            sum = sum + self.bit_planes[i]
        return sum

    def concat(self):
        # Concatenate these images for ease of display using cv2.hconcat()
        finalr = cv2.hconcat([self.get_plane(8), self.get_plane(7), self.get_plane(6), self.get_plane(5)])
        finalv = cv2.hconcat([self.get_plane(4), self.get_plane(3), self.get_plane(2), self.get_plane(1)])

        # Vertically concatenate
        final = cv2.vconcat([finalr, finalv])

        cv2.imwrite('results/bit_planes.png', final)
