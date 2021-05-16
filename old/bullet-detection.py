import cv2
import numpy as np

# Get the source image
img = cv2.imread('top.jpeg')

# Threshold the image
img_thresholded = cv2.inRange(img, (100, 100, 100), (255, 255, 255))
#cv2.imshow('Image Thresholded', img_thresholded)

# Remove noise from the binary image using the opening operation
kernel = np.ones((10,10),np.uint8)
opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
#cv2.imshow('opening',opening)

# Find contours based on the denoised image
contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(len(contours))

for contour in contours:
    # Get the area of the contours
    area = cv2.contourArea(contour)
    print(area)
    
    # Check if area is between max and min values for a bullet hole. Area is usually about 1000
    if area<1500 and area>500:
        #print(area)

        # Draw the detected contour for debugging
        cv2.drawContours(img,[contour],0,(255,0,0),2)

        # Create an enclosing circle that can represent the bullet hole
        (x,y),radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)

        # Draw the enclosing circle in addition to a dot at the center
        cv2.circle(img,center,radius,(0,255,0),2)
        cv2.circle(img,center,1,(0,0,255),2)

cv2.imshow('Hole Analysis', img)
