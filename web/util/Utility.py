import math

import cv2
import numpy as np
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity


def convert_dec_to_hex(decimal_number):
    if decimal_number <= 15:
        return "0" + np.base_repr(decimal_number, 16)
    else:
        return np.base_repr(decimal_number, 16)


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
    image_a = cv2.imread(first_image)
    image_b = cv2.imread(second_image)

    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # structural_similarity_index = structural_similarity(image_a, image_b, multichannel=True)
    structural_similarity_index = structural_similarity(gray_a, gray_b)

    print("Structural Similarity Index: {}".format(structural_similarity_index))


def psnr(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    psnr = cv2.PSNR(img1, img2, 255)

    img1 = img1.astype(np.float64) / 255.
    img2 = img2.astype(np.float64) / 255.

    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        print("Same Image")
    else:
        print(10 * math.log10(1. / mse))

    return psnr


def sort_second(val):
    return val[1]


def generate_keys(private_key_file, public_key_file):
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open(private_key_file, "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open(public_key_file, "wb")
    file_out.write(public_key)
    file_out.close()


def sign_image(file, private_key_file, signature_file):
    key = RSA.import_key(open(private_key_file).read())
    h = SHA256.new()
    block_size = 65536

    with open(file, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(block_size)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            h.update(fb)  # Update the hash
            fb = f.read(block_size)  # Read the next block from the file

    signature = pkcs1_15.new(key).sign(h)

    f = open(signature_file, 'wb')
    f.write(signature)
    f.close()


def verify(file, public_key_file, signature_file):
    key = RSA.import_key(open(public_key_file).read())

    signature = open(signature_file, 'rb').read()

    h = SHA256.new()
    block_size = 65536

    with open(file, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(block_size)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            h.update(fb)  # Update the hash
            fb = f.read(block_size)  # Read the next block from the file
    try:
        pkcs1_15.new(key).verify(h, signature)
        is_valid = True
    except (ValueError, TypeError):
        is_valid = False

    return is_valid