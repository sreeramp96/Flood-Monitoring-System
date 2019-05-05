from imutils.perspective import four_point_transform
from imutils import paths
import numpy as np
import imutils 
import argparse
import cv2
#import random
import math
import matplotlib.pyplot as plt

scaling_factorx = 0.8
scaling_factory = 0.8

cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
count = 0
height = []

#for capture frame by frame
#nframes = 1024
#interval = 5
#for i in range(nframes):
     #ret, img = cap.read()
     #cv2.imwrite('./img_'+str(i).zfill(4)+'.png', img)
     #random_time = interval
    
while(1):

    ret, frame = cap.read()

    if frame is None:
    	break
	
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 1, 100)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap);

    if lines is not None:
	    for line in lines:
		for x1, x2, y1, y2 in line:
			dot1 = (x1, y1)
			dot2 = (x2, y2)
			cv2.line(frame, dot1, dot2, (255,0,0), 3)
			length = y1 - y2
			print(length)
			height.append(length)

    cv2.imshow("Outpur Frame", frame)

    frame = cv2.resize(frame, None, fx = scaling_factorx, fy = scaling_factory, interpolation = cv2.INTER_AREA)

    edged_frame = cv2.Canny(frame, 1, 100)
    cv2.imshow('Edged Frame', edged_frame)

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

x = []
y = []

for i in range(len(height)):
	x.append(i)
	y.append(height[i])

cap.release()
cv2.destroyAllWindows()

print(x,y) 
plt.plot(x, y)  
plt.xlabel('x - axis') 
plt.ylabel('y - axis')  
plt.title('Height') 
plt.show()

