import random
import time
from multiprocessing import Queue

import cv2

import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle

if __name__ == "__main__":
    result_queue = Queue()
    img = cv2.imread('../img/test_middle.png')
    height = int(len(img))
    width = int(len(img[0]))

    x = int(height / 2)
    y = int(width / 2)

    top_left = img[:x, :y]
    top_right = img[:x, y:width]
    bottom_left = img[x:height, :y]
    bottom_right = img[x:height, y:width]

    # top = np.concatenate((top_left, top_right), 1)
    # bottom = np.concatenate((bottom_left, bottom_right), 1)
    # son = np.concatenate((top, bottom), 0)
    # cv2.imwrite('../results/son.png', son)
    #
    # cv2.imwrite('../results/top_left.png', top_left)
    # cv2.imwrite('../results/top_right.png', top_right)
    # cv2.imwrite('../results/bottom_left.png', bottom_left)
    # cv2.imwrite('../results/bottom_right.png', bottom_right)

    shuffle = KnuthShuffle()
    image_encryption = ImageEncryption()
    random.seed(123)
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    random_numbers = Util.generate_random_number(random, height, width)

    rand_top_left = random_numbers[:x, :y]
    rand_top_right = random_numbers[:x, y:width]
    rand_bottom_left = random_numbers[x:height, :y]
    rand_bottom_right = random_numbers[x:height, y:width]

    start = time.time()
    en_image_top_left = image_encryption.encrypt(sBox, rand_top_left, top_left)
    en_image_top_right = image_encryption.encrypt(sBox, rand_top_right, top_right)
    en_image_bottom_left = image_encryption.encrypt(sBox, rand_bottom_left, bottom_left)
    en_image_bottom_right = image_encryption.encrypt(sBox, rand_bottom_right, bottom_right)
    # procs = []
    # proc1 = Process(target=image_encryption.encrypt, args=(sBox, rand_top_left, top_left, result_queue))
    # procs.append(proc1)
    # proc1.start()
    #
    # proc2 = Process(target=image_encryption.encrypt, args=(sBox, rand_top_left, top_right, result_queue))
    # procs.append(proc2)
    # proc2.start()
    #
    # proc3 = Process(target=image_encryption.encrypt, args=(sBox, rand_top_left, bottom_left, result_queue))
    # procs.append(proc3)
    # proc3.start()
    #
    # proc4 = Process(target=image_encryption.encrypt, args=(sBox, rand_top_left, bottom_right, result_queue))
    # procs.append(proc4)
    # proc4.start()
    #
    # item1 = result_queue.get()
    # item2 = result_queue.get()
    # item3 = result_queue.get()
    # item4 = result_queue.get()
    #
    # for proc in procs:
    #     proc.join()
    end = time.time()
    print(end - start)

    # cv2.imwrite('../results/en_top_left.png', en_image_top_left)
    # cv2.imwrite('../results/en_top_right.png', en_image_top_right)
    # cv2.imwrite('../results/en_bottom_left.png', en_image_bottom_left)
    # cv2.imwrite('../results/en_bottom_right.png', en_image_bottom_right)
    #
    # top = np.concatenate((en_image_top_left, en_image_top_right), 1)
    # bottom = np.concatenate((en_image_bottom_left, en_image_bottom_right), 1)
    # son = np.concatenate((top, bottom), 0)
    # cv2.imwrite('../results/son.png', son)
    #
    # cv2.imwrite('../results/top_left.png', top_left)
    # cv2.imwrite('../results/top_right.png', top_right)
    # cv2.imwrite('../results/bottom_left.png', bottom_left)
    # cv2.imwrite('../results/bottom_right.png', bottom_right)
