# coding : utif-8

import cv2

img1 = cv2.imread('ml.png')
img2 = cv2.imread('opencv_logo.png')
height, width, _ = img2.shape
img2 = cv2.resize(img2, (width, height))
dst = cv2.addWeighted(img1,0.7,img2,0.3,0)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()