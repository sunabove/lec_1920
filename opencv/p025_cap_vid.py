# coding: utf-8
print( "Hello ...", flush=True )

import time
import numpy as np
import cv2

print( "Done importing!", flush=True )

print( "Opening video device ....", flush=True )

cap = cv2.VideoCapture(0)

print( "Done...", flush=True )
print( "Video capturing ....", flush=True )

frame_rate = 10
prev = 0

while(True):
    time_elapsed = time.time() - prev

    if prev is 0 or time_elapsed > 1./frame_rate :
        prev = time.time()
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # flip image vertically
        vf_gray = cv2.flip( gray, 0 )
        # flip image horizontally
        #hg_gray = cv2.flip( gray, 1 )
        # Display the resulting frame
        cv2.imshow('frame', vf_gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pass
    else :
        time.sleep( 0.01 )
    pass
pass

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print( "Done...", flush=True )
print( "Good bye!", flush=True )

pass