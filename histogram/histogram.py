import matplotlib.pyplot as plt
import numpy as np

import Utility as Util

fig, ax = plt.subplots(2,3, constrained_layout=True)

hist = Util.img_ravel("cat.png")
ax[0][0].hist(hist, 256, [0, 256])
ax[0][0].set_title('Original image')

hist = Util.img_ravel("encrypted_image.png")
ax[0][1].hist(hist, 256, [0, 256])
ax[0][1].set_title('Encrypted image')

hist = Util.img_ravel("decrypted_image.png")
ax[0][2].hist(hist, 256, [0, 256])
ax[0][2].set_title('Decrypted image')

hist = Util.img_ravel("./img/red.png")
ax[1][0].hist(hist, 256, [0, 256])
ax[1][0].set_title('Red')

hist = Util.img_ravel("./img/red.png")
ax[1][1].hist(hist, 256, [0, 256])
ax[1][1].set_title('Green')

hist = Util.img_ravel("./img/red.png")
ax[1][2].hist(hist, 256, [0, 256])
ax[1][2].set_title('Blue')





fig.suptitle('Histogram Analysis')

plt.show()
