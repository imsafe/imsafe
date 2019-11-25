import Utility as Util
import cv2
import numpy as np
import math

img1_path = "img/coin.png"
img2_path = "results/4-bit-slice.png"
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)


print(Util.psnr(img1, img1))

img1 = img1.astype(np.float64) / 255.
img2 = img2.astype(np.float64) / 255.

mse = np.mean((img1 - img1) ** 2)
if mse == 0:
     print("Same Image")
else:
    print(10 * math.log10(1. / mse))
