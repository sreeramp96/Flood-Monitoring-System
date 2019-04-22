from imutils.perspective import four_point_transform
import numpy as np
import argparse
import cv2

scaling_factorx = 0.8
scaling_factory = 0.8

#start recording
cap = cv2.VideoCapture(0) 
#background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2() 
count = 0

while(1):
 
  #Capture frame-by-frame
  ret, frame = cap.read()
  # ret = 1 if the video is captured; frame is the image
  
  cv2.imwrite('frame%d.jpg' %count, frame)
  count = count + 1
  
  frame = cv2.resize(frame, None, fx = scaling_factorx, fy = scaling_factory, interpolation = cv2.INTER_AREA)
  
  fgmask = fgbg.apply(frame) #applying foreground mask
  cv2.imshow('frame', fgmask) #shows the background subtracted frame
  
  gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
  cv2.imshow('Original',frame) #original frame
  
  edged_frame = cv2.Canny(frame,100,200)
  cv2.imshow('Edges',edged_frame) #edge detected frame
  
  k = cv2.waitKey(5);
  if k == 27:
    break
cap.release() #When everything done, release the capture
cv2.destroyAllWindows()
