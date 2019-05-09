from imutils.perspective import four_point_transform
from imutils import paths
import numpy as np
import imutils
import argparse
import cv2
import random
import math
import matplotlib.pyplot as plt
from firebase import firebase
import json

firebase = firebase.FirebaseApplication('https://floodmonitoringsystem-5c2e1.firebaseio.com/', None)

scaling_factorx = 0.8
scaling_factory = 0.8

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
count = 0
height = []

# for capture frame by frame
nframes = 20
interval = 10
flag = 0
r = None
for i in range(nframes):
    ret, frame = cap.read()
    # Select ROI
    if flag == 0:
        r = cv2.selectROI(frame)
        print(r)
        frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]  # Crop image
        flag = 1
    frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]  # Crop image
    cv2.imwrite('./img_' + str(i).zfill(4) + '.png', frame)
    random_time = interval

# if __name__ == '__main__' :
# im = cv2.imread("image.jpg") # Read image
# r = cv2.selectROI(im)  # Select ROI
# imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] # Crop image
# cv2.imshow("Image", imCrop)# Display cropped image
# cv2.waitKey(0)

while (1):

    ret, frame = cap.read()

    if frame is None:
        break

    frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 1, 100)
    minLineLength = 250
    maxLineGap = 50
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, minLineLength, maxLineGap)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if lines is not None:
        for line in lines:
            for x1, x2, y1, y2 in line:
                dot1 = (x1, y1)
                dot2 = (x2, y2)
                cv2.line(frame, dot1, dot2, (255, 0, 0), 3)
                length = y1 - y2
                print(length)
                height.append(length)
                if length < 100:
                    data = {'height': length, 'message': 'crtical'}
                    result = firebase.post("/floodmonitoringsystem-5c2e1/data/", data)

cv2.imshow("Output Frame", frame)

frame = cv2.resize(frame, None, fx=scaling_factorx, fy=scaling_factory, interpolation=cv2.INTER_AREA)

edged_frame = cv2.Canny(frame, 1, 100)
cv2.imshow('Edged Frame', edged_frame)

x = []
y = []

for i in range(len(height)):
    x.append(i)
    y.append(height[i])

cap.release()
cv2.destroyAllWindows()

print(x, y)
plt.plot(x, y)
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Height')
plt.show()
