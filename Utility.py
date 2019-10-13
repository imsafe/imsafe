import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def convertDecToHex(decimalNumber):
    if decimalNumber <= 15:
        return "0" + np.base_repr(decimalNumber, 16)
    else:
        return np.base_repr(decimalNumber, 16)


def imageHistogram():
    img = cv.imread('cat.png', 0)
    hist = cv.calcHist([img], [0], None, [256], [0, 256])
    hist, bins = np.histogram(img.ravel(), 256, [0, 256])
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()
