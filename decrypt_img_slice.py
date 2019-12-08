import random
import time
from multiprocessing import Process, Queue

import cv2

from util import Utility as Util
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle
from slicing.Slicer import Slicer

if __name__ == "__main__":
    result_queue = Queue()
    img = cv2.imread('results/son.png')
    height = int(len(img))
    width = int(len(img[0]))

    array_slicer = Slicer(img, height, width)

    top_left, top_right, bottom_left, bottom_right = array_slicer.slice()

    shuffle = KnuthShuffle()
    image_encryption = ImageEncryption()
    random.seed(123)
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    random_numbers = Util.generate_random_number(random, height, width)
    array_slicer.set_array(random_numbers)

    rand_top_left, rand_top_right, rand_bottom_left, rand_bottom_right = array_slicer.slice()

    start = time.time()

    procs = []
    proc1 = Process(target=image_encryption.decrypt, args=(sBox, inverse_sBox, rand_top_left, top_left, result_queue))
    procs.append(proc1)
    proc1.start()

    proc2 = Process(target=image_encryption.decrypt, args=(sBox, inverse_sBox, rand_top_right, top_right, result_queue))
    procs.append(proc2)
    proc2.start()

    proc3 = Process(target=image_encryption.decrypt,
                    args=(sBox, inverse_sBox, rand_bottom_left, bottom_left, result_queue))
    procs.append(proc3)
    proc3.start()

    proc4 = Process(target=image_encryption.decrypt,
                    args=(sBox, inverse_sBox, rand_bottom_right, bottom_right, result_queue))
    procs.append(proc4)
    proc4.start()

    item1 = result_queue.get()
    item2 = result_queue.get()
    item3 = result_queue.get()
    item4 = result_queue.get()

    for proc in procs:
        proc.join()

    end = time.time()
    print(end - start)

    # cv2.imwrite('results/en_top_left.png', en_image_top_left)
    # cv2.imwrite('results/en_top_right.png', en_image_top_right)
    # cv2.imwrite('results/en_bottom_left.png', en_image_bottom_left)
    # cv2.imwrite('results/en_bottom_right.png', en_image_bottom_right)
    #
    # son = Slicer.concatenate(en_image_top_left, en_image_top_right, en_image_bottom_left, en_image_bottom_right)
    # cv2.imwrite('results/son.png', son)

    cv2.imwrite('results/dec_top_left.png', item1)
    cv2.imwrite('results/dec_top_right.png', item2)
    cv2.imwrite('results/dec_bottom_left.png', item3)
    cv2.imwrite('results/dec_bottom_right.png', item4)

    son = Slicer.concatenate(item1, item2, item3, item4)
    cv2.imwrite('results/dec_son.png', son)
    #
    # cv2.imwrite('results/top_left.png', top_left)
    # cv2.imwrite('results/top_right.png', top_right)
    # cv2.imwrite('results/bottom_left.png', bottom_left)
    # cv2.imwrite('results/bottom_right.png', bottom_right)
