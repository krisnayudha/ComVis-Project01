# this file use for testing your object detection with minimum requirement

import cv2 
import numpy as np

def nothing(x):
	#any operation
	pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('Trackbars')
cv2.createTrackbar('l_h', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('l_s', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('l_v', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('u_h', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('u_s', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('u_v', 'Trackbars', 0, 255, nothing)

while True:
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# get values from trackars 
	l_h = cv2.getTrackbarPos('l_h', 'Trackbars')
	l_s = cv2.getTrackbarPos('l_s', 'Trackbars')
	l_v = cv2.getTrackbarPos('l_s', 'Trackbars')
	u_h = cv2.getTrackbarPos('u_h', 'Trackbars')
	u_s = cv2.getTrackbarPos('u_s', 'Trackbars')
	u_v = cv2.getTrackbarPos('u_s', 'Trackbars')


	lower_yellow = np.array([l_h, l_s, l_v]) # 15, 93, 243
	upper_yellow = np.array([u_h, u_s, u_v]) # 53, 219, 211

	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

	yellow = cv2.bitwise_and(hsv, hsv, mask=mask)

	cv2.imshow('input', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('yellow', yellow)


	if cv2.waitKey(1) == 27:		# press "esc" to exit
		break

cap.release()
cv2.destroyAllWindows()