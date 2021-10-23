#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#region Information
############################################################
## Target Analysis                                        ##
############################################################
## Copyright (c) 2021 Sigmond Kukla, All Rights Reserved  ##
############################################################
## Author: Sigmond Kukla                                  ##
## Copyright: Copyright 2021, Sigmond Kukla               ##
## The Target Analysis system does not include a license. ##
## This means that this work is under exclusive           ##
## copyright by the developer (Sigmond Kukla) alone.      ##
## Therefore, you are not permitted to copy, distribute,  ##
## or modify this work and claim it is your own.          ##
## Maintainer: Sigmond Kukla                              ##
## Contact: picoplanetdev@gmail.com (business)            ##
##          skukla61@mtlstudents.net (school)             ##
## Status: Released, active development                   ##
############################################################
#endregion

#region Import libraries
from tkinter.constants import BOTH, BOTTOM, DISABLED, HORIZONTAL, LEFT, NORMAL, NSEW, RIDGE, RIGHT, TOP, X
import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image
import os
import csv
import numpy as np
import math
import datetime
import matplotlib.pyplot as plt
import matplotlib
from configparser import ConfigParser
#endregion

# Loads an image for the left side of the target
def loadImageLeft():
    label.config(text="Loading left image...") # Update the main label

    leftCanvas.delete("all") # Clear the left canvas in case it already has an image

    imageFile = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    leftImage = cv2.imread(imageFile) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    leftCanvas.grid(row = 0, column = 0) # Refresh the canvas
    
    global leftPreview # Images must be stored globally to be show on the canvas
    leftPreview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 350), Image.ANTIALIAS)) # Store the image as a tkinter photo image and resize it
    leftCanvas.create_image(0, 0, anchor="nw", image=leftPreview) # Place the image on the canvas

    label.config(text="Right image loaded") # Update the main label

    root.geometry("550x540") # Increase the window size to accomodate the image

    cropLeft(leftImage) # Crop the image to prepare for analysis

# Loads an image for the right side of the target
def loadImageRight():
    label.config(text="Loading right image...") # Update the main label

    rightCanvas.delete("all") # Clear the right canvas in case it already has an image

    imageFile = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    rightImage = cv2.imread(imageFile) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    rightCanvas.grid(row = 0, column = 1) # Refresh the canvas
    
    global rightPreview # Images must be stored globally to be show on the canvas
    rightPreview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 350), Image.ANTIALIAS)) # Store the image as a tkinter photo image and resize it
    rightCanvas.create_image(0, 0, anchor="nw", image=rightPreview) # Place the image on the canvas

    label.config(text="Left image loaded") # Update the main label

    root.geometry("550x540") # Increase the window size to accomodate the image

    cropRight(rightImage) # Crop the image to prepare for analysis

# Loads an image taken by a smartphone camera that includes the entire target (CURRENTLY DISABLED)
def loadSingleImage():
    imageFile = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    singleImage = cv2.imread(imageFile) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    label.config(text="Single image loaded") # Update the main label

    cropSingle(singleImage) # Crop the image to prepare for analysis

# Loads an image for an Orion target
def loadImageOrion():
    label.config(text="Loading image...") # Update the main label

    orionSingleCanvas.delete("all") # Clear the orion single canvas in case it already has an image

    imageFile = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    singleImage = cv2.imread(imageFile) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    orionSingleCanvas.grid(row = 0, column = 1) # Refresh the canvas
    
    global orionPreview # Images must be stored globally to be show on the canvas
    orionPreview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 350), Image.ANTIALIAS)) # Store the image as a tkinter photo image and resize it
    orionSingleCanvas.create_image(0, 0, anchor="nw", image=orionPreview) # Place the image on the canvas

    label.config(text="Orion image loaded") # Update the main label

    root.geometry("550x540") # Increase the window size to accomodate the image

    cropOrion(singleImage) # Crop the image to prepare for analysis

# Somewhat derived from loadSingleImage (CURRENTLY DISABLED)
def loadOutdoorBull():
    imageFile = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    singleImage = cv2.imread(imageFile) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    label.config(text="Outdoor image loaded") # Update the main label

    # Perform the cropping and analysis automatically
    checkOutputDir()

    dsize = (int(singleImage.shape[1] * 0.2), int(singleImage.shape[0] * 0.2))
    resized = cv2.resize(singleImage, dsize)

    cv2.imwrite("images/output/outdoorBull.jpg", resized)

    global csvName
    csvName = "data/data-" + nameVar.get() + dayVar.get() + monthVar.get() + yearVar.get() + targetNumVar.get() + ".csv"

    analyzeOutdoorImage("images/output/outdoorBull.jpg")

# Crop image for an Orion target
def cropOrion(image):
    label.config(text="Cropping image...") # Update the main label
    checkOutputDir() # Make sure the output directory exists

    # Height and width are set once and used for all bulls
    # The height and width are determined by the size of the image multipled by a ratio,
    # allowing slight deviations in printer resolution to be ignored
    h=int((400/3507)*image.shape[0])
    w=int((400/2550)*image.shape[1])

    y=int((425/3507)*image.shape[0])
    x=int((1070/2550)*image.shape[1])
    crop1 = image[y:y+h, x:x+w]

    y=int((425/3507)*image.shape[0])
    x=int((1920/2550)*image.shape[1])
    crop2 = image[y:y+h, x:x+w]

    y=int((1175/3507)*image.shape[0])
    x=int((1920/2550)*image.shape[1])

    crop3 = image[y:y+h, x:x+w]

    y=int((1925/3507)*image.shape[0])
    x=int((1920/2550)*image.shape[1])

    crop4 = image[y:y+h, x:x+w]

    y=int((2680/3507)*image.shape[0])
    x=int((1920/2550)*image.shape[1])

    crop5 = image[y:y+h, x:x+w]

    y=int((2680/3507)*image.shape[0])
    x=int((1070/2550)*image.shape[1])

    crop6 = image[y:y+h, x:x+w]

    y=int((420/3507)*image.shape[0])
    x=int((225/2550)*image.shape[1])

    crop7 = image[y:y+h, x:x+w]

    y=int((1175/3507)*image.shape[0])
    x=int((225/2550)*image.shape[1])

    crop8 = image[y:y+h, x:x+w]

    y=int((1925/3507)*image.shape[0])
    x=int((225/2550)*image.shape[1])

    crop9 = image[y:y+h, x:x+w]

    y=int((2680/3507)*image.shape[0])
    x=int((225/2550)*image.shape[1])

    crop10 = image[y:y+h, x:x+w]

    # Save the cropped images
    cv2.imwrite("images/output/top-mid.jpg", crop1)
    cv2.imwrite("images/output/top-right.jpg", crop2)
    cv2.imwrite("images/output/upper-right.jpg", crop3)
    cv2.imwrite("images/output/lower-right.jpg", crop4)
    cv2.imwrite("images/output/bottom-right.jpg", crop5)
    cv2.imwrite("images/output/bottom-mid.jpg", crop6)
    cv2.imwrite("images/output/top-left.jpg", crop7)
    cv2.imwrite("images/output/upper-left.jpg", crop8)
    cv2.imwrite("images/output/lower-left.jpg", crop9)
    cv2.imwrite("images/output/bottom-left.jpg", crop10)

    label.config(text="Cropped image") # Update the main label

