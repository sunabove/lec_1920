# coding: utf-8

import cv2
from timeit import timeit

# Load an color image in grayscale
print( cv2.useOptimized() )

img = cv2.imread('messi5.jpg',0)

code_to_test = """
res = cv2.medianBlur(img,49)
"""
elapsed_time = timeit(code_to_test, number=100)/100

print(elapsed_time)  