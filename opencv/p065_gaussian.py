# coding: utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./data/opencv_logo.png')
blur = cv2.GaussianBlur(img,(5,5), 0)
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur), plt.title('Gaussian')
plt.xticks([]), plt.yticks([])
plt.show()