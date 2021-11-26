# this file use for testing your object detection with minimum requirement

import cv2 
import numpy as np

def nothing(x):
	#any operation
	pass

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1)
# img = cv2.imread('shapes1.png', 1)

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

	# get values from trackbars 
	l_h = cv2.getTrackbarPos('l_h', 'Trackbars')
	l_s = cv2.getTrackbarPos('l_s', 'Trackbars')
	l_v = cv2.getTrackbarPos('l_v', 'Trackbars')
	u_h = cv2.getTrackbarPos('u_h', 'Trackbars')
	u_s = cv2.getTrackbarPos('u_s', 'Trackbars')
	u_v = cv2.getTrackbarPos('u_v', 'Trackbars')


	lower_yellow = np.array([l_h, l_s, l_v]) # 15, 93, 0
	upper_yellow = np.array([u_h, u_s, u_v]) # 40, 255, 255
	
	# lower_yellow = np.array([15,93,0])
	# upper_yellow = np.array([40,255,255])

	# set kernel to filtering mask
	kernel = np.ones((15,15),np.uint8)

	# threshold the hsv image to get only yellow color
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	img = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	
	imghsv = cv2.bitwise_and(hsv, hsv, mask=mask)

	cv2.imshow('input', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('yellow', imghsv)



	if cv2.waitKey(1) == 27:		# press "esc" to exit
		break

# cv2.waitKey(0)
# cap.release()
cv2.destroyAllWindows()