from imutils.perspective import four_point_transform
import numpy as np
import argparse
import cv2
 
cap = cv2.VideoCapture(0) #start recording
fgbg = cv2.createBackgroundSubtractorMOG2() #background subtrator

while(1):
  ret, frame = cap.read()
  fgmask = fgbg.apply(frame) #applying foreground mask
  cv2.imshow('frame', fgmask) #shows the background subtracted frame
  
  gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
  cv2.imshow('Original',frame) #original frame
  
  edged_frame = cv2.Canny(frame,100,200)
  cv2.imshow('Edges',edged_frame) #edge detected frame
  
  k= cv2.waitKey(5);
  if k==27:
    break
cap.release()
cv2.destroyAllWindows()