# Runs perspective transform to the image and crops it to 10 output images (CURRENTLY DISABLED)
def cropSingle(image):
    # Helper function for four_point_transform - puts points in order in a clockwise fashion with the top left point listed first
    def order_points(pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype = "float32")
        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # return the ordered coordinates
        return rect
    # Helper function for cropSingle - Calculates perspective transform for an image
    def four_point_transform(image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = order_points(pts)
        (tl, tr, br, bl) = rect
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        # return the warped image
        return warped
    # Helper function for cropSingle - Appends to list clicked points on the image
    def singleImageClicked(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            singleImageClickPosition.append((x*5,y*5))
            #print("Appended position " + str(x) + "," + str(y))

    copy = image.copy()

    label.config(text="Cropping single image...")

    checkOutputDir()

    global singleImageClickPosition
    singleImageClickPosition = []

    dsize = (int(copy.shape[1] * 0.2), int(copy.shape[0] * 0.2))
    previewImage = cv2.resize(copy, dsize)

    cv2.imshow("Single Image", previewImage)
    cv2.setMouseCallback('Single Image', singleImageClicked)
    cv2.waitKey(0)

    points = np.asarray(singleImageClickPosition, dtype = "float32")

    warped = four_point_transform(copy, points)

    dsize = 2982,3408
    resizedImage = cv2.resize(warped, dsize, interpolation = cv2.INTER_AREA)

    cv2.imwrite("images/output/resized.jpg", resizedImage)

    y=250
    x=1215
    h=540
    w=540
    crop1 = resizedImage[y:y+h, x:x+w]

    y=250
    x=2215
    h=540
    w=540
    crop2 = resizedImage[y:y+h, x:x+w]

    y=1010
    x=2215
    h=540
    w=540
    crop3 = resizedImage[y:y+h, x:x+w]

    y=1785
    x=2215
    h=540
    w=540
    crop4 = resizedImage[y:y+h, x:x+w]

    y=2550
    x=2215
    h=540
    w=540
    crop5 = resizedImage[y:y+h, x:x+w]

    y=2550
    x=1210
    h=540
    w=540
    crop6 = resizedImage[y:y+h, x:x+w]

    y=2550
    x=205
    h=540
    w=540
    crop7 = resizedImage[y:y+h, x:x+w]

    y=1785
    x=205
    h=540
    w=540
    crop8 = resizedImage[y:y+h, x:x+w]

    y=1010
    x=205
    h=540
    w=540
    crop9 = resizedImage[y:y+h, x:x+w]

    y=250
    x=205
    h=540
    w=540
    crop10 = resizedImage[y:y+h, x:x+w]

    cv2.imwrite("images/output/top-mid.jpg", crop1)
    cv2.imwrite("images/output/top-right.jpg", crop2)
    cv2.imwrite("images/output/upper-right.jpg", crop3)
    cv2.imwrite("images/output/lower-right.jpg", crop4)
    cv2.imwrite("images/output/bottom-right.jpg", crop5)
    cv2.imwrite("images/output/bottom-mid.jpg", crop6)
    cv2.imwrite("images/output/bottom-left.jpg", crop7)
    cv2.imwrite("images/output/lower-left.jpg", crop8)
    cv2.imwrite("images/output/upper-left.jpg", crop9)
    cv2.imwrite("images/output/top-left.jpg", crop10)

# Crop image for right side of the target and start analysis process
def cropRight(image):
    label.config(text="Cropping right image...") # Update main label

    checkOutputDir() # Make sure that output directory exists

    #region Crop the image
    # if dpiVar.get() == 2:
    #     dsize = (2550, 3507)
    #     image = cv2.resize(image, dsize, interpolation = cv2.INTER_LINEAR)

    y=int((275/3507)*image.shape[0])
    x=int((720/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop1 = image[y:y+h, x:x+w]

    y=int((275/3507)*image.shape[0])
    x=int((1760/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop2 = image[y:y+h, x:x+w]

    y=int((1070/3507)*image.shape[0])
    x=int((1760/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop3 = image[y:y+h, x:x+w]

    y=int((1880/3507)*image.shape[0])
    x=int((1760/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop4 = image[y:y+h, x:x+w]

    y=int((2680/3507)*image.shape[0])
    x=int((1760/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop5 = image[y:y+h, x:x+w]

    y=int((2680/3507)*image.shape[0])
    x=int((720/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop6 = image[y:y+h, x:x+w]
    #endregion

    # Save the cropped sections
    cv2.imwrite("images/output/top-mid.jpg", crop1)
    cv2.imwrite("images/output/top-right.jpg", crop2)
    cv2.imwrite("images/output/upper-right.jpg", crop3)
    cv2.imwrite("images/output/lower-right.jpg", crop4)
    cv2.imwrite("images/output/bottom-right.jpg", crop5)
    cv2.imwrite("images/output/bottom-mid.jpg", crop6)

    label.config(text="Cropped right image") # Update the main label

# Crop image for left side of the target and start analysis process
def cropLeft(image):
    label.config(text="Cropping left image...") # Update main label

    checkOutputDir() # Make sure that output directory exists

    # Flips the image vertically and horizontally before cropping
    verticalFlippedImage = cv2.flip(image, -1)
    cv2.imwrite("images/output/vertical-flipped.jpg", verticalFlippedImage)

    #region Crop each image
    # if dpiVar.get() == 2:
    #     dsize = (2550, 3507)
    #     verticalFlippedImage = cv2.resize(verticalFlippedImage, dsize, interpolation = cv2.INTER_LINEAR)

    y=int((240/3507)*image.shape[0])
    x=int((185/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop2 = verticalFlippedImage[y:y+h, x:x+w]

    y=int((1040/3507)*image.shape[0])
    x=int((185/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop3 = verticalFlippedImage[y:y+h, x:x+w]

    y=int((1840/3507)*image.shape[0])
    x=int((185/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop4 = verticalFlippedImage[y:y+h, x:x+w]

    y=int((2645/3507)*image.shape[0])
    x=int((185/2550)*image.shape[1])
    h=int((580/3507)*image.shape[0])
    w=int((580/2550)*image.shape[1])
    crop5 = verticalFlippedImage[y:y+h, x:x+w]
    #endregion

    # Save the cropped sections
    cv2.imwrite("images/output/top-left.jpg", crop2)
    cv2.imwrite("images/output/upper-left.jpg", crop3)
    cv2.imwrite("images/output/lower-left.jpg", crop4)
    cv2.imwrite("images/output/bottom-left.jpg", crop5)

    label.config(text="Cropped image") # Update the main label

# Runs the analyzeImage function for every image that has been cropped out
def analyzeTarget(type):
    label.config(text="Analyzing target...") # Update main label

    # Create and store a name for the target output file
    global csvName
    csvName = "data/data-" + nameVar.get() + dayVar.get() + monthVar.get() + yearVar.get() + targetNumVar.get() + ".csv"

    # If the CSV file already exists, delete it
    if os.path.exists(str(os.getcwd()) +"/" + csvName):
        print("CSV already exists. Removing old version")
        os.remove(os.getcwd() + "/" + csvName)
    
    # Create the CSV file template
    with open(csvName, 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Image", "Dropped", "X", "HoleX", "HoleY", "Distance", "HoleRatioX", "HoleRatioY"])
        csvfile.close()

    # Analyze each cropped image
    if type == "nra":
        analyzeImage("images/output/top-mid.jpg")
        analyzeImage("images/output/top-right.jpg")
        analyzeImage("images/output/upper-right.jpg")
        analyzeImage("images/output/lower-right.jpg")
        analyzeImage("images/output/bottom-right.jpg")
        analyzeImage("images/output/bottom-mid.jpg")
        analyzeImage("images/output/bottom-left.jpg")
        analyzeImage("images/output/lower-left.jpg")
        analyzeImage("images/output/upper-left.jpg")
        analyzeImage("images/output/top-left.jpg")
    elif type == "orion":
        analyzeOrionImage("images/output/top-mid.jpg")
        analyzeOrionImage("images/output/top-right.jpg")
        analyzeOrionImage("images/output/upper-right.jpg")
        analyzeOrionImage("images/output/lower-right.jpg")
        analyzeOrionImage("images/output/bottom-right.jpg")
        analyzeOrionImage("images/output/bottom-mid.jpg")
        analyzeOrionImage("images/output/bottom-left.jpg")
        analyzeOrionImage("images/output/lower-left.jpg")
        analyzeOrionImage("images/output/upper-left.jpg")
        analyzeOrionImage("images/output/top-left.jpg")
    elif type == "orion-nrascoring":
        analyzeOrionImageNRAScoring("images/output/top-mid.jpg")
        analyzeOrionImageNRAScoring("images/output/top-right.jpg")
        analyzeOrionImageNRAScoring("images/output/upper-right.jpg")
        analyzeOrionImageNRAScoring("images/output/lower-right.jpg")
        analyzeOrionImageNRAScoring("images/output/bottom-right.jpg")
        analyzeOrionImageNRAScoring("images/output/bottom-mid.jpg")
        analyzeOrionImageNRAScoring("images/output/bottom-left.jpg")
        analyzeOrionImageNRAScoring("images/output/lower-left.jpg")
        analyzeOrionImageNRAScoring("images/output/upper-left.jpg")
        analyzeOrionImageNRAScoring("images/output/top-left.jpg")
    # Create variables to store the score and x count
    global score, xCount
    score = 100
    xCount = 0

    # Update the score and x count from the saved target CSV file
    with open(csvName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                score -= int(row[1])
                xCount += int(row[2])
            line_count += 1
    
    # If a global data CSV doesn't exist, create it
    if not os.path.exists(str(os.getcwd()) +"/data/data.csv"):
        createCSV()

    # Save the target's basic info to the global data CSV
    with open("data/data.csv", 'a', newline="") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([nameVar.get(), dayVar.get() + " " + monthVar.get() + " " + yearVar.get(), targetNumVar.get(), score, xCount])
                csvfile.close()

    label.config(text="Done") # Update main label

    # Enable the "Show Output" menu item
    # If any menu items have been added above this, make sure to recount them to get the correct index
    # Counting starts at zero.
    filemenu.entryconfigure(1, state=NORMAL)

    
    if individualOutputTypeVar.get() == "tkinter":
        # If the user uses the new analysis window, open it
        # There is no need to show the output here, instead, if it is needed,
        # it will be shown when the Finish button is pressed in the analysis window
        openAnalysisWindow()
    elif showOutputWhenFinishedVar.get():
        showOutput() # Otherwise, show the output now that analysis has finished

# Shows the results of the program in a separate window and provides buttons for opening CSV files
def showOutput():
    label.config(text="Showing output") # Update main label

    #region Create window
    showOutputWindow = tk.Toplevel(root)
    showOutputWindow.minsize(525,750)
    showOutputWindow.geometry("525x750")
    showOutputWindow.tk.call('wm', 'iconphoto', showOutputWindow._w, tk.PhotoImage(file='assets/icon.png'))
    showOutputWindow.title("Target Analysis")
    #endregion

    #region Create frames
    # Only buttons and labels go in the top frame
    outputTopFrame = ttk.Frame(showOutputWindow)
    outputTopFrame.pack(side=TOP, fill=X, expand=True, pady=10)

    # Target images are shown in the bottom frame
    outputBottomFrame = ttk.Frame(showOutputWindow)
    outputBottomFrame.pack(side=TOP, fill=X)
    #endregion

    #region Create buttons and info at the top
    # Create a button to open the target CSV file
    openTargetCSVButton = ttk.Button(outputTopFrame, text="Open target CSV", command=lambda: openFile('"' + os.getcwd() + "/" + csvName + '"'))
    openTargetCSVButton.grid(row=0, column=0)
    outputTopFrame.grid_columnconfigure(0, weight=1)
    
    # Create a label for the score
    scoreLabel = ttk.Label(outputTopFrame, text=str(score) + "-" + str(xCount) + "X", font='bold')
    scoreLabel.grid(row=0, column=1)
    outputTopFrame.grid_columnconfigure(1, weight=1)

    # Create a button to open the global data CSV file
    openDataCSVButton = ttk.Button(outputTopFrame, text="Open data CSV", command=lambda: openFile('"' + os.getcwd() + "/data/data.csv" + '"'))
    openDataCSVButton.grid(row=0, column=2)
    outputTopFrame.grid_columnconfigure(2, weight=1)
    #endregion

    #region Create canvases and images for each bull
    topLeftCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    topLeftCanvas.grid(row = 0, column = 0)

    global topLeftOutput
    topLeftOutput = ImageTk.PhotoImage(Image.open("images/output/top-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    topLeftCanvas.create_image(0, 0, anchor="nw", image=topLeftOutput)

    upperLeftCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    upperLeftCanvas.grid(row = 1, column = 0)

    global upperLeftOutput
    upperLeftOutput = ImageTk.PhotoImage(Image.open("images/output/upper-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    upperLeftCanvas.create_image(0, 0, anchor="nw", image=upperLeftOutput)

    lowerLeftCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    lowerLeftCanvas.grid(row = 2, column = 0)

    global lowerLeftOutput
    lowerLeftOutput = ImageTk.PhotoImage(Image.open("images/output/lower-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    lowerLeftCanvas.create_image(0, 0, anchor="nw", image=lowerLeftOutput)

    bottomLeftCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    bottomLeftCanvas.grid(row = 3, column = 0)

    global bottomLeftOutput
    bottomLeftOutput = ImageTk.PhotoImage(Image.open("images/output/bottom-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    bottomLeftCanvas.create_image(0, 0, anchor="nw", image=bottomLeftOutput)

    topMidCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    topMidCanvas.grid(row = 0, column = 1)

    global topMidOutput
    topMidOutput = ImageTk.PhotoImage(Image.open("images/output/top-mid.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    topMidCanvas.create_image(0, 0, anchor="nw", image=topMidOutput)

    bottomMidCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    bottomMidCanvas.grid(row = 3, column = 1)

    global bottomMidOutput
    bottomMidOutput = ImageTk.PhotoImage(Image.open("images/output/bottom-mid.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    bottomMidCanvas.create_image(0, 0, anchor="nw", image=bottomMidOutput)

    topRightCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    topRightCanvas.grid(row = 0, column = 2)

    global topRightOutput
    topRightOutput = ImageTk.PhotoImage(Image.open("images/output/top-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    topRightCanvas.create_image(0, 0, anchor="nw", image=topRightOutput)

    upperRightCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    upperRightCanvas.grid(row = 1, column = 2)

    global upperRightOutput
    upperRightOutput = ImageTk.PhotoImage(Image.open("images/output/upper-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    upperRightCanvas.create_image(0, 0, anchor="nw", image=upperRightOutput)

    lowerRightCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    lowerRightCanvas.grid(row = 2, column = 2)

    global lowerRightOutput
    lowerRightOutput = ImageTk.PhotoImage(Image.open("images/output/lower-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    lowerRightCanvas.create_image(0, 0, anchor="nw", image=lowerRightOutput)

    bottomRightCanvas = tk.Canvas(outputBottomFrame, width=170,height=170)
    bottomRightCanvas.grid(row = 3, column = 2)

    global bottomRightOutput
    bottomRightOutput = ImageTk.PhotoImage(Image.open("images/output/bottom-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    bottomRightCanvas.create_image(0, 0, anchor="nw", image=bottomRightOutput)
    #endregion

# Open the working folder in Explorer
# TODO Make this work on any operating system
# I a just going to display a warning message for now that should only be visible if the function fails on non Windows systems
def showFolder():
    label.config(text="Opening folder... ONLY WORKS ON WINDOWS")
    os.system("explorer " + '"' + os.getcwd() + '"') # Run a system command to open the folder using Explorer (Windows only)
    label.config(text="Working directory opened in Explorer") # Update the main label

# Open documentation with associated viewer
def openFile(file):
    label.config(text="Opening file " + str(file)) # Update the main label
    os.system(file) # Run a system command to open the file using the default viewer (should work on any operating system)

# Create CSV file set up for the global data csv
def createCSV():
    # Open the CSV file
    with open('data/data.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) # Create a filewriter
        filewriter.writerow(['Name', 'Date', 'Target Number', 'Score','X']) # Write the header row
        csvfile.close() # Close the file
    label.config(text="Created CSV data file") # Update the main label

# Opens and analyzes all files in a folder (more complex because it has to distinguish between left and right images)
def openFolder():
    # Temporarily save the showOutputWhenFinishedVar to restore after the function is done
    # Then set it to false so that the output is not shown (because for large folders it could take a while)
    showOutputWhenFinishedBackup = showOutputWhenFinishedVar.get()
    showOutputWhenFinishedVar.set(False)

    label.config(text="Opening folder") # Update the main label

    folder = filedialog.askdirectory() # Get the folder to open
    fileNum = 0 # Keep track of how many files have been opened
    
    # os.listdir() returns a list of all files in the folder
    for file in os.listdir(folder):
        # Ignore files that are not images
        if file.endswith(".jpeg") or file.endswith(".jpg"):
            path = os.getcwd() + "/images/" + file # Get the path to the file
            setInfoFromFile(file) # Set the info from the file (correct naming is important for this operation)
            fileImage = cv2.imread(path) # Open the image

            # Check if the image is a left or right image
            if "left" in file:
                cropLeft(fileImage)
            elif "right" in file:
                cropRight(fileImage)
            
            fileNum += 1 # Increment the file number

            # For every two files opened, analyze the target
            # Again, it is imperative that the naming convention is correct
            # See the README for more information
            if fileNum == 2:
                analyzeTarget("nra")
                fileNum = 0 # Reset the file number and continue
    
    showOutputWhenFinishedVar.set(showOutputWhenFinishedBackup) # Revert the showOutputWhenFinishedVar to its original value

# Opens and analyzes all files in a folder
def openFolderOrion():
    # Temporarily save the showOutputWhenFinishedVar to restore after the function is done
    # Then set it to false so that the output is not shown (because for large folders it could take a while)
    showOutputWhenFinishedBackup = showOutputWhenFinishedVar.get()
    showOutputWhenFinishedVar.set(False)

    label.config(text="Opening folder") # Update the main label

    folder = filedialog.askdirectory() # Get the folder to open
    
    # os.listdir() returns a list of all files in the folder
    for file in os.listdir(folder):
        # Ignore files that are not images
        if file.endswith(".jpeg") or file.endswith(".jpg"):
            path = folder + "/" + file # Get the path to the file
            setInfoFromFile(file) # Set the info from the file (correct naming is important for this operation)
            fileImage = cv2.imread(path) # Open the image for OpenCV
            cropOrion(fileImage) # Crop the image
            analyzeTarget("orion") # Analyze the target
    
    showOutputWhenFinishedVar.set(showOutputWhenFinishedBackup) # Revert the showOutputWhenFinishedVar to its original value

# Allows viewing of trends from existing data files
def showTrends():
    label.config(text="Showing trends window") # Update the main label

    #region Create window
    trendsWindow = tk.Toplevel(root)
    trendsWindow.minsize(250,100)
    trendsWindow.geometry("250x100")
    trendsWindow.tk.call('wm', 'iconphoto', trendsWindow._w, tk.PhotoImage(file='assets/icon.png'))
    trendsWindow.title("Target Analysis")
    #endregion

    def showMostMissed():
        bulls = [0,0,0,0,0,0,0,0,0,0] # Create a list of bulls to keep track of the most missed targets

        folder = filedialog.askdirectory() # Get the folder to open
        # os.listdir() returns a list of all files in the folder
        for file in os.listdir(folder):
            # Ignore files that are not target CSVs
            if not "data.csv" in file and not ".gitkeep" in file:
                # Open the CSV file
                with open("data/" + file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',') # Create a CSV reader
                    line_count = 0 # Keep track of the line number
                    for row in csv_reader:
                        # Ignore the header row and rows beyond ten (if there are more than ten rows, there is a problem)
                        if line_count != 0 and line_count <= 10:
                            bulls[line_count-1] += int(row[1]) # Add the score from each bull to the bulls list
                        line_count += 1 # Increment the line number
                    csv_file.close() # Close the file

        # Create a frame to display the data
        frame = ttk.Frame(trendsWindow)
        frame.pack(pady=5)

        trendsWindow.geometry("250x300") # Resize the window to accomodate the data display

        # Create a label for a header
        mostMissedLabel = ttk.Label(frame, text="Most missed is highest number")
        mostMissedLabel.grid(row=0, column=0, columnspan=3)

        #region Create a label for each bull
        label1 = ttk.Label(frame, text=str(bulls[0]), borderwidth=2, relief=RIDGE, padding=10)
        label1.grid(row=1,column=0)

        label2 = ttk.Label(frame, text=str(bulls[1]), borderwidth=2, relief=RIDGE, padding=10)
        label2.grid(row=2,column=0)

        label3 = ttk.Label(frame, text=str(bulls[2]), borderwidth=2, relief=RIDGE, padding=10)
        label3.grid(row=3,column=0)

        label4 = ttk.Label(frame, text=str(bulls[3]), borderwidth=2, relief=RIDGE, padding=10)
        label4.grid(row=4,column=0)

        label5 = ttk.Label(frame, text=str(bulls[4]), borderwidth=2, relief=RIDGE, padding=10)
        label5.grid(row=1,column=1)

        label6 = ttk.Label(frame, text=str(bulls[5]), borderwidth=2, relief=RIDGE, padding=10)
        label6.grid(row=1,column=2)

        label7 = ttk.Label(frame, text=str(bulls[6]), borderwidth=2, relief=RIDGE, padding=10)
        label7.grid(row=2,column=2)

        label8 = ttk.Label(frame, text=str(bulls[7]), borderwidth=2, relief=RIDGE, padding=10)
        label8.grid(row=3,column=2)

        label9 = ttk.Label(frame, text=str(bulls[8]), borderwidth=2, relief=RIDGE, padding=10)
        label9.grid(row=4,column=2)

        label10 = ttk.Label(frame, text=str(bulls[9]), borderwidth=2, relief=RIDGE, padding=10)
        label10.grid(row=4,column=1)
        #endregion

    def showTrendGraph():
        dataCSV = filedialog.askopenfilename() # Get the CSV file to open (this can be a backup to accomodate for multiple shooters)

        # Create some arrays for relevant data
        dates = []
        scores = []
        xCount = []

        # Open the CSV file
        with open(dataCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',') # Create a CSV reader
            line_count = 0 # Keep track of the line number
            for row in csv_reader:
                # Ignore the header row
                if line_count != 0:
                    dates.append(row[1]) # The dates are in the second column
                    scores.append(row[3]) # The scores are in the fourth column
                    xCount.append(row[4]) # The xCount are in the fifth column
                line_count += 1 # Increment the line number
            csv_file.close() # Close the file
        
        # Zip the data together, with the dates first
        # Then sort the data using the date as the key
        sortedZipped = sorted(zip(dates,scores,xCount), key=lambda date: datetime.datetime.strptime(date[0], "%d %B %Y"))

        # Unpack the data back into separate lists
        dates,scores,xCount = map(list,zip(*sortedZipped))

        # Convert the scores and xCount back
        scores = list(map(int, scores))
        xCount = list(map(int, xCount))

        # Create some matplotlib plots to show data
        fig,axs = plt.subplots(2)

        # Plot the scores and xCount on separate graphs
        axs[0].plot(dates,scores, marker='o', color = 'blue')
        axs[1].plot(dates,xCount, marker='x', color = 'orange')

        # Create a label for each point for the scores graph
        for x,y in zip(dates,scores):
            label = y
            axs[0].annotate(label, # this is the text
                        (x,y), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(-15,0), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center

        # Create a label for each point for the xCount graph
        for x,y in zip(dates,xCount):
            label = str(y) + "X"
            axs[1].annotate(label, # this is the text
                        (x,y), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(-15,0), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center

        # Convert the dates to numbers
        datesNum = matplotlib.dates.datestr2num(dates)

        # Create a trendline for the scores graph
        z = np.polyfit(datesNum, scores, 1)
        p = np.poly1d(z)

        # Plot the trendline on the scores graph
        axs[0].plot(dates,p(datesNum), 'r--')

        # Set the x axis user-facing label to Date for both graphs
        axs[0].set_xlabel('Date')
        axs[1].set_xlabel('Date')
        
        # Set the y axis user-facing label to Score and X Count for each graph respectively
        axs[0].set_ylabel('Score')
        axs[1].set_ylabel('X Count')

        # Angle the dates at a 40 degree angle for both graphs
        axs[0].xaxis.set_tick_params(rotation=40)
        axs[1].xaxis.set_tick_params(rotation=40)

        # Add some space between the graphs
        plt.subplots_adjust(hspace=0.8)

        # Show the plots
        plt.show()

    # Create a button to load a folder of data (for one shooter) to show which bull has the highest value (thus the most missed)
    loadFolderButton = ttk.Button(trendsWindow, text="Load Folder (for most missed)", command=showMostMissed)
    loadFolderButton.pack(padx=10, pady=10)

    # Create a button to load a global data CSV (for one shooter) to show improvement over time
    loadCSVButton = ttk.Button(trendsWindow, text="Load CSV (for graph)", command=showTrendGraph)
    loadCSVButton.pack(padx=10, pady=0)

# Sets file options by parsing a correctly-named target         
def setInfoFromFile(file):
    filename = os.path.basename(file) # Get the filename alone in case it is given a full path

    dayVar.set(filename[0:2]) # Set the day

    yearVar.set(filename[5:9]) # Set the year

    month = filename[2:5] # Get the month

    # Create a dictionary to convert the 3 letter month month to a full name
    months = {
        'jan': 'January', 
        'feb': 'February', 
        'mar': 'March', 
        'apr': 'April', 
        'may': 'May', 
        'jun': 'June', 
        'jul': 'July', 
        'aug': 'August', 
        'sep': 'September', 
        'oct': 'October', 
        'nov': 'November', 
        'dec': 'December'}
    
    # Replace the 3 letter month with the full name using the dictionary
    for short, full in months.items():
        month = month.replace(short, full)

    monthVar.set(month) # Set the month

    targetNumVar.set(filename[-6]) # Set the target number

    # The final section of the filename can be any length and it is "left" or "right" for NRA A-17 targets
    # However, Orion targets use only one scan so that space can hold the shooter's name
    # This is a kind of hacky way to determine if this is an Orion target
    if tabControl.tab(tabControl.select(), "text") == "NRA/USAS-50":
        nameVar.set(filename[9:-6])

    # Update the main label
    label.config(text="Set date to: " + monthVar.get() + " " + dayVar.get() + " " + yearVar.get() + " with target number " + targetNumVar.get())

# Sets file options from today's date
def setInfoFromToday():
    today = datetime.datetime.now() # Get today's date

    monthVar.set(today.strftime("%B")) # Set the month from the date
    dayVar.set(today.strftime("%d")) # Set the day from the date
    yearVar.set(today.strftime("%Y")) # Set the year from the date

    targetNumVar.set("1") # Default the target number to 1

    # Update the main label
    label.config(text="Set date to: " + monthVar.get() + " " + dayVar.get() + " " + yearVar.get() + " with target number " + targetNumVar.get())

# Delete all files in the data folder
def clearData():
    path = str(os.getcwd()) + "/data" # Set the path to the data folder
    # List all the files in the folder
    for file in os.listdir(path):
        # If the file is a CSV (meaning that it was probably generated by the software, delete it)
        if file.endswith(".csv"):
            os.remove(path + "\\" + file)
    
    path = str(os.getcwd()) + "/images/output" # Set the path to the images/output folder
    # List all the files in the folder
    for file in os.listdir(path):
        # If the file is a JPG (meaning that it was probably generated by the software, delete it)
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            os.remove(path + "/" + file)

    label.config(text="/data and /images/output directories cleared") # Update the main label

# Create a settings window
def openSettings():
    # If the settings window is going to be closed, save the changes and destroy the window
    def onCloseSettings():
        updateConfig()
        settingsWindow.destroy()

    # Update the settings using the config-backup.ini file, which should never be changed
    def revertSettings():
        updateSettingsFromConfigFile("config-backup.ini")
        updateConfig()

    label.config(text="Showing settings window") # Update the main label

    #region Create settings window
    settingsWindow = tk.Toplevel(root)
    settingsWindow.title("Target Analysis")
    settingsWindow.minsize(width=500, height=640)
    settingsWindow.geometry("500x640")
    settingsWindow.tk.call('wm', 'iconphoto', settingsWindow._w, tk.PhotoImage(file='assets/icon.png'))
    #endregion

    #region Create frames
    # Each global setting has its own frame
    settingsTopFrame = ttk.Frame(settingsWindow)
    settingsTopFrame.pack(side=TOP, expand=False, pady=5, fill=X)

    settingsGlobalLabelFrame = ttk.Frame(settingsWindow)
    settingsGlobalLabelFrame.pack(side=TOP, fill=X)

    settingsDpiFrame = ttk.Frame(settingsWindow)
    settingsDpiFrame.pack(side=TOP, fill=X, padx=5)

    settingsShowOutputFrame = ttk.Frame(settingsWindow)
    settingsShowOutputFrame.pack(side=TOP, fill=X, padx=5)

    settingsIndivdualOutputFrame = ttk.Frame(settingsWindow)
    settingsIndivdualOutputFrame.pack(side=TOP, fill=X, padx=5)

    settingsDarkModeFrame = ttk.Frame(settingsWindow)
    settingsDarkModeFrame.pack(side=TOP, fill=X, padx=5)

    settingsGlobalSeparator = ttk.Separator(settingsWindow, orient=HORIZONTAL)
    settingsGlobalSeparator.pack(side=TOP, fill=X, pady=5)

    settingsBottomFrame = ttk.Frame(settingsWindow)
    settingsBottomFrame.pack(side=TOP, fill=X)

    settingsButtonsFrame = ttk.Frame(settingsWindow)
    settingsButtonsFrame.pack(side=BOTTOM, fill=X)

    # Notebook allows for a tabbed view
    settingsTabControl = ttk.Notebook(settingsBottomFrame)

    settingstab1NRAA17 = ttk.Frame(settingsTabControl)
    settingstab2orion = ttk.Frame(settingsTabControl)
    settingstab3orionDPI2 = ttk.Frame(settingsTabControl)

    settingsTabControl.add(settingstab1NRAA17, text ='NRA A-17')
    settingsTabControl.add(settingstab2orion, text ='NRA/USAS-50 Orion 300dpi')
    settingsTabControl.add(settingstab3orionDPI2, text ='NRA/USAS-50 Orion 600dpi')

    settingsTabControl.pack(side=TOP, fill=X, padx=10, pady=5)

    saveSeparator = ttk.Separator(settingsButtonsFrame, orient=HORIZONTAL)
    saveSeparator.pack(side=TOP, fill=X)

    revertButton = ttk.Button(settingsButtonsFrame, text="Revert settings to default", command=revertSettings)
    revertButton.pack(side=LEFT, pady=5, padx=5)

    saveButton = ttk.Button(settingsButtonsFrame, text="Save Settings", command=updateConfig)
    saveButton.pack(side=RIGHT, pady=5, padx=5)
    #endregion

    #region Create top label
    # Header label
    settingsLabel1 = ttk.Label(settingsTopFrame, text="Settings", font='bold')
    settingsLabel1.pack(side=TOP)
    # Warning label
    settingsLabel2 = ttk.Label(settingsTopFrame, text="⚠️ Change these only if the software does not work properly ⚠️")
    settingsLabel2.pack(side=TOP)
    # Separator
    labelSeparator = ttk.Separator(settingsTopFrame, orient=HORIZONTAL)
    labelSeparator.pack(side=TOP, fill=X, pady=(5, 0))
    #endregion

    #region Create top widgets
    # Global settings label
    settingsLabel1 = ttk.Label(settingsGlobalLabelFrame, text="Global settings", font = 'bold')
    settingsLabel1.pack()

    # 300dpi / 600dpi selection buttons
    dpiButton300 = ttk.Radiobutton(settingsDpiFrame, text="300 dpi scanner", variable=dpiVar, value=1)
    dpiButton300.grid(row=1, column=0)
    dpiButton600 = ttk.Radiobutton(settingsDpiFrame, text="600 dpi scanner", variable=dpiVar, value=2)
    dpiButton600.grid(row=1, column=1)

    # Show output when finished switch
    global showOutputWhenFinishedVar
    showOutputWhenFinishedCheckButtonSettings = ttk.Checkbutton(settingsShowOutputFrame, text='Show output when finished', style='Switch.TCheckbutton', variable=showOutputWhenFinishedVar, onvalue=True, offvalue=False)
    showOutputWhenFinishedCheckButtonSettings.grid(column=0, row=0)

    # Use new analysis display switch (tkinter version)
    global individualOutputTypeVar
    individualOutputTypeCheckButtonSettings = ttk.Checkbutton(settingsIndivdualOutputFrame, text='Use new analysis display', style='Switch.TCheckbutton', variable=individualOutputTypeVar, onvalue="tkinter", offvalue="legacy")
    individualOutputTypeCheckButtonSettings.grid(column=0, row=0)

    # Dark mode switch
    # TODO: Figure out why dark mode makes labels more padded
    global darkModeVar
    darkModeCheckbutton = ttk.Checkbutton(settingsDarkModeFrame, text='Use dark theme', style='Switch.TCheckbutton', variable=darkModeVar, onvalue=True, offvalue=False, command=switchDarkMode)
    darkModeCheckbutton.grid(column=0, row=0)
    #endregion

    #region Create NRA A-17 widgets
    # Create a header label
    settingsLabel2 = ttk.Label(settingstab1NRAA17, text="NRA A-17 settings" , font='bold')
    settingsLabel2.grid(row=0, column=0, columnspan=2)

    # The settings should be self explanatory
    # But if you aren't sure, check the **Tuning Overview** in README.md
    nraKernalSizeLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Kernel Size")
    nraKernalSizeLabel.grid(row=1, column=0)
    nraKernalSizeEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraKernalSize)
    nraKernalSizeEntry.grid(row=1, column=1)

    nraParam1Label = ttk.Label(settingstab1NRAA17, text="NRA A-17 Param 1")
    nraParam1Label.grid(row=2, column=0)
    nraParam1Entry = ttk.Entry(settingstab1NRAA17, textvariable=nraParam1)
    nraParam1Entry.grid(row=2, column=1)

    nraParam2Label = ttk.Label(settingstab1NRAA17, text="NRA A-17 Param 2")
    nraParam2Label.grid(row=3, column=0)
    nraParam2Entry = ttk.Entry(settingstab1NRAA17, textvariable=nraParam2)
    nraParam2Entry.grid(row=3, column=1)

    nraMinRadiusLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Min Circle Radius")
    nraMinRadiusLabel.grid(row=4, column=0)
    nraMinRadiusEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraMinRadius)
    nraMinRadiusEntry.grid(row=4, column=1)

    nraThreshMinLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Thresh Min")
    nraThreshMinLabel.grid(row=5, column=0)
    nraThreshMinEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraThreshMin)
    nraThreshMinEntry.grid(row=5, column=1)

    nraThreshMaxLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Thresh Max")
    nraThreshMaxLabel.grid(row=6, column=0)
    nraThreshMaxEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraThreshMax)
    nraThreshMaxEntry.grid(row=6, column=1)

    nraMorphologyOpeningKernelSizeLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Morph Kernal Size")
    nraMorphologyOpeningKernelSizeLabel.grid(row=7, column=0)
    nraMorphologyOpeningKernelSizeEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraMorphologyOpeningKernelSize)
    nraMorphologyOpeningKernelSizeEntry.grid(row=7, column=1)

    nraMinContourAreaLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Min cnt area")
    nraMinContourAreaLabel.grid(row=8, column=0)
    nraMinContourAreaEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraMinContourArea)
    nraMinContourAreaEntry.grid(row=8, column=1)

    nraMaxContourAreaLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Max cnt area")
    nraMaxContourAreaLabel.grid(row=9, column=0)
    nraMaxContourAreaEntry = ttk.Entry(settingstab1NRAA17, textvariable=nraMaxContourArea)
    nraMaxContourAreaEntry.grid(row=9, column=1)

    nramaxHoleRadiusLabel = ttk.Label(settingstab1NRAA17, text="NRA A-17 Max hole radius")
    nramaxHoleRadiusLabel.grid(row=10, column=0)
    nramaxHoleRadiusEntry = ttk.Entry(settingstab1NRAA17, textvariable=nramaxHoleRadius)
    nramaxHoleRadiusEntry.grid(row=10, column=1)
    #endregion

    #region Create Orion widgets
    # Create a header label
    settingsLabel1 = ttk.Label(settingstab2orion, text="Orion settings (300dpi)" , font='bold')
    settingsLabel1.grid(row=0, column=0, columnspan=2)

    # Create a header label for the Orion 600dpi settigs
    settingsLabelOrion600 = ttk.Label(settingstab3orionDPI2, text="Orion settings (600dpi)" , font='bold')
    settingsLabelOrion600.grid(row=0, column=0, columnspan=2)

    # The settings should be self explanatory
    # But if you aren't sure, check the **Tuning Overview** in README.md
    # Settings below include both 300dpi (dpi1) and 600dpi (dpi2) settings
    # They are simply sorted into either settingstab2orion (dpi1) or settingstab3orionDPI2 (dpi2)

    orionKernelSizeDpi1Label = ttk.Label(settingstab2orion, text="Orion Kernel Size dpi 1")
    orionKernelSizeDpi1Label.grid(row=1, column=0)
    orionKernelSizeDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionKernelSizeDpi1)
    orionKernelSizeDpi1Entry.grid(row=1, column=1)

    orionKernelSizeDpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion Kernel Size dpi 2")
    orionKernelSizeDpi2Label.grid(row=2, column=0)
    orionKernelSizeDpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionKernelSizeDpi2)
    orionKernelSizeDpi2Entry.grid(row=2, column=1)

    orionParam1Dpi1Label = ttk.Label(settingstab2orion, text="Orion Param1 dpi 1")
    orionParam1Dpi1Label.grid(row=3, column=0)
    orionParam1Dpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionParam1Dpi1)
    orionParam1Dpi1Entry.grid(row=3, column=1)

    orionParam2Dpi1Label = ttk.Label(settingstab2orion, text="Orion Param2 dpi 1")
    orionParam2Dpi1Label.grid(row=4, column=0)
    orionParam2Dpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionParam2Dpi1)
    orionParam2Dpi1Entry.grid(row=4, column=1)

    orionParam1Dpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion Param1 dpi 2")
    orionParam1Dpi2Label.grid(row=5, column=0)
    orionParam1Dpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionParam1Dpi2)
    orionParam1Dpi2Entry.grid(row=5, column=1)

    orionParam2Dpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion Param2 dpi 2")
    orionParam2Dpi2Label.grid(row=6, column=0)
    orionParam2Dpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionParam2Dpi2)
    orionParam2Dpi2Entry.grid(row=6, column=1)

    orionMinRadiusDpi1Label = ttk.Label(settingstab2orion, text="Orion MinRadius dpi 1")
    orionMinRadiusDpi1Label.grid(row=7, column=0)
    orionMinRadiusDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionMinRadiusDpi1)
    orionMinRadiusDpi1Entry.grid(row=7, column=1)

    orionMinRadiusDpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion MinRadius dpi 2")
    orionMinRadiusDpi2Label.grid(row=8, column=0)
    orionMinRadiusDpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionMinRadiusDpi2)
    orionMinRadiusDpi2Entry.grid(row=8, column=1)

    orionThreshMinLabel = ttk.Label(settingstab2orion, text="Orion thresh min")
    orionThreshMinLabel.grid(row=9, column=0)
    orionThreshMinEntry = ttk.Entry(settingstab2orion, textvariable=orionThreshMin)
    orionThreshMinEntry.grid(row=9, column=1)

    orionThreshMaxLabel = ttk.Label(settingstab2orion, text="Orion thresh max")
    orionThreshMaxLabel.grid(row=10, column=0)
    orionThreshMaxEntry = ttk.Entry(settingstab2orion, textvariable=orionThreshMax)
    orionThreshMaxEntry.grid(row=10, column=1)

    orionThreshMinLabel = ttk.Label(settingstab3orionDPI2, text="Orion thresh min")
    orionThreshMinLabel.grid(row=9, column=0)
    orionThreshMinEntry = ttk.Entry(settingstab3orionDPI2, textvariable=orionThreshMin)
    orionThreshMinEntry.grid(row=9, column=1)

    orionThreshMaxLabel = ttk.Label(settingstab3orionDPI2, text="Orion thresh max")
    orionThreshMaxLabel.grid(row=10, column=0)
    orionThreshMaxEntry = ttk.Entry(settingstab3orionDPI2, textvariable=orionThreshMax)
    orionThreshMaxEntry.grid(row=10, column=1)

    orionMinContourAreaDpi1Label = ttk.Label(settingstab2orion, text="Orion min cnt area dpi 1")
    orionMinContourAreaDpi1Label.grid(row=11, column=0)
    orionMinContourAreaDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionMinContourAreaDpi1)
    orionMinContourAreaDpi1Entry.grid(row=11, column=1)

    orionMaxContourAreaDpi1Label = ttk.Label(settingstab2orion, text="Orion max cnt area dpi 1")
    orionMaxContourAreaDpi1Label.grid(row=12, column=0)
    orionMaxContourAreaDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionMaxContourAreaDpi1)
    orionMaxContourAreaDpi1Entry.grid(row=12, column=1)

    orionMinContourAreaDpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion min cnt area dpi 2")
    orionMinContourAreaDpi2Label.grid(row=13, column=0)
    orionMinContourAreaDpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionMinContourAreaDpi2)
    orionMinContourAreaDpi2Entry.grid(row=13, column=1)

    orionMaxContourAreaDpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion max cnt area dpi 2")
    orionMaxContourAreaDpi2Label.grid(row=14, column=0)
    orionMaxContourAreaDpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionMaxContourAreaDpi2)
    orionMaxContourAreaDpi2Entry.grid(row=14, column=1)

    orionmaxHoleRadiusDpi1Label = ttk.Label(settingstab2orion, text="Orion min hole rad dpi 1")
    orionmaxHoleRadiusDpi1Label.grid(row=15, column=0)
    orionmaxHoleRadiusDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionmaxHoleRadiusDpi1)
    orionmaxHoleRadiusDpi1Entry.grid(row=15, column=1)

    orionmaxHoleRadiusDpi2Label = ttk.Label(settingstab3orionDPI2, text="Orion min hole rad dpi 2")
    orionmaxHoleRadiusDpi2Label.grid(row=16, column=0)
    orionmaxHoleRadiusDpi2Entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionmaxHoleRadiusDpi2)
    orionmaxHoleRadiusDpi2Entry.grid(row=16, column=1)
    #endregion

    settingsWindow.protocol("WM_DELETE_WINDOW", onCloseSettings) # If the settings window is closing, run the onCloseSettings function

# Show analysis output for each image
def openAnalysisWindow():
    # Load all of the images that have been saved from analysis
    def loadImages():
        # Create a list of images
        global outputImages
        global outputImageNames
        outputImages = []
        outputImageNames = []
        # os.listdir returns a list of the files in the directory
        for file in os.listdir("images/output"):
            # Output images are saved as such: <original image name>-output.png
            if file.endswith("output.jpg"):
                outputImages.append(ImageTk.PhotoImage(Image.open("images/output/" + file).resize((600, 600), Image.ANTIALIAS))) # Load the image as a tkinter photo image and add it to the list
                outputImageNames.append(file) # Add the image name to the list
        
        # Prepare image names lists for use by ordering them in a clockwise fashion, starting with the top middle target image.
        # Define the correct order for the list
        clockwiseOrder = {"top-mid.jpg-output.jpg" : 0, 
                            "top-right.jpg-output.jpg" : 1, 
                            "upper-right.jpg-output.jpg" : 2, 
                            "lower-right.jpg-output.jpg" : 3, 
                            "bottom-right.jpg-output.jpg" : 4, 
                            "bottom-mid.jpg-output.jpg" : 5,
                            "bottom-left.jpg-output.jpg" : 6,
                            "lower-left.jpg-output.jpg" : 7,
                            "upper-left.jpg-output.jpg" : 8, 
                            "top-left.jpg-output.jpg" : 9}
        # Sort the images and image names list by the image names according to the clockwise order
        sortedZipped = sorted(zip(outputImages, outputImageNames), key=lambda d: clockwiseOrder[d[1]])
        # Unzip the sorted list into images and image names
        outputImages = [x for x, y in sortedZipped]
        outputImageNames = [y for x, y in sortedZipped]
        # Create friendly names for use in the GUI by removing the file extension and "-output" from the image name,
        # replacing the hyphens with spaces and capitalizing the first letter of each word.
        global outputFriendlyNames
        outputFriendlyNames = [(y.split(".jpg-output.jpg")[0]).replace("-", " ").capitalize() for x, y in sortedZipped]

    # Delete everything on the analysis canvas
    def clearCanvas():
        analysisCanvas.delete("all")

    # Shows the indexth image in the outputImages list
    def showImage(index):
        analysisCanvas.create_image(0, 0, anchor="nw", image=outputImages[index]) # Create the image on the canvas
        analysisTopLabel.config(text=outputFriendlyNames[index]) # Update the top label with the friendly name of the image

    # Advance to the next image in the outputImages list if allowed
    def onNextButtonPressed():
        global imageIndex
        if imageIndex < len(outputImages) - 1:
            imageIndex += 1
            clearCanvas()
            showImage(imageIndex)
        updateButtons()

    # Move back to the previous image in the outputImages list if allowed
    def onBackButtonPressed():
        global imageIndex
        if imageIndex > 0:
            imageIndex -= 1
            clearCanvas()
            showImage(imageIndex)
        updateButtons()

    # Close the analysis window and show the output window if enabled
    def onFinishButtonPressed():
        analysisWindow.destroy()
        if showOutputWhenFinishedVar.get():
            showOutput()

    # Update the buttons to show the correct state based on the current image index
    def updateButtons():
        if imageIndex == 0:
            analysisBackButton.config(state=DISABLED) # Disable the back button if the first image is showing
        else:
            analysisBackButton.config(state=NORMAL) # Enable the back button if the first image is not showing

        if imageIndex == len(outputImages)-1:
            analysisNextButton.config(text="Finish", style="Accent.TButton", command=onFinishButtonPressed) # If the last image is showing, change the next button to say "Finish" and make it an accent button (blue) for emphasis
        else:
            analysisNextButton.config(state=NORMAL, text="Next", style="Button.TButton") # If the last image is not showing, change the next button to say "Next" and make it a normal button

    #region Create the analysis window
    analysisWindow = tk.Toplevel(root)
    analysisWindow.title("Target Analysis")
    analysisWindow.minsize(width=600, height=690)
    analysisWindow.geometry("600x690")
    analysisWindow.tk.call('wm', 'iconphoto', analysisWindow._w, tk.PhotoImage(file='assets/icon.png'))
    #endregion

    #region Create frames
    # Top frame shows the image name
    analysisTopFrame = ttk.Frame(analysisWindow)
    analysisTopFrame.pack(side=TOP, fill=X)

    # Images frame holds the canvas with the images
    analysisImagesFrame = ttk.Frame(analysisWindow)
    analysisImagesFrame.pack(side=TOP, fill=X)

    # Bottom frame holds the buttons
    analysisBottomFrame = ttk.Frame(analysisWindow)
    analysisBottomFrame.pack(side=BOTTOM, fill=X)
    #endregion

    #region Create top label
    analysisTopLabel = ttk.Label(analysisTopFrame, text="Analysis", font="bold")
    analysisTopLabel.pack(pady=10)
    #endregion

    #region Create canvas
    analysisCanvas = tk.Canvas(analysisImagesFrame, width=600, height=600)
    analysisCanvas.pack()
    #endregion

    #region Create buttons
    analysisNextButton = ttk.Button(analysisBottomFrame, text="Next", command=onNextButtonPressed)#, style="Accent.TButton")
    analysisNextButton.pack(side=RIGHT, padx=5, pady=5)

    analysisBackButton = ttk.Button(analysisBottomFrame, text="Back", command=onBackButtonPressed)#, style="Accent.TButton")
    analysisBackButton.pack(side=LEFT, padx=5, pady=5)
    #endregion

    #Show first image
    global imageIndex
    imageIndex = 0
    loadImages()
    clearCanvas()
    showImage(imageIndex)
    updateButtons()

# Enables/Disables dark theme UI based on darkMode boolean variable state
def switchDarkMode():
    # If dark mode is enabled, set the theme to dark
    if darkModeVar.get() == True:
        root.tk.call("set_theme", "dark") # Set the theme to dark
    else:
        root.tk.call("set_theme", "light") # Set the theme to light

# Read settings from config file and apply them to the necessary tk vars
def updateSettingsFromConfigFile(file):
    # Create a config parser
    config = ConfigParser()

    config.read(file) # Read the given config file
    
    # Set variables to the values in the config file
    dpiVar.set(config.getint("settings", "dpi"))
    darkModeVar.set(config.getboolean("settings", "darkMode"))
    showOutputWhenFinishedVar.set(config.getboolean("settings", "showOutputWhenFinished"))
    individualOutputTypeVar.set(config.get('settings', 'individualOutputType'))
    useFileInfo.set(config.getboolean("settings", "useFileInfo"))
    switchDarkMode() # Apply the dark mode setting

    # Continue setting variables for the Orion targets
    orionKernelSizeDpi1.set(config.getint("orion", "orionKernelSizeDpi1"))
    orionKernelSizeDpi2.set(config.getint("orion", "orionKernelSizeDpi2"))
    orionParam1Dpi1.set(config.getfloat("orion", "orionParam1Dpi1"))
    orionParam2Dpi1.set(config.getint("orion", "orionParam2Dpi1"))
    orionMinRadiusDpi1.set(config.getint("orion", "orionMinRadiusDpi1"))
    orionParam1Dpi2.set(config.getint("orion", "orionParam1Dpi2"))
    orionParam2Dpi2.set(config.getint("orion", "orionParam2Dpi2"))
    orionMinRadiusDpi2.set(config.getint("orion", "orionMinRadiusDpi2"))
    orionThreshMin.set(config.getint("orion", "orionThreshMin"))
    orionThreshMax.set(config.getint("orion", "orionThreshMax"))
    orionMorphologyOpeningKernelSizeDpi1.set(config.getint("orion", "orionMorphologyOpeningKernelSizeDpi1"))
    orionMorphologyOpeningKernelSizeDpi2.set(config.getint("orion", "orionMorphologyOpeningKernelSizeDpi2"))
    orionMinContourAreaDpi1.set(config.getint("orion", "orionMinContourAreaDpi1"))
    orionMinContourAreaDpi2.set(config.getint("orion", "orionMinContourAreaDpi2"))
    orionMaxContourAreaDpi1.set(config.getint("orion", "orionMaxContourAreaDpi1"))
    orionMaxContourAreaDpi2.set(config.getint("orion", "orionMaxContourAreaDpi2"))
    orionmaxHoleRadiusDpi1.set(config.getint("orion", "orionmaxHoleRadiusDpi1"))
    orionmaxHoleRadiusDpi2.set(config.getint("orion", "orionmaxHoleRadiusDpi2"))

    # Continue setting variables for the NRA A-17
    nraKernalSize.set(config.getint("nra", "nraKernalSize"))
    nraParam1.set(config.getfloat("nra", "nraParam1"))
    nraParam2.set(config.getint("nra", "nraParam2"))
    nraMinRadius.set(config.getint("nra", "nraMinRadius"))
    nraThreshMin.set(config.getint("nra", "nraThreshMin"))
    nraThreshMax.set(config.getint("nra", "nraThreshMax"))
    nraMorphologyOpeningKernelSize.set(config.getint("nra", "nraMorphologyOpeningKernelSize"))
    nraMinContourArea.set(config.getint("nra", "nraMinContourArea"))
    nraMaxContourArea.set(config.getint("nra", "nraMaxContourArea"))
    nramaxHoleRadius.set(config.getint("nra", "nramaxHoleRadius"))

# Save settings to config file
def createDefaultConfigFile(file):
    # Create a config parser
    config = ConfigParser()

    config.read(file) # Read the given config file

    config.add_section('settings') # Add the settings section to the config file

    # Add the settings to the config file
    config.set('settings', 'dpi', str(dpiVar.get()))
    config.set('settings', 'darkMode', str(darkModeVar.get()))
    config.set('settings', 'showOutputWhenFinished', str(showOutputWhenFinishedVar.get()))
    config.set('settings', 'individualOutputType', str(individualOutputTypeVar.get()))
    config.set('settings', 'useFileInfo', str(useFileInfo.get()))

    # Add the orion section to the config file
    config.add_section('orion')
    # Settings for the orion targets
    config.set('orion', 'orionKernelSizeDpi1', str(orionKernelSizeDpi1.get()))
    config.set('orion', 'orionKernelSizeDpi2', str(orionKernelSizeDpi2.get()))
    config.set('orion', 'orionParam1Dpi1', str(orionParam1Dpi1.get()))
    config.set('orion', 'orionParam2Dpi1', str(orionParam2Dpi1.get()))
    config.set('orion', 'orionMinRadiusDpi1', str(orionMinRadiusDpi1.get()))
    config.set('orion', 'orionParam1Dpi2', str(orionParam1Dpi2.get()))
    config.set('orion', 'orionParam2Dpi2', str(orionParam2Dpi2.get()))
    config.set('orion', 'orionMinRadiusDpi2', str(orionMinRadiusDpi2.get()))
    config.set('orion', 'orionThreshMin', str(orionThreshMin.get()))
    config.set('orion', 'orionThreshMax', str(orionThreshMax.get()))
    config.set('orion', 'orionMorphologyOpeningKernelSizeDpi1', str(orionMorphologyOpeningKernelSizeDpi1.get()))
    config.set('orion', 'orionMorphologyOpeningKernelSizeDpi2', str(orionMorphologyOpeningKernelSizeDpi2.get()))
    config.set('orion', 'orionMinContourAreaDpi1', str(orionMinContourAreaDpi1.get()))
    config.set('orion', 'orionMinContourAreaDpi2', str(orionMinContourAreaDpi2.get()))
    config.set('orion', 'orionMaxContourAreaDpi1', str(orionMaxContourAreaDpi1.get()))
    config.set('orion', 'orionMaxContourAreaDpi2', str(orionMaxContourAreaDpi2.get()))
    config.set('orion', 'orionmaxHoleRadiusDpi1', str(orionmaxHoleRadiusDpi1.get()))
    config.set('orion', 'orionmaxHoleRadiusDpi2', str(orionmaxHoleRadiusDpi2.get()))

    # Add the NRA A-17 section to the config file
    config.add_section('nra')
    # Settings for the NRA A-17 targets
    config.set('nra', 'nraKernalSize', str(nraKernalSize.get()))
    config.set('nra', 'nraParam1', str(nraParam1.get()))
    config.set('nra', 'nraParam2', str(nraParam2.get()))
    config.set('nra', 'nraMinRadius', str(nraMinRadius.get()))
    config.set('nra', 'nraThreshMin', str(nraThreshMin.get()))
    config.set('nra', 'nraThreshMax', str(nraThreshMax.get()))
    config.set('nra', 'nraMorphologyOpeningKernelSize', str(nraMorphologyOpeningKernelSize.get()))
    config.set('nra', 'nraMinContourArea', str(nraMinContourArea.get()))
    config.set('nra', 'nraMaxContourArea', str(nraMaxContourArea.get()))
    config.set('nra', 'nramaxHoleRadius', str(nramaxHoleRadius.get()))

    # Write the changes to the config file
    with open(file, 'w') as f:
        config.write(f)

# Updates config.ini file with current settings
def updateConfig():
    config = ConfigParser() # Create a config parser

    config.read('config.ini') # Read the config file

    # Update the settings in the config file
    config.set('settings', 'dpi', str(dpiVar.get()))
    config.set('settings', 'darkMode', str(darkModeVar.get()))
    config.set('settings', 'showOutputWhenFinished', str(showOutputWhenFinishedVar.get()))
    config.set('settings', 'individualOutputType', str(individualOutputTypeVar.get()))
    config.set('settings', 'useFileInfo', str(useFileInfo.get()))
    # Continue updating the settings for the Orion section
    config.set('orion', 'orionKernelSizeDpi1', str(orionKernelSizeDpi1.get()))
    config.set('orion', 'orionKernelSizeDpi2', str(orionKernelSizeDpi2.get()))
    config.set('orion', 'orionParam1Dpi1', str(orionParam1Dpi1.get()))
    config.set('orion', 'orionParam2Dpi1', str(orionParam2Dpi1.get()))
    config.set('orion', 'orionMinRadiusDpi1', str(orionMinRadiusDpi1.get()))
    config.set('orion', 'orionParam1Dpi2', str(orionParam1Dpi2.get()))
    config.set('orion', 'orionParam2Dpi2', str(orionParam2Dpi2.get()))
    config.set('orion', 'orionMinRadiusDpi2', str(orionMinRadiusDpi2.get()))
    config.set('orion', 'orionThreshMin', str(orionThreshMin.get()))
    config.set('orion', 'orionThreshMax', str(orionThreshMax.get()))
    config.set('orion', 'orionMorphologyOpeningKernelSizeDpi1', str(orionMorphologyOpeningKernelSizeDpi1.get()))
    config.set('orion', 'orionMorphologyOpeningKernelSizeDpi2', str(orionMorphologyOpeningKernelSizeDpi2.get()))
    config.set('orion', 'orionMinContourAreaDpi1', str(orionMinContourAreaDpi1.get()))
    config.set('orion', 'orionMinContourAreaDpi2', str(orionMinContourAreaDpi2.get()))
    config.set('orion', 'orionMaxContourAreaDpi1', str(orionMaxContourAreaDpi1.get()))
    config.set('orion', 'orionMaxContourAreaDpi2', str(orionMaxContourAreaDpi2.get()))
    config.set('orion', 'orionmaxHoleRadiusDpi1', str(orionmaxHoleRadiusDpi1.get()))
    config.set('orion', 'orionmaxHoleRadiusDpi2', str(orionmaxHoleRadiusDpi2.get()))
    # Continue updating the settings for the NRA A-17 section
    config.set('nra', 'nraKernalSize', str(nraKernalSize.get()))
    config.set('nra', 'nraParam1', str(nraParam1.get()))
    config.set('nra', 'nraParam2', str(nraParam2.get()))
    config.set('nra', 'nraMinRadius', str(nraMinRadius.get()))
    config.set('nra', 'nraThreshMin', str(nraThreshMin.get()))
    config.set('nra', 'nraThreshMax', str(nraThreshMax.get()))
    config.set('nra', 'nraMorphologyOpeningKernelSize', str(nraMorphologyOpeningKernelSize.get()))
    config.set('nra', 'nraMinContourArea', str(nraMinContourArea.get()))
    config.set('nra', 'nraMaxContourArea', str(nraMaxContourArea.get()))
    config.set('nra', 'nramaxHoleRadius', str(nramaxHoleRadius.get()))

    # Write the changes to the config file
    with open('config.ini', 'w') as f:
        config.write(f)

# Ensures that an image/output directory is available to save images
def checkOutputDir():
    path = os.getcwd() + "/images/output" # Store the path to the output directory
    # If the output directory does not exist, create it
    if os.path.isdir(path) == False:
        os.mkdir(path)
    # Otherwise, nothing needs to be done

# Analyze an outdoor bull (CURRENTLY DISABLED) (ALSO NOT COMMENTED)
def analyzeOutdoorImage(image):
    # Basic implementation of the distance formula
    def ComputeDistance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA A-23 target in inches
    outer = 5.89
    six = 4.89/outer
    seven = 3.89/outer
    eight = 2.89/outer
    nine = 1.89/outer
    ten = 0.89/outer
    xRing = 0.39/outer

    spindleRadius = 0.11 # These are still in mm oof
    outerSpindleRadius = 0.177 # I might need to fix this
    #endregion

    droppedPoints = 0
    xCount = 0

    img = cv2.imread(image)
    output = img.copy()

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur using 3 * 3 kernel
    gray_blurred = cv2.blur(gray, (3, 3))
    cv2.imshow("gray_blurred", gray_blurred)

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
            # These need to be recalculated for the outdoor targets
            # if r/width < 0.4 and r/width > 0.35:
            #     pixelOuter = outer/37.670 * r
            
            # if r/width < 0.35:
            #     pixelOuter = outer/29.210 * r

            pixelSix = pixelOuter*six
            pixelSeven = pixelOuter*seven
            pixelEight = pixelOuter*eight
            pixelNine = pixelOuter*nine
            pixelTen = pixelOuter*ten
            pixelX = pixelOuter*xRing

            spindleRadius = spindleRadius*(pixelOuter/outer)
            #print(spindleRadius)
            outerSpindleRadius = outerSpindleRadius*(pixelOuter/outer)

            cv2.circle(output, (a, b), int(pixelOuter), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSix), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSeven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelEight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelNine), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelTen), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelX), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    # Make the image binary using a threshold
    img_thresholded = cv2.inRange(img, (100, 100, 100), (255, 255, 255))
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    kernel = np.ones((4,4),np.uint8)
    opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening',opening)

    # Find contours based on the denoised image
    contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # Get the area of the contours
        area = cv2.contourArea(contour)
        print(area)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000
        if area<200 and area>50:
            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
            holeCenter = (int(holeX),int(holeY))
            holeRadius = int(holeRadius)
            print("HoleRadius: " + str(holeRadius))
            if holeRadius < 40:
                #cv2.circle(output,holeCenter,holeRadius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, holeCenter, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,holeCenter,int(spindleRadius),(0,255,255),2)
                #cv2.circle(output,holeCenter,int(outerSpindleRadius),(0,255,255),2)

                distance = ComputeDistance(holeX, holeY, a, b)

                # Currently only scores target to a 4
                if distance-spindleRadius < pixelX:
                    print("X")
                    cv2.putText(output, "X", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    xCount += 1

                if distance+spindleRadius < pixelTen and distance-spindleRadius > pixelX:
                    print("0")
                    cv2.putText(output, "0", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                if distance-spindleRadius > pixelTen and distance+spindleRadius < pixelNine:
                    print("1")
                    cv2.putText(output, "1", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 1

                if distance-spindleRadius > pixelNine and distance+spindleRadius < pixelEight:
                    print("2")
                    cv2.putText(output, "2", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 2

                if distance-spindleRadius > pixelEight and distance+spindleRadius < pixelSeven:
                    print("3")
                    cv2.putText(output, "3", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 3

                if distance-spindleRadius > pixelSeven and distance+spindleRadius < pixelSix:
                    print("4")
                    cv2.putText(output, "4", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 4

                holeRatioX = (holeX-a) / pixelOuter
                holeRatioY = (holeY-a) / pixelOuter

                global csvName

                with open(csvName, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, droppedPoints, xCount, holeX, holeY, distance, holeRatioX, holeRatioY])
                    csvfile.close()
    #endregion

    cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
    cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output)

# Derived from improved.py
def analyzeImage(image):
    # Basic implementation of the distance formula
    def ComputeDistance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA A-17 target in millimeters
    outer = 46.150
    five = 37.670/outer
    six = 29.210/outer
    seven = 20.750/outer
    eight = 12.270/outer
    nine = 3.810/outer

    spindleRadius = 2.83
    outerSpindleRadius = 4.5
    #endregion

    # Hold local dropped points and x count variables
    droppedPoints = 0
    xCount = 0

    img = cv2.imread(image) # Read in the image for OpenCV
    output = img.copy() # Create a copy of the image to draw on

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur using 3 * 3 kernel
    gray_blurred = cv2.blur(gray, (nraKernalSize.get(), nraKernalSize.get()))
    #cv2.imshow("gray_blurred", gray_blurred)

    #threshold_image=cv2.inRange(gray_blurred, 100, 255)
    #cv2.imshow("threshold_image", threshold_image)
    
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, nraParam1.get(), nraParam2.get(), minRadius = nraMinRadius.get())
    
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

            spindleRadius = spindleRadius*(pixelOuter/outer)
            outerSpindleRadius = outerSpindleRadius*(pixelOuter/outer)

            cv2.circle(output, (a, b), int(pixelOuter), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelFive), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSix), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSeven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelEight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelNine), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    # Make the image binary using a threshold
    img_thresholded = cv2.inRange(img, (nraThreshMin.get(), nraThreshMin.get(), nraThreshMin.get()), (nraThreshMax.get(), nraThreshMax.get(), nraThreshMax.get()))
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    kernel = np.ones((nraMorphologyOpeningKernelSize.get(),nraMorphologyOpeningKernelSize.get()),np.uint8)
    opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening',opening)

    # Find contours based on the denoised image
    contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # Get the area of the contours
        area = cv2.contourArea(contour)
        print(area)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000
        if area<nraMaxContourArea.get() and area>nraMinContourArea.get():

            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
            holeCenter = (int(holeX),int(holeY))
            holeRadius = int(holeRadius)
            #print(holeRadius)
            if holeRadius < nramaxHoleRadius.get():
                #cv2.circle(output,holeCenter,holeRadius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, holeCenter, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,holeCenter,int(spindleRadius),(0,255,255),2)
                #cv2.circle(output,holeCenter,int(outerSpindleRadius),(0,255,255),2)

                distance = ComputeDistance(holeX, holeY, a, b)

                # Currently only scores target to a 4
                if distance-spindleRadius < pixelNine:
                    print("X")
                    cv2.putText(output, "X", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    xCount += 1

                if distance+spindleRadius < pixelEight and distance-spindleRadius > pixelNine:
                    print("0")
                    cv2.putText(output, "0", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                if distance+spindleRadius > pixelEight and distance+spindleRadius < pixelSeven:
                    print("1")
                    cv2.putText(output, "1", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 1

                if distance+spindleRadius > pixelSeven and distance+spindleRadius < pixelSix:
                    print("2")
                    cv2.putText(output, "2", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 2

                if distance+spindleRadius > pixelSix and distance+spindleRadius < pixelFive:
                    print("3")
                    cv2.putText(output, "3", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 3

                if distance+spindleRadius > pixelFive and distance+spindleRadius < pixelOuter:
                    print("4")
                    cv2.putText(output, "4", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 4

                holeRatioX = (holeX-a) / pixelOuter
                holeRatioY = (holeY-a) / pixelOuter

                global csvName

                with open(csvName, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, droppedPoints, xCount, holeX, holeY, distance, holeRatioX, holeRatioY])
                    csvfile.close()
    #endregion

    if individualOutputTypeVar.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Derived from analyzeImage
def analyzeOrionImage(image):
    # Basic implementation of the distance formula
    def ComputeDistance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA/USAS-50 target in millimeters
    outer = 33.38
    four = 28.5/outer
    five = 23.63/outer
    six = 18.75/outer
    seven = 13.87/outer
    eight = 9/outer
    nine = 4.12/outer
    ten = 0.76/outer

    # outer = 33.63
    # four = 28.75/outer
    # five = 23.88/outer
    # six = 19/outer
    # seven = 14.12/outer
    # eight = 9.25/outer
    # nine = 4.37/outer
    # ten = 1.01/outer

    innerSpindleRadius = 2.83
    outerSpindleRadius = 4.49
    #endregion

    # Hold local dropped points and x count variables
    droppedPoints = 0
    xCount = 0

    img = cv2.imread(image) # Read in the image for OpenCV
    output = img.copy() # Create a copy of the image to draw on

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if dpiVar.get() == 1:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orionKernelSizeDpi1.get(), orionKernelSizeDpi1.get()))
        

    if dpiVar.get() == 2:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orionKernelSizeDpi2.get(), orionKernelSizeDpi2.get()))

    #cv2.imshow("gray_blurred", gray_blurred)

    # Currently not performing any threshold operation
    #threshold_image=cv2.inRange(gray_blurred, 100, 255)
    #cv2.imshow("threshold_image", threshold_image)
    
    # Apply Hough transform on the blurred image.
    if dpiVar.get() == 1:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orionParam1Dpi1.get(), orionParam2Dpi1.get(), minRadius = orionMinRadiusDpi1.get())

    if dpiVar.get() == 2:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orionParam1Dpi2.get(), orionParam2Dpi2.get(), minRadius = orionMinRadiusDpi2.get())
    
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

            #print(str(r/width))
            if r/width < 0.37 and r/width > 0.32:
                pixelOuter = outer/23.63 * r
                #print("Fixing radius proportions")
            if r/width < 0.43 and r/width > 0.39:
                pixelOuter = outer/28.75 * r

            pixelFour = pixelOuter*four
            pixelFive = pixelOuter*five
            pixelSix = pixelOuter*six
            pixelSeven = pixelOuter*seven
            pixelEight = pixelOuter*eight
            pixelNine = pixelOuter*nine
            pixelTen = pixelOuter*ten

            outerSpindleRadius = outerSpindleRadius*(pixelOuter/outer)
            innerSpindleRadius = innerSpindleRadius*(pixelOuter/outer)

            cv2.circle(output, (a, b), int(pixelOuter), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelFour), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelFive), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSix), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSeven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelEight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelNine), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelTen), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    
    img_thresholded = cv2.inRange(img, (orionThreshMin.get(), orionThreshMin.get(), orionThreshMin.get()), (orionThreshMax.get(), orionThreshMax.get(), orionThreshMax.get())) # Make the image binary using a threshold
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    if dpiVar.get() == 1:
        kernel = np.ones((orionMorphologyOpeningKernelSizeDpi1.get(),orionMorphologyOpeningKernelSizeDpi1.get()),np.uint8)
    
    if dpiVar.get() == 2:
        kernel = np.ones((orionMorphologyOpeningKernelSizeDpi2.get(),orionMorphologyOpeningKernelSizeDpi2.get()),np.uint8)
    
    opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening',opening)

    # Find contours based on the denoised image
    contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #print("Contours: " + str(len(contours)))
    for contour in contours:
        
        # Get the area of the contours
        area = cv2.contourArea(contour)

        #cv2.drawContours(output,[contour],0,(255,0,0),2)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000

        if dpiVar.get() == 1:
            minArea = orionMinContourAreaDpi1.get()
            maxArea = orionMaxContourAreaDpi1.get()
        if dpiVar.get() == 2:
            minArea = orionMinContourAreaDpi2.get()
            maxArea = orionMaxContourAreaDpi2.get()

        if area<maxArea and area>minArea:
            # Draw the detected contour for debugging
            #cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole
            (holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
            holeCenter = (int(holeX),int(holeY))
            holeRadius = int(holeRadius)
            #print("Hole radius: " + str(holeRadius))
            #cv2.circle(output, holeCenter, holeRadius, (255,0,0), 2)
            # compute the center of the contour (different way than enclosing circle) (I don't even understand how it works)
            # M = cv2.moments(contour)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])
            
            # holeX = cX
            # holeY = cY

            holeCenter = (int(holeX),int(holeY))

            if dpiVar.get() == 1:
                maxHoleRadius = orionmaxHoleRadiusDpi1.get()
            if dpiVar.get() == 2:
                maxHoleRadius = orionmaxHoleRadiusDpi2.get()
            
            if holeRadius < maxHoleRadius:
                #cv2.circle(output,holeCenter,holeRadius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, holeCenter, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,holeCenter,int(outerSpindleRadius),(0,255,255),2)
                #cv2.circle(output,holeCenter,int(innerSpindleRadius),(255,255,0),2)

                distance = ComputeDistance(holeX, holeY, a, b)
                print("Distance: " + str(distance))
                print("Inner Spindle: " + str(innerSpindleRadius))
                # print("D-O: " + str(distance-outerSpindleRadius))
                # print("D+O: " + str(distance+outerSpindleRadius))
                print("pixelTen: " + str(pixelTen))
                # print("pixelNine: " + str(pixelNine))
                # print("pixelEight: " + str(pixelEight))
                # print("pixelSeven: " + str(pixelSeven))
                #print("holeRadius: " + str(holeRadius))

                if distance-outerSpindleRadius <= pixelTen or distance+outerSpindleRadius <= pixelEight:
                    print("X")
                    cv2.putText(output, "X", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    xCount += 1
                else:
                    if distance+outerSpindleRadius <= pixelSeven:
                        print("0")
                        cv2.putText(output, "0", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    else:
                        if distance+outerSpindleRadius <= pixelSix:
                            print("1")
                            cv2.putText(output, "1", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                            droppedPoints += 1
                        else:
                            if distance+outerSpindleRadius <= pixelFive:
                                print("2")
                                cv2.putText(output, "2", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                                droppedPoints += 2
                            else:
                                if distance+outerSpindleRadius <= pixelFour:
                                    print("3")
                                    cv2.putText(output, "3", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                                    droppedPoints += 3
                                else:
                                    print("Score more than 4 or low confidence: CHECK MANUALLY")
                                    label.config(text="Bull " + str(image) + " low confidence")
                                    

                holeRatioX = (holeX-a) / pixelOuter
                holeRatioY = (holeY-a) / pixelOuter

                global csvName

                with open(csvName, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, droppedPoints, xCount, holeX, holeY, distance, holeRatioX, holeRatioY])
                    csvfile.close()
    #endregion

    if individualOutputTypeVar.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Derived from analyzeOrionImage and analyzeImage
def analyzeOrionImageNRAScoring(image):
    # Basic implementation of the distance formula
    def ComputeDistance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA A-17 target in millimeters
    # because scoring is performed according to the NRA A-17 target
    outer = 46.150
    five = 37.670/outer
    six = 29.210/outer
    seven = 20.750/outer
    eight = 12.270/outer
    nine = 3.810/outer

    spindleRadius = 2.83
    outerSpindleRadius = 4.5
    #endregion

    # Hold local dropped points and x count variables
    droppedPoints = 0
    xCount = 0

    img = cv2.imread(image) # Read in the image for OpenCV
    output = img.copy() # Create a copy of the image to draw on

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if dpiVar.get() == 1:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orionKernelSizeDpi1.get(), orionKernelSizeDpi1.get()))
        

    if dpiVar.get() == 2:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orionKernelSizeDpi2.get(), orionKernelSizeDpi2.get()))

    #cv2.imshow("gray_blurred", gray_blurred)

    # Currently not performing any threshold operation
    #threshold_image=cv2.inRange(gray_blurred, 100, 255)
    #cv2.imshow("threshold_image", threshold_image)
    
    # Apply Hough transform on the blurred image.
    if dpiVar.get() == 1:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orionParam1Dpi1.get(), orionParam2Dpi1.get(), minRadius = orionMinRadiusDpi1.get())

    if dpiVar.get() == 2:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orionParam1Dpi2.get(), orionParam2Dpi2.get(), minRadius = orionMinRadiusDpi2.get())
    
    # Draw circles that are detected
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

            pixelOuter = r * 1.382564409826243

            # Perform a calculation to determine if the system detected the wrong ring, and if so, correct the error
            height, width, channels = img.shape

            #print(str(r/width))
            if r/width < 0.37 and r/width > 0.32:
                pixelOuter = outer/23.63 * r
                #print("Fixing radius proportions")
            if r/width < 0.43 and r/width > 0.39:
                pixelOuter = outer/28.75 * r

            pixelFive = pixelOuter*five
            pixelSix = pixelOuter*six
            pixelSeven = pixelOuter*seven
            pixelEight = pixelOuter*eight
            pixelNine = pixelOuter*nine

            spindleRadius = spindleRadius*(pixelOuter/outer)
            outerSpindleRadius = outerSpindleRadius*(pixelOuter/outer)

            cv2.circle(output, (a, b), int(pixelOuter), (0, 255, 0), 2)
            #cv2.circle(output, (a, b), int(pixelFour), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelFive), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSix), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelSeven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelEight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixelNine), (0, 255, 0), 2)
            #cv2.circle(output, (a, b), int(pixelTen), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    
    img_thresholded = cv2.inRange(img, (orionThreshMin.get(), orionThreshMin.get(), orionThreshMin.get()), (orionThreshMax.get(), orionThreshMax.get(), orionThreshMax.get())) # Make the image binary using a threshold
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    if dpiVar.get() == 1:
        kernel = np.ones((orionMorphologyOpeningKernelSizeDpi1.get(),orionMorphologyOpeningKernelSizeDpi1.get()),np.uint8)
    
    if dpiVar.get() == 2:
        kernel = np.ones((orionMorphologyOpeningKernelSizeDpi2.get(),orionMorphologyOpeningKernelSizeDpi2.get()),np.uint8)
    
    opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening',opening)

    # Find contours based on the denoised image
    contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #print("Contours: " + str(len(contours)))
    for contour in contours:
        
        # Get the area of the contours
        area = cv2.contourArea(contour)

        #cv2.drawContours(output,[contour],0,(255,0,0),2)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000

        if dpiVar.get() == 1:
            minArea = orionMinContourAreaDpi1.get()
            maxArea = orionMaxContourAreaDpi1.get()
        if dpiVar.get() == 2:
            minArea = orionMinContourAreaDpi2.get()
            maxArea = orionMaxContourAreaDpi2.get()

        if area<maxArea and area>minArea:
            # Draw the detected contour for debugging
            #cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole
            (holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
            holeCenter = (int(holeX),int(holeY))
            holeRadius = int(holeRadius)
            #print("Hole radius: " + str(holeRadius))
            #cv2.circle(output, holeCenter, holeRadius, (255,0,0), 2)
            # compute the center of the contour (different way than enclosing circle) (I don't even understand how it works)
            # M = cv2.moments(contour)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])
            
            # holeX = cX
            # holeY = cY

            holeCenter = (int(holeX),int(holeY))

            if dpiVar.get() == 1:
                maxHoleRadius = orionmaxHoleRadiusDpi1.get()
            if dpiVar.get() == 2:
                maxHoleRadius = orionmaxHoleRadiusDpi2.get()
            
            if holeRadius < maxHoleRadius:
                #cv2.circle(output,holeCenter,holeRadius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, holeCenter, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,holeCenter,int(outerSpindleRadius),(0,255,255),2)
                #cv2.circle(output,holeCenter,int(innerSpindleRadius),(255,255,0),2)

                distance = ComputeDistance(holeX, holeY, a, b)

                if distance-spindleRadius < pixelNine:
                    print("X")
                    cv2.putText(output, "X", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    xCount += 1

                if distance+spindleRadius < pixelEight and distance-spindleRadius > pixelNine:
                    print("0")
                    cv2.putText(output, "0", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                if distance+spindleRadius > pixelEight and distance+spindleRadius < pixelSeven:
                    print("1")
                    cv2.putText(output, "1", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 1

                if distance+spindleRadius > pixelSeven and distance+spindleRadius < pixelSix:
                    print("2")
                    cv2.putText(output, "2", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 2

                if distance+spindleRadius > pixelSix and distance+spindleRadius < pixelFive:
                    print("3")
                    cv2.putText(output, "3", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 3

                if distance+spindleRadius > pixelFive and distance+spindleRadius < pixelOuter:
                    print("4")
                    cv2.putText(output, "4", (int(holeX-50),int(holeY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    droppedPoints += 4
                                    

                holeRatioX = (holeX-a) / pixelOuter
                holeRatioY = (holeY-a) / pixelOuter

                global csvName

                with open(csvName, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, droppedPoints, xCount, holeX, holeY, distance, holeRatioX, holeRatioY])
                    csvfile.close()
    #endregion

    if individualOutputTypeVar.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

#region Initialize tkinter window
root = tk.Tk()
# Set the initial theme
root.tk.call("source", "assets/sun-valley/sun-valley.tcl")
root.tk.call("set_theme", "light")
# Set up the window geometry
root.minsize(550,400)
root.geometry("550x400")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='assets/icon.png'))
root.title("Target Analysis")
#endregion

#region Global variables
# DPI is consistent across all targets that would be scanned. Therefore, it only needs to be set once for all of them.
dpiVar = tk.IntVar(root, 1)
darkModeVar = tk.BooleanVar(root, False)
showOutputWhenFinishedVar = tk.BooleanVar(root, True)
individualOutputTypeVar = tk.StringVar(root, "tkinter")
useFileInfo = tk.BooleanVar(root, True)

#region While many similar parameters exist for non-Orion targets, each has been tuned for its use case and therefore are unique to Orion scanning.
orionKernelSizeDpi1 = tk.IntVar(root, 2)
orionKernelSizeDpi2 = tk.IntVar(root, 5)
orionParam1Dpi1 = tk.DoubleVar(root, 1.4)
orionParam2Dpi1 = tk.IntVar(root, 200)
orionMinRadiusDpi1 = tk.IntVar(root, 130)
orionParam1Dpi2 = tk.IntVar(root, 2)
orionParam2Dpi2 = tk.IntVar(root, 600)
orionMinRadiusDpi2 = tk.IntVar(root, 260)
orionThreshMin = tk.IntVar(root, 100)
orionThreshMax = tk.IntVar(root, 255)
orionMorphologyOpeningKernelSizeDpi1 = tk.IntVar(root, 2)
orionMorphologyOpeningKernelSizeDpi2 = tk.IntVar(root, 2)
orionMinContourAreaDpi1 = tk.IntVar(root, 200)
orionMaxContourAreaDpi1 = tk.IntVar(root, 5000)
orionMinContourAreaDpi2 = tk.IntVar(root, 5000)
orionMaxContourAreaDpi2 = tk.IntVar(root, 12000)
orionmaxHoleRadiusDpi1 = tk.IntVar(root, 40)
orionmaxHoleRadiusDpi2 = tk.IntVar(root, 90)
#endregion

#region Fine tuning settings for non-Orion targets
nraKernalSize = tk.IntVar(root, 3)
nraParam1 = tk.DoubleVar(root, 1.4)
nraParam2 = tk.IntVar(root, 200)
nraMinRadius = tk.IntVar(root, 130)
nraThreshMin = tk.IntVar(root, 100)
nraThreshMax = tk.IntVar(root, 255)
nraMorphologyOpeningKernelSize = tk.IntVar(root, 10)
nraMinContourArea = tk.IntVar(root, 200)
nraMaxContourArea = tk.IntVar(root, 1500)
nramaxHoleRadius = tk.IntVar(root, 40)
#endregion

# Check for a config file. If it exists, load the values from it. Otherwise, create a config file frome the defaults.
if os.path.isfile("config.ini"):
    # If the file exists, update settings to match the config file
    updateSettingsFromConfigFile("config.ini")
else:
    # If the file does not exist, create it and set the default values
    createDefaultConfigFile("config.ini")

# If there is not config backup, create one now
if not os.path.isfile("config-backup.ini"):
    # If the file does not exist, create it and set the default values
    createDefaultConfigFile("config-backup.ini")
#endregion

#region Menubar with File and Help menus
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="Load left image", command=loadImageLeft)
#filemenu.add_command(label="Load right image", command=loadImageRight)
#filemenu.add_command(label="Load single image", command=loadSingleImage)
#filemenu.add_command(label="Analyze target", command=analyzeTarget)
#filemenu.add_command(label="Open Folder", command=openFolder)
filemenu.add_command(label="Show in Explorer", command=showFolder)
filemenu.add_command(label="Show Output", command=showOutput, state=DISABLED)
filemenu.add_command(label="Show Trends", command=showTrends)
#filemenu.add_command(label="(Experimental) Load Outdoor", command=loadOutdoorBull)
filemenu.add_separator()
filemenu.add_command(label="Settings", command=openSettings)
filemenu.add_separator()
filemenu.add_command(label="Clear data", command=clearData)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
#filemenu.add_command(label="Analysis Window", command=openAnalysisWindow)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="README", command=lambda: openFile('"' + os.getcwd() + "/README.md" + '"'))
helpmenu.add_command(label="Scanning diagram", command=lambda: openFile('"' + os.getcwd() + "/help/" + "scanner-digital.png" + '"'))
helpmenu.add_command(label="Accuracy screenshot", command=lambda: openFile('"' + os.getcwd() + "/help/" + "accuracy-vs-hand-scored.png" + '"'))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
#endregion

#region Set up frames
# Topframe holds the main label
topFrame = ttk.Frame(root)
topFrame.pack(fill=X)

# Options frame has the settings for name, date, etc
optionsFrame = ttk.Frame(root)
optionsFrame.pack(side=tk.TOP, padx=7.5, pady=7.5)

# Notebook allows for a tabbed view of the different target types
tabControl = ttk.Notebook(root)

tab1indoor = ttk.Frame(tabControl)
tab2orion = ttk.Frame(tabControl)

tabControl.add(tab1indoor, text ='NRA A-17')
tabControl.add(tab2orion, text ='NRA/USAS-50')

tabControl.pack(side=tk.TOP, fill=BOTH, padx=10, pady=10)

# Buttons frames are a child of the tabs
buttonsFrame = ttk.Frame(tab1indoor)
buttonsFrame.pack(side=tk.TOP)

bottomFrame = ttk.Frame(tab1indoor)
bottomFrame.pack(side=tk.TOP)

orionButtonsFrame = ttk.Frame(tab2orion)
orionButtonsFrame.pack(side=tk.TOP)

orionBottomFrame = ttk.Frame(tab2orion)
orionBottomFrame.pack(side=tk.TOP)
#endregion

#region Label at top of the frame alerts the user to the program's actions uses topFrame
label = ttk.Label(topFrame, text="Load an image to get started")
label.pack(side=tk.TOP, padx=10, pady=5)

# Add a separator line
labelSeparator = ttk.Separator(topFrame, orient=HORIZONTAL)
labelSeparator.pack(side=TOP, fill=X)
#endregion

#region Options area uses optionsFrame
# Month entry
monthVar = tk.StringVar()
monthVar.set("Month")
monthEntry = ttk.Entry(optionsFrame, textvariable=monthVar, width=10)
monthEntry.grid(column = 0, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Day entry
dayVar = tk.StringVar()
dayVar.set("Day")
dateEntry = ttk.Entry(optionsFrame, textvariable=dayVar, width=5)
dateEntry.grid(column = 1, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Year entry
yearVar = tk.StringVar()
yearVar.set("Year")
yearEntry = ttk.Entry(optionsFrame, textvariable=yearVar, width=5)
yearEntry.grid(column = 2, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Target number entry
targetNumVar = tk.StringVar()
targetNumVar.set("Num")
targetNumEntry = ttk.Entry(optionsFrame, textvariable=targetNumVar, width=5)
targetNumEntry.grid(column = 3, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Name entry
nameVar = tk.StringVar()
nameVar.set("Name")
nameEntry = ttk.Entry(optionsFrame, textvariable=nameVar, width=30)
nameEntry.grid(column = 0, row = 1, columnspan = 4, sticky=NSEW, padx=2.5)

# Today button and use file info switch are placed to the right of the name and date
# Use today's date button
todayButton = ttk.Button(optionsFrame, text="Use Today", command=setInfoFromToday)
todayButton.grid(column=4, row=0, rowspan=2, padx=2.5)

# Use info from file switch
useFileInfoCheckbutton = ttk.Checkbutton(optionsFrame, text='Use info from file', style='Switch.TCheckbutton', variable=useFileInfo, onvalue=True, offvalue=False, command=updateConfig)
useFileInfoCheckbutton.grid(column=5, row=0, rowspan=2, padx=5)
#endregion

#region Buttons for NRA A-17 target loading and analysis
leftImageButton = ttk.Button(buttonsFrame, text = "Select left image", command = loadImageLeft)
leftImageButton.grid(row=0, column=0, padx=5, pady=5)

analyzeTargetButton = ttk.Button(buttonsFrame, text = "Analyze target", command = lambda: analyzeTarget("nra"))
analyzeTargetButton.grid(row=0, column=1, padx=5, pady=5)

rightImageButton = ttk.Button(buttonsFrame, text = "Select right image", command = loadImageRight)
rightImageButton.grid(row=0, column=2, padx=5, pady=5)

rightImageButton = ttk.Button(buttonsFrame, text = "Open folder", command = openFolder)
rightImageButton.grid(row=0, column=3, padx=5, pady=5)
#endregion

#region Buttons for Orion NRA/USAS-50 target loading and analysis
loadImageButton = ttk.Button(orionButtonsFrame, text = "Select image", command = loadImageOrion)
loadImageButton.grid(row=0, column=0, padx=5, pady=5)

analyzeOrionTargetButton = ttk.Button(orionButtonsFrame, text = "Analyze target", command = lambda: analyzeTarget("orion"))
analyzeOrionTargetButton.grid(row=0, column=1, padx=5, pady=5)

analyzeOrionTargetButton = ttk.Button(orionButtonsFrame, text = "Analyze with Orion scoring", command = lambda: analyzeTarget("orion-nrascoring"))
analyzeOrionTargetButton.grid(row=0, column=2, padx=5, pady=5)

openFolderOrionTargetButton = ttk.Button(orionButtonsFrame, text = "Open folder", command = openFolderOrion)
openFolderOrionTargetButton.grid(row=0, column=3, padx=5, pady=5)
#endregion

#region Add canvases for NRA A-17 target preview
leftCanvas = tk.Canvas(bottomFrame, width=230,height=300)
leftCanvas.grid(row = 0, column = 0, padx=5, pady=5)

rightCanvas = tk.Canvas(bottomFrame, width=230,height=300)
rightCanvas.grid(row = 0, column = 1, padx=5, pady=5)
#endregion

#region Add a single canvas for Orion NRA/USAS-50 target preview
orionSingleCanvas = tk.Canvas(orionBottomFrame, width=230,height=300)
orionSingleCanvas.grid(row = 0, column = 0)
#endregion

tk.mainloop()