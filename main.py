# this file use for testing your object detection with minimum requirement

import cv2 
import numpy as np

cap = cv2.VideoCapture(1)

while True:
	ret, frame = cap.read()
	cv2.imshow('input', frame)
	if cv2.waitkey(1) == 99:		# press "C" to capture
		break

cap.release()

cv2.imshow('Captured Image', frame)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_yellow = np.array9([0, 199, 204])
upper_yellow = np.array([155, 253, 255])
mask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)

bit_yellow = cv2.bitwise_and(hsv, hsv, mask=mask1)
imgyellow = cv2.cvtColor(bit_yellow, cv2.COLOR_HSV2BGR)

cv2.imshow('yellow', imgyellow)