import cv2
import numpy as np
import PySimpleGUI as sg

head = [['Jumlah Segitiga', 'Posisi 1', 'Posisi 2', 'Posisi 3']]
data = [['Small', 0, 0, 0],
		['Medium',0, 0, 0],
		['Large', 0, 0, 0]]
layout = [[sg.Image('blank640x480.png', key = 'input'),sg.Image('balnk640x480.png', key = 'impro')],
			[sg.Button('Captured'), 
			sg.Button('Exit'),
			sg.Table(data, headings=head,hide_vertical_scroll=True, justification='center', key='table', num_rows=4)],
			[]]

window = sg.Window('Triangle detection and Position', layout)

# image = cv2.imread("shapes1.png",1) # load image in color
cap = cv2.VideoCapture(1)

while True : 
	event, values = window.read(timeout=10)
	ret, Frame = cap.read()
	imgbytes = cv2.imencode('.png', Frame)[1].tobytes()
	window['input'].update(data=imgbytes)

	# find object with yellow color
	hsv = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)
	lower_yellow = np.array([0, 199, 204])
	upper_yellow = np.array([155, 253, 255])
	mask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)

	# convert to grayscale
	gray_image = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

	# find threshold of the image
	_, thrash = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)
	contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	# find the centre of the object
	cnt = contours[0]
	M = cv2.moments(cnt)


	for contour in contours:
		area = cv2.contourArea(contours[contour])
		x,y,w,h = cv2.boundingRect(contours[contour])
		rect_area = w*h
		shape = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		# x_cor = shape.ravel()[0]
		# y_cor = shape.ravel()[1]

		# if len(shape) == 3:
		# 	cv2.drawContours(Frame, [shape], 0, (0,0,255), 4)
		# 	cv2.putText(Frame, "Triangle", (x_cor, y_cor), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
		if len(shape) == 3:
			if rect_area <= 2000:
				ukuran = 'S'
			elif 2001 <= rect_area <= 5000:
				ukuran = 'M'
			elif 5001 <= rect_area <= 8000:
				ukuran = 'L'
			

# cv2.imshow("shape", Frame)
# cv2.imshow("Bin", thrash)
# cv2.waitKey(0)
# cv2.destroyAllWindows()