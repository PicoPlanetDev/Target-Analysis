# import the necessary packages
import numpy as np
import argparse
import cv2

# multipliers

outer = 46.150

five = 37.670/outer
six = 29.210/outer
seven = 20.750/outer
eight = 12.270/outer
nine = 3.810/outer

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

im = image.copy()

grayHoles=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
grayHoles=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)[1]
#cv2.imshow('gray',gray)

contours,hierarchy = cv2.findContours(grayHoles,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE   )

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area>600 and area<690:
        cv2.drawContours(output,[cnt],0,(255,0,0),2)
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(output,center,radius,(0,255,0),2)

#scv2.imshow('im',im)

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
		cv2.circle(output, (x, y), r, (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(r*five), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(r*six), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(r*seven), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(r*eight), (0, 255, 0), 2)
		cv2.circle(output, (x, y), int(r*nine), (0, 255, 0), 2)
		#cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	# show the output image
	cv2.imshow("output", np.hstack([image, output]))
	cv2.waitKey(0)

