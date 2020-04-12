import os.path
import time
from multiprocessing import Process, Queue
from django.contrib.staticfiles.storage import staticfiles_storage

import cv2
import numpy as np
from django.conf import settings

from .encryption.ImageEncryption import ImageEncryption
from .encryption.KnuthShuffle import KnuthShuffle
from .slicing.Slicer import Slicer
from .util import Utility as Util

def decrypt(obj, password):
    en_img = cv2.imread(obj.image.path)

    height = int(len(en_img))
    width = int(len(en_img[0]))

    array_slicer = Slicer(en_img, height, width)
    en_img_top_left, en_img_top_right, en_img_bottom_left, en_img_bottom_right = array_slicer.slice()

    np.random.seed(int(password))

    shuffle = KnuthShuffle()
    s_box = shuffle.create_s_box(np.random)
    inverse_s_box = shuffle.create_inverse_s_box()

    random_numbers = np.random.randint(0, 16, (height, width, 6))
    array_slicer.set_array(random_numbers)
    rand_top_left, rand_top_right, rand_bottom_left, rand_bottom_right = array_slicer.slice()

    image_encryption = ImageEncryption()

    start = time.perf_counter()

    result_queue = Queue()

    procs = []
    proc1 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_top_left, en_img_top_left, result_queue, 1))
    procs.append(proc1)
    proc1.start()

    proc2 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_top_right, en_img_top_right, result_queue, 2))
    procs.append(proc2)
    proc2.start()

    proc3 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_bottom_left, en_img_bottom_left, result_queue, 3))
    procs.append(proc3)
    proc3.start()

    proc4 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_bottom_right, en_img_bottom_right, result_queue, 4))
    procs.append(proc4)
    proc4.start()

    image_slice_list = [result_queue.get() for i in range(4)]
    image_slice_list.sort(key=Util.sort_second)

    for proc in procs:
        proc.join()

    finish = time.perf_counter()

    print('Finished in {} second(s)'.format(finish - start))

    decrypted_image = Slicer.concatenate(image_slice_list[0][0], image_slice_list[1][0], image_slice_list[2][0],
                                        image_slice_list[3][0])

    media_root = settings.MEDIA_ROOT
    write_path = os.path.join(settings.MEDIA_ROOT, 'decrypted/'+obj.name+str(obj.id)+'.png') 
    cv2.imwrite(write_path, decrypted_image)
    
    return 'https://imsafe.systems'+settings.MEDIA_URL+'decrypted/'+obj.name+str(obj.id)+'.png'
