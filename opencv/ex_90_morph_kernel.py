# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging as log
log.basicConfig( format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)04d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S', level=log.INFO )

# 모폴로이 커널 예
import cv2

rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

print()
print( "Rectangle")
print(rect)

print()
print( "Cross")
print(cross)

print()
print( "Ellipse")
print(ellipse)
