# coding: utf-8

import warnings 
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=RuntimeWarning)

import cv2
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg',0)
rows,cols = img.shape
M = np.float32([[1,0,100],[0,1,50]])
dst = cv2.warpAffine(img,M,(cols,rows))

mpl.rcParams['toolbar'] = 'None'
plt.imshow( dst )
plt.show() 