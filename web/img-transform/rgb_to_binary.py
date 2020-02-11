import cv2
import os

originalImage = cv2.imread('../img/coin.png')
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('Black white image', blackAndWhiteImage)
cv2.imshow('Original image',originalImage)
cv2.imshow('Gray image', grayImage)

cv2.imwrite('blackAndWhiteImage.png', blackAndWhiteImage )
cv2.imwrite('originalImage.png', originalImage)

original_size = os.path.getsize('../img/coin.png')
binary_size = os.path.getsize('blackAndWhiteImage.png')
print('Original image: ' , original_size)
print('Binary image: ' , binary_size)
print(original_size/binary_size*100)
