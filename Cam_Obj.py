import cv2
import numpy as np
import PySimpleGUI as sg

head = ['Jumlah Segitiga','Posisi 1','Posisi 2','Posisi 3']
data = [['Small', 0,0,0,0],
		['Medium',0,0,0,0],
		['Large',0,0,0,0]]
layout = [[sg.Image('blank640x480.png', key = 'input'),sg.Image('blank640x480.png', key = 'impro')],
			[sg.Button('Captured'), 
			sg.Button('Exit'), 
			sg.Table(data,headings = head,hide_vertical_scroll=True, justification='center', key='table', num_rows=3,auto_size_columns=True)
			],
			[]]

window = sg.Window('Triangle detection and Position', layout)


# image = cv2.imread("shapes1.png",1) # load image in color
cap = cv2.VideoCapture(1)



while True : 
	event, values = window.read(0.01)
	ret, Frame = cap.read()
	imgbytes = cv2.imencode('.png', Frame)[1].tobytes()
	window['input'].update(data=imgbytes)

	if event == 'Captured':
		smallposisi1 = 0
		smallposisi2 = 0
		smallposisi3 = 0
		mediumposisi1 = 0
		mediumposisi2 = 0
		mediumposisi3 = 0
		largeposisi1 = 0
		largeposisi2 = 0
		largeposisi3 = 0
		# capture object
		objectFrame = Frame

		# find object with yellow color
		hsv = cv2.cvtColor(objectFrame, cv2.COLOR_BGR2HSV)
		lower_yellow = np.array([15,93,0])
		upper_yellow = np.array([40,255,255])

		# set kernel to filtering mask
		kernel = np.ones((15,15),np.uint8)

		# threshold the hsv image to get only yellow color
		mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
		img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		img = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		imghsv = cv2.bitwise_and(hsv, hsv, mask=mask)

		# find triangle object with approxPoly
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

		# imgbytes = cv2.imencode('.png', mask)[1].tobytes()
		# window['impro'].update(data=imgbytes)

		for contour in contours:
			area = cv2.contourArea(contour)
			shape = cv2.approxPolyDP(contour, 0.1*cv2.arcLength(contour, True), True)
			x,y,w,h = cv2.boundingRect(shape)
			
			if len(shape) == 3:
				rect = cv2.minAreaRect(contour)
				box = cv2.boxPoints(rect)
				border = np.int0(box)
				borderImg = cv2.drawContours(objectFrame,[border], 0, (255, 0 , 255), 2)
				# #  calculate moments for each cotour
				M = cv2.moments(contour)

				# calculate x,y coordinate of center 
				if M['m00'] != 0:
					cX = int(M['m10']/M['m00'])
					cY = int(M['m01']/M['m00'])
				else:
					cX, cY = 0,0

				cv2.putText(borderImg, "points: " + str(len(shape)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
				cv2.putText(borderImg, "area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
				cv2.circle(borderImg, (cX, cY), 2, (0,255,0), -1)
				cv2.putText(borderImg, "center: " + str(int(cX)) + "," + str(int(cY)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
				imgbytes = cv2.imencode('.png', borderImg)[1].tobytes()
				window['impro'].update(data=imgbytes)

				if area <= 1000:
					ukuran = 'S'
					if cX <= 210:
						smallposisi1 = smallposisi1 + 1
					if 210 < cX <= 420:
						smallposisi2 = smallposisi2 + 1
					if cX > 420:
						smallposisi3 = smallposisi3 + 1
				elif 1000 < area <= 3000:
					ukuran = 'M'
					if cX <= 210:
						mediumposisi1 = mediumposisi1 + 1
					if 210 < cX <= 420:
						mediumposisi2 = mediumposisi2 + 1
					if cX > 420:
						mediumposisi3 = mediumposisi3 + 1
				elif area > 3000:
					if cX <= 210:
						largeposisi1 = largeposisi1 + 1
					if 210 < cX <= 420:
						largeposisi2 = largeposisi2 + 1
					if cX > 420:
						largeposisi3 = largeposisi3 + 1

		data = [['Small', smallposisi1,smallposisi2,smallposisi3],
				['Medium', mediumposisi1,mediumposisi2,mediumposisi3],
				['Large', largeposisi1,largeposisi2,largeposisi3]]

		window['table'].update(data)
	elif event == 'Exit':
		break

cap.release()
window.close()