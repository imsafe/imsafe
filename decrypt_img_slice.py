import random
import time
from multiprocessing import Process, Queue

import cv2

from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle
from slicing.Slicer import Slicer
from util import Utility as Util

if __name__ == "__main__":
    result_queue = Queue()

    encrypted_image_file_name = 'results/encrypted_image.png'
    decrypted_image_file_name = 'results/decrypted_image.png'

    en_img = cv2.imread(encrypted_image_file_name)

    height = int(len(en_img))
    width = int(len(en_img[0]))

    array_slicer = Slicer(en_img, height, width)
    en_img_top_left, en_img_top_right, en_img_bottom_left, en_img_bottom_right = array_slicer.slice()

    random.seed(123)

    shuffle = KnuthShuffle()
    sBox = shuffle.create_sBox(random)
    inverse_sBox = shuffle.create_inverse_sBox()

    random_numbers = Util.generate_random_number(random, height, width)

    array_slicer.set_array(random_numbers)
    rand_top_left, rand_top_right, rand_bottom_left, rand_bottom_right = array_slicer.slice()

    image_encryption = ImageEncryption()

    start = time.perf_counter()

    procs = []
    proc1 = Process(target=image_encryption.decrypt,
                    args=(sBox, inverse_sBox, rand_top_left, en_img_top_left, result_queue, 1))
    procs.append(proc1)
    proc1.start()

    proc2 = Process(target=image_encryption.decrypt,
                    args=(sBox, inverse_sBox, rand_top_right, en_img_top_right, result_queue, 2))
    procs.append(proc2)
    proc2.start()

    proc3 = Process(target=image_encryption.decrypt,
                    args=(sBox, inverse_sBox, rand_bottom_left, en_img_bottom_left, result_queue, 3))
    procs.append(proc3)
    proc3.start()

    proc4 = Process(target=image_encryption.decrypt,
                    args=(sBox, inverse_sBox, rand_bottom_right, en_img_bottom_right, result_queue, 4))
    procs.append(proc4)
    proc4.start()

    image_slice_list = [result_queue.get() for i in range(4)]
    image_slice_list.sort(key=Util.sortSecond)

    for proc in procs:
        proc.join()

    finish = time.perf_counter()

    print('Finished in {} second(s)'.format(finish - start))

    cv2.imwrite('results/dec_top_left.png', image_slice_list[0][0])
    cv2.imwrite('results/dec_top_right.png', image_slice_list[1][0])
    cv2.imwrite('results/dec_bottom_left.png', image_slice_list[2][0])
    cv2.imwrite('results/dec_bottom_right.png', image_slice_list[3][0])

    decrypted_image = Slicer.concatenate(image_slice_list[0][0], image_slice_list[1][0], image_slice_list[2][0],
                                         image_slice_list[3][0])
    cv2.imwrite(decrypted_image_file_name, decrypted_image)
