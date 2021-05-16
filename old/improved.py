import numpy as np
import cv2
import math
import argparse
import csv

# multipliers are from NRA A-17 target in millimeters
outer = 46.150
five = 37.670/outer
six = 29.210/outer
seven = 20.750/outer
eight = 12.270/outer
nine = 3.810/outer

spindleRadius = 2.794

droppedPoints = 0
xCount = 0

# Basic implementation of the distance formula
def ComputeDistance(x1, y1, x2, y2):
	return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

# Set up argparse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-m", "--month", required = True, help = "Month")
ap.add_argument("-d", "--day", required = True, help = "Day")
ap.add_argument("-y", "--year", required = True, help = "Year")
ap.add_argument("-n", "--name", required = True, help = "Name")
args = vars(ap.parse_args())

# Get the image from args
img = cv2.imread(args["image"])

# Get the source image and make a copy for use as the output
#img = cv2.imread('images/bottom-right.jpg')

output = img.copy()

# --- [FINDS THE TARGET] ---
# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# Blur using 3 * 3 kernel
gray_blurred = cv2.blur(gray, (3, 3))
#cv2.imshow("gray_blurred", gray_blurred)

#threshold_image=cv2.inRange(gray_blurred, 100, 255)
#cv2.imshow("threshold_image", threshold_image)
  
# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1.4, 200, minRadius = 130)
  
# Draw circles that are detected
if detected_circles is not None:
  
	# Convert the circle parameters a, b and r to integers
	detected_circles = np.uint16(np.around(detected_circles))
  
	for pt in detected_circles[0, :]:
		a, b, r = pt[0], pt[1], pt[2]

		# Draw a small circle (of radius 1) to show the center.
		cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

		pixelOuter = r

		# Perform a calculation to determine if the system detected the wrong ring, and if so, correct the error
		height, width, channels = img.shape
		if r/width < 0.4 and r/width > 0.35:
			pixelOuter = outer/37.670 * r
		
		if r/width < 0.35:
			pixelOuter = outer/29.210 * r

		pixelFive = pixelOuter*five
		pixelSix = pixelOuter*six
		pixelSeven = pixelOuter*seven
		pixelEight = pixelOuter*eight
		pixelNine = pixelOuter*nine

		spindleRadius = 2.794*(pixelOuter/outer)

		cv2.circle(output, (a, b), int(pixelOuter), (0, 255, 0), 2)
		cv2.circle(output, (a, b), int(pixelFive), (0, 255, 0), 2)
		cv2.circle(output, (a, b), int(pixelSix), (0, 255, 0), 2)
		cv2.circle(output, (a, b), int(pixelSeven), (0, 255, 0), 2)
		cv2.circle(output, (a, b), int(pixelEight), (0, 255, 0), 2)
		cv2.circle(output, (a, b), int(pixelNine), (0, 255, 0), 2)

		# Draw a small circle to show the center.
		cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

# --- [FINDS BULLET HOLES] ---
# Make the image binary using a threshold
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
		#cv2.drawContours(output,[contour],0,(255,0,0),2)

		# Create an enclosing circle that can represent the bullet hole
		(holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
		holeCenter = (int(holeX),int(holeY))
		holeRadius = int(holeRadius)

		# Draw the enclosing circle in addition to a dot at the center
		#cv2.circle(output,holeCenter,holeRadius,(0,255,0),2)
		cv2.circle(output, holeCenter, 1, (0, 0, 255), 3)

		# Draw the spindle
		cv2.circle(output,holeCenter,int(spindleRadius),(0,255,255),2)

		distance = ComputeDistance(holeX, holeY, a, b)

		# Currently only scores target to a 4
		if distance-spindleRadius < pixelNine:
			print("X")
			cv2.putText(output, "X", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
			xCount += 1

		if distance+spindleRadius < pixelEight and distance-spindleRadius > pixelNine:
			print("0")
			cv2.putText(output, "0", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

		if distance+spindleRadius > pixelEight and distance-spindleRadius < pixelSeven:
			print("1")
			cv2.putText(output, "1", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
			droppedPoints += 1

		if distance+spindleRadius > pixelSeven and distance-spindleRadius < pixelSix:
			print("2")
			cv2.putText(output, "2", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
			droppedPoints += 2

		if distance+spindleRadius > pixelSix and distance-spindleRadius < pixelFive:
			print("3")
			cv2.putText(output, "3", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
			droppedPoints += 3

		if distance+spindleRadius > pixelFive and distance-spindleRadius < pixelOuter:
			print("4")
			cv2.putText(output, "4", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
			droppedPoints += 4

with open('data.csv', 'a', newline="") as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow([args["name"], args["month"],args["day"],args["year"],"100","0"])
	filewriter.close()

# show the output image
cv2.imshow("output", output) # cv2.imshow("output", np.hstack([img, output]))
print(args["image"])
cv2.imwrite(args["image"] + "-output.jpg", output)
cv2.waitKey(0)