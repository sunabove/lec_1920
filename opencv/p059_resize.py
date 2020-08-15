# coding: utf-8

import warnings 
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=RuntimeWarning)

import cv2
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg')
res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#OR

height, width = img.shape[:2]
res = cv2.resize(img,(2*width, 2*height), interpolation = cv2.INTER_CUBIC)

mpl.rcParams['toolbar'] = 'None'
plt.imshow(res)
plt.show() 