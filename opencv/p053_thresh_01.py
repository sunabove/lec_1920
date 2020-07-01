# coding: utf-8

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread( './data/gradient.png',0)

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

fig = plt.figure()
rows = 2
cols = 3
for r in range( rows ) :
    for c in range(cols) :
        idx = r*cols + c
        img = images[idx]
        ax = fig.add_subplot( rows, cols, idx + 1)
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.set_title( titles[idx] )
        ax.set_xticks([]), ax.set_yticks([])        
    pass
pass

plt.show()
