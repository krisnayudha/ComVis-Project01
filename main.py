import cv2


image = cv2.imread("shapes1.png",1) # load image in color

# convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#find threshold of the image
_, thrash = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
	shape = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
	x_cor = shape.ravel()[0]
	y_cor = shape.ravel()[1]

	if len(shape) == 3:
		cv2.drawContours(image, [shape], 0, (0,0,255), 4)
		cv2.putText(image, "Triangle", (x_cor, y_cor), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))

cv2.imshow("shape", image)
cv2.imshow("Bin", thrash)
cv2.waitKey(0)
cv2.destroyAllWindows()