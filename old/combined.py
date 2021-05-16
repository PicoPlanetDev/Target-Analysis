# import the necessary packages
import numpy as np
import cv2
import math

# multipliers are from NRA A-17 target in millimeters
outer = 46.150
five = 37.670/outer
six = 29.210/outer
seven = 20.750/outer
eight = 12.270/outer
nine = 3.810/outer

def ComputeDistance(x1, y1, x2, y2):
	return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

# Get the source image
img = cv2.imread('bottom-right.jpeg')
output = img.copy()

# --- [FINDS BULLET HOLES] ---

# Threshold the image
img_thresholded = cv2.inRange(img, (100, 100, 100), (255, 255, 255))
#cv2.imshow('Image Thresholded', img_thresholded)

# Remove noise from the binary image using the opening operation
kernel = np.ones((10,10),np.uint8)
opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
#cv2.imshow('opening',opening)

# Find contours based on the denoised image
contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
	# Get the area of the contours
	area = cv2.contourArea(contour)
	
	# Check if area is between max and min values for a bullet hole. Area is usually about 1000
	if area<1500 and area>500:

		# Draw the detected contour for debugging
		cv2.drawContours(output,[contour],0,(255,0,0),2)

		# Create an enclosing circle that can represent the bullet hole
		(holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
		holeCenter = (int(holeX),int(holeY))
		holeRadius = int(holeRadius)

		# Draw the enclosing circle in addition to a dot at the center
		cv2.circle(output,holeCenter,holeRadius,(0,255,0),2)
		cv2.circle(output,holeCenter,1,(0,0,255),2)

# --- [FINDS THE TARGET] ---

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, minRadius=130)
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle

		if r-

		pixelOuter = r
		pixelFive = r*five
		pixelSix = r*six
		pixelSeven = r*seven
		pixelEight = r*eight
		pixelNine = r*nine

		cv2.circle(output, (x, y), r, (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(pixelFive), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(pixelSix), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(pixelSeven), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(pixelEight), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(pixelNine), (0, 255, 0), 2)
		cv2.circle(output, (x, y), 1, (0, 0, 255), 2)
		#cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

distance = ComputeDistance(holeX, holeY, x, y)
print(distance)

if distance-holeRadius < pixelNine:
	print("X")
	cv2.putText(output, "X", (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

if distance-holeRadius < pixelEight and distance-holeRadius > pixelNine:
	print("0")
	cv2.putText(output, "1", (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

if distance-holeRadius < pixelSeven and distance-holeRadius > pixelEight:
	print("1")
	cv2.putText(output, "2", (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

if distance-holeRadius < pixelSix and distance-holeRadius > pixelSeven:
	print("2")
	cv2.putText(output, "3", (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

if distance-holeRadius < pixelFive and distance-holeRadius > pixelSix:
	print("3")
	cv2.putText(output, "4", (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

if distance-holeRadius < pixelOuter and distance-holeRadius > pixelFive:
	print("4")
	cv2.putText(output, "5", (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

# Currently only scores target to a 4

# show the output image
cv2.imshow("output", output) # cv2.imshow("output", np.hstack([img, output]))
cv2.waitKey(0)