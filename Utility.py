import numpy as np
from skimage.measure import compare_ssim
import cv2
from matplotlib import pyplot as plt


def convertDecToHex(decimalNumber):
    if decimalNumber <= 15:
        return "0" + np.base_repr(decimalNumber, 16)
    else:
        return np.base_repr(decimalNumber, 16)


def image_histogram(image):
    img = cv2.imread(image, 0)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist, bins = np.histogram(img.ravel(), 256, [0, 256])
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()

def img_ravel(image):
    img = cv2.imread(image, 0)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist, bins = np.histogram(img.ravel(), 256, [0, 256])

    return img.ravel()

def calculate_ssim(first_image, second_image):
    imageA = cv2.imread(first_image)
    imageB = cv2.imread(second_image)

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # structural_similarity_index = compare_ssim(imageA, imageB, multichannel=True)
    structural_similarity_index = compare_ssim(grayA, grayB)

    print("Structural Similarity Index: {}".format(structural_similarity_index))
