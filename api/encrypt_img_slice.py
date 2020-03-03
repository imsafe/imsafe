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

def encrypt(obj, password):
    # image_file_name = 'media/' + img_name
    # encrypted_image_file_name = staticfiles_storage.path('results/encrypted_image.png')

    # img = cv2.imread(image_file_name)
    img = ImageEncryption.readb64(obj.image)

    height = int(len(img))
    width = int(len(img[0]))

    array_slicer = Slicer(img, height, width)
    img_top_left, img_top_right, img_bottom_left, img_bottom_right = array_slicer.slice()

    np.random.seed(int(password))

    shuffle = KnuthShuffle()
    s_box = shuffle.create_s_box(np.random)

    random_numbers = np.random.randint(0, 16, (height, width, 6))
    array_slicer.set_array(random_numbers)
    rand_top_left, rand_top_right, rand_bottom_left, rand_bottom_right = array_slicer.slice()

    image_encryption = ImageEncryption()

    start = time.perf_counter()

    result_queue = Queue()

    procs = []
    proc1 = Process(target=image_encryption.encrypt, args=(s_box, rand_top_left, img_top_left, result_queue, 1))
    procs.append(proc1)
    proc1.start()

    proc2 = Process(target=image_encryption.encrypt, args=(s_box, rand_top_right, img_top_right, result_queue, 2))
    procs.append(proc2)
    proc2.start()

    proc3 = Process(target=image_encryption.encrypt, args=(s_box, rand_bottom_left, img_bottom_left, result_queue, 3))
    procs.append(proc3)
    proc3.start()

    proc4 = Process(target=image_encryption.encrypt, args=(s_box, rand_bottom_right, img_bottom_right, result_queue, 4))
    procs.append(proc4)
    proc4.start()

    image_slice_list = [result_queue.get() for i in range(4)]
    image_slice_list.sort(key=Util.sort_second)

    for proc in procs:
        proc.join()

    finish = time.perf_counter()

    print('Finished in {} second(s)'.format(finish - start))

    encrypted_image = Slicer.concatenate(image_slice_list[0][0], image_slice_list[1][0], image_slice_list[2][0],
                                         image_slice_list[3][0])

    media_root = settings.MEDIA_ROOT
    write_path = media_root+'/uploads/'+obj.name+'.png' 
    cv2.imwrite(write_path, encrypted_image)
    obj.image = write_path
    obj.save()

    # ------------
    # private_key_file = staticfiles_storage.path('keys/private-'+img_name+'.pem')
    # public_key_file = staticfiles_storage.path('keys/public-'+img_name+'.pem')
    # signature_file = staticfiles_storage.path('keys/signature-'+img_name+'.pem')

    # Util.generate_keys(private_key_file, public_key_file)
    # Util.sign_image(encrypted_image_file_name, private_key_file, signature_file)

    return True

if __name__ == '__main__':
    encrypt()


