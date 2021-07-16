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
## Email: picoplanetdev@gmail.com (business)              ##
##        skukla61@mtlstudents.net (school)               ##
## Status: Released, active development                   ##
############################################################
#endregion

#region Import libraries
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, EW, FLAT, HORIZONTAL, LEFT, NORMAL, NSEW, RIDGE, RIGHT, S, SOLID, SUNKEN, TOP, X
from typing_extensions import IntVar
import cv2
import tkinter as tk
from tkinter import StringVar, ttk
from cv2 import data
from numpy.core.numeric import count_nonzero
from ttkthemes import ThemedTk
from tkinter import Frame, filedialog
from PIL import ImageTk,Image
import os
import csv
import numpy as np
import math
import datetime
from numpy.core.fromnumeric import var
import matplotlib.pyplot as plt
import matplotlib
from configparser import ConfigParser
#endregion

# Loads an image for the left side of the target
def loadImageLeft():
    leftCanvas.delete("all")

    imageFile = filedialog.askopenfilename()
    leftImage = cv2.imread(imageFile)

    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    leftCanvas.grid(row = 0, column = 0)
    
    global leftPreview
    leftPreview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 350), Image.ANTIALIAS))
    leftCanvas.create_image(0, 0, anchor="nw", image=leftPreview)

    label.config(text="Right image loaded")

    root.geometry("500x500")

    cropLeft(leftImage)

# Loads an image for the right side of the target
def loadImageRight():
    rightCanvas.delete("all")

    imageFile = filedialog.askopenfilename()
    rightImage = cv2.imread(imageFile)

    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    rightCanvas.grid(row = 0, column = 1)
    
    global rightPreview
    rightPreview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 350), Image.ANTIALIAS))
    rightCanvas.create_image(0, 0, anchor="nw", image=rightPreview)

    label.config(text="Left image loaded")

    root.geometry("500x500")

    cropRight(rightImage)

# Loads an image taken by a smartphone camera that includes the entire target (CURRENTLY DISABLED)
def loadSingleImage():
    imageFile = filedialog.askopenfilename()
    singleImage = cv2.imread(imageFile)

    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    label.config(text="Single image loaded")

    cropSingle(singleImage)

# Derived from loadSingleImage and loadImage<Left/Right>
def loadImageOrion():
    orionSingleCanvas.delete("all")
    imageFile = filedialog.askopenfilename()
    singleImage = cv2.imread(imageFile)

    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    orionSingleCanvas.grid(row = 0, column = 1)
    
    global orionPreview
    orionPreview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 350), Image.ANTIALIAS))
    orionSingleCanvas.create_image(0, 0, anchor="nw", image=orionPreview)

    label.config(text="Orion single image loaded")

    root.geometry("500x500")

    cropOrion(singleImage)

# Somewhat derived from loadSingleImage (CURRENTLY DISABLED)
def loadOutdoorBull():
    imageFile = filedialog.askopenfilename()
    singleImage = cv2.imread(imageFile)

    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    label.config(text="Single image loaded")

    checkOutputDir()

    dsize = (int(singleImage.shape[1] * 0.2), int(singleImage.shape[0] * 0.2))
    resized = cv2.resize(singleImage, dsize)

    cv2.imwrite("images/output/outdoorBull.jpg", resized)

    global csvName
    csvName = "data/data-" + nameVar.get() + dayVar.get() + monthVar.get() + yearVar.get() + targetNumVar.get() + ".csv"

    analyzeOutdoorImage("images/output/outdoorBull.jpg")

# Crop image for orion target
def cropOrion(image):
    label.config(text="Cropping Orion image...")
    checkOutputDir()

    h=400 * dpiVar.get()
    w=400 * dpiVar.get()

    y=425 * dpiVar.get()
    x=1070 * dpiVar.get()
    crop1 = image[y:y+h, x:x+w]

    y=425 * dpiVar.get()
    x=1920 * dpiVar.get()
    crop2 = image[y:y+h, x:x+w]

    y=1175 * dpiVar.get()
    x=1920 * dpiVar.get()

    crop3 = image[y:y+h, x:x+w]

    y=1925 * dpiVar.get()
    x=1920 * dpiVar.get()

    crop4 = image[y:y+h, x:x+w]

    y=2680 * dpiVar.get()
    x=1920 * dpiVar.get()

    crop5 = image[y:y+h, x:x+w]

    y=2680 * dpiVar.get()
    x=1070 * dpiVar.get()

    crop6 = image[y:y+h, x:x+w]

    y=420 * dpiVar.get()
    x=225 * dpiVar.get()

    crop7 = image[y:y+h, x:x+w]

    y=1175 * dpiVar.get()
    x=225 * dpiVar.get()

    crop8 = image[y:y+h, x:x+w]

    y=1925 * dpiVar.get()
    x=225 * dpiVar.get()

    crop9 = image[y:y+h, x:x+w]

    y=2680 * dpiVar.get()
    x=225 * dpiVar.get()

    crop10 = image[y:y+h, x:x+w]

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
    label.config(text="Cropping right side...")

    checkOutputDir()

    #region Crop the image
    if dpiVar.get() == 2:
        dsize = (2550, 3507)
        image = cv2.resize(image, dsize, interpolation = cv2.INTER_LINEAR)

    y=275
    x=720
    h=580
    w=580
    crop1 = image[y:y+h, x:x+w]

    y=275
    x=1760
    h=580
    w=580
    crop2 = image[y:y+h, x:x+w]

    y=1070
    x=1760
    h=580
    w=580
    crop3 = image[y:y+h, x:x+w]

    y=1880
    x=1760
    h=580
    w=580
    crop4 = image[y:y+h, x:x+w]

    y=2680
    x=1760
    h=580
    w=580
    crop5 = image[y:y+h, x:x+w]

    y=2680
    x=720
    h=580
    w=580
    crop6 = image[y:y+h, x:x+w]
    #endregion

    # Save the cropped sections
    cv2.imwrite("images/output/top-mid.jpg", crop1)
    cv2.imwrite("images/output/top-right.jpg", crop2)
    cv2.imwrite("images/output/upper-right.jpg", crop3)
    cv2.imwrite("images/output/lower-right.jpg", crop4)
    cv2.imwrite("images/output/bottom-right.jpg", crop5)
    cv2.imwrite("images/output/bottom-mid.jpg", crop6)

    #region (OLD) Open Explorer to the location of the images
    #os.system("explorer " + '"' + os.getcwd() + "\images" + '"')
    #endregion

    #region (OLD) Run the analysis program on all of the images
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\top-mid.jpg" + '"')
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\top-right.jpg" + '"')
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\upper-right.jpg" + '"')
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\lower-right.jpg" + '"')
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\bottom-right.jpg" + '"')
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\bottom-mid.jpg" + '"')
    #endregion

    #region (OLD) Run the analysis function
    # analyzeImage("images/output/top-mid.jpg")
    # analyzeImage("images/output/top-right.jpg")
    # analyzeImage("images/output/upper-right.jpg")
    # analyzeImage("images/output/lower-right.jpg")
    # analyzeImage("images/output/bottom-right.jpg")
    # analyzeImage("images/output/bottom-mid.jpg")
    #endregion
    
    #label.config(text="Done")

# Crop image for left side of the target and start analysis process
def cropLeft(image):
    label.config(text="Cropping left side...")

    checkOutputDir()

    # Flips the image vertically and horizontally before cropping
    verticalFlippedImage = cv2.flip(image, -1)
    cv2.imwrite("images/output/vertical-flipped.jpg", verticalFlippedImage)

    #region Crop each image
    if dpiVar.get() == 2:
        dsize = (2550, 3507)
        verticalFlippedImage = cv2.resize(verticalFlippedImage, dsize, interpolation = cv2.INTER_LINEAR)

    y=240
    x=185
    h=580
    w=580
    crop2 = verticalFlippedImage[y:y+h, x:x+w]

    y=1040
    x=185
    h=580
    w=580
    crop3 = verticalFlippedImage[y:y+h, x:x+w]

    y=1840
    x=185
    h=580
    w=580
    crop4 = verticalFlippedImage[y:y+h, x:x+w]

    y=2645
    x=185
    h=580
    w=580
    crop5 = verticalFlippedImage[y:y+h, x:x+w]
    #endregion

    # Save the cropped sections
    cv2.imwrite("images/output/top-left.jpg", crop2)
    cv2.imwrite("images/output/upper-left.jpg", crop3)
    cv2.imwrite("images/output/lower-left.jpg", crop4)
    cv2.imwrite("images/output/bottom-left.jpg", crop5)

    # Open Explorer to the location of the images
    #os.system("explorer " + '"' + os.getcwd() + "\images" + '"')

    #region (OLD) Run the analysis program on all of the images
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\top-left.jpg" + '"' + " --month " + monthVar.get() + " --day " + dayVar.get() + " --year " + yearVar.get() + " --name " + nameVar.get())
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\upper-left.jpg" + '"' + " --month " + monthVar.get() + " --day " + dayVar.get() + " --year " + yearVar.get() + " --name " + nameVar.get())
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\lower-left.jpg" + '"' + " --month " + monthVar.get() + " --day " + dayVar.get() + " --year " + yearVar.get() + " --name " + nameVar.get())
    #os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\output\\bottom-left.jpg" + '"' + " --month " + monthVar.get() + " --day " + dayVar.get() + " --year " + yearVar.get() + " --name " + nameVar.get())
    #endregion

    #region (OLD) Run the analysis function on each image
    # analyzeImage("images/output/top-left.jpg")
    # analyzeImage("images/output/upper-left.jpg")
    # analyzeImage("images/output/lower-left.jpg")
    # analyzeImage("images/output/bottom-left.jpg")
    #endregion

    #label.config(text="Done")

# Runs the analyzeImage function for every image that has been cropped out
def analyzeTarget():
    label.config(text="Analyzing target...")

    global csvName
    csvName = "data/data-" + nameVar.get() + dayVar.get() + monthVar.get() + yearVar.get() + targetNumVar.get() + ".csv"

    #print(str(os.getcwd())+"\\"+csvName)
    if os.path.exists(str(os.getcwd()) +"\\" + csvName):
        #print("CSV already exists. Removing old version")
        os.remove(os.getcwd() + "\\" + csvName)
    
    with open(csvName, 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Image", "Dropped", "X", "HoleX", "HoleY", "Distance", "HoleRatioX", "HoleRatioY"])
        csvfile.close()

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

    global score, xCount
    score = 100
    xCount = 0

    with open(csvName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                score -= int(row[1])
                xCount += int(row[2])
            line_count += 1
    
    #print(str(os.getcwd()) +"data\data.csv")
    if not os.path.exists(str(os.getcwd()) +"\data\data.csv"):
        createCSV()

    with open("data/data.csv", 'a', newline="") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([nameVar.get(), dayVar.get() + " " + monthVar.get() + " " + yearVar.get(), targetNumVar.get(), score, xCount])
                csvfile.close()

    label.config(text="Done")

    # Make sure to count which entry this is! Starts at ZERO not one.
    filemenu.entryconfigure(1, state=NORMAL)

    #showOutput()

# Runs the analyzeImage function for every image that has been cropped out
def analyzeTargetOrion():
    label.config(text="Analyzing Orion target...")

    global csvName
    csvName = "data/data-" + nameVar.get() + dayVar.get() + monthVar.get() + yearVar.get() + targetNumVar.get() + ".csv"

    #print(str(os.getcwd())+"\\"+csvName)
    if os.path.exists(str(os.getcwd()) +"\\" + csvName):
        #print("CSV already exists. Removing old version")
        os.remove(os.getcwd() + "\\" + csvName)
    
    with open(csvName, 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Image", "Dropped", "X", "HoleX", "HoleY", "Distance", "HoleRatioX", "HoleRatioY"])
        csvfile.close()

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

    # Make sure to count which entry this is! Starts at ZERO not one.
    filemenu.entryconfigure(1, state=NORMAL)

    global score, xCount
    score = 100
    xCount = 0

    with open(csvName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                score -= int(row[1])
                xCount += int(row[2])
            line_count += 1
    
    #print(str(os.getcwd()) +"data\data.csv")
    if not os.path.exists(str(os.getcwd()) +"\data\data.csv"):
        createCSV()

    with open("data/data.csv", 'a', newline="") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([nameVar.get(), dayVar.get() + " " + monthVar.get() + " " + yearVar.get(), targetNumVar.get(), score, xCount])
                csvfile.close()

    label.config(text="Done")

    # Make sure to count which entry this is! Starts at ZERO not one.
    filemenu.entryconfigure(1, state=NORMAL)

    #showOutput()

# Shows the results of the program in a separate window and provides buttons for opening CSV files
def showOutput():
    label.config(text="Showing output")

    #region Create Toplevel window
    targetWindow = tk.Toplevel(root)
    targetWindow.minsize(525,750)
    targetWindow.geometry("525x750")
    targetWindow.iconbitmap("assets/icon.ico")
    targetWindow.title("Target Analysis")
    #endregion

    #region Create frames
    outputTopFrame = ttk.Frame(targetWindow)
    outputTopFrame.pack(side=TOP, fill=X, expand=True, pady=10)

    outputBottomFrame = ttk.Frame(targetWindow)
    outputBottomFrame.pack(side=TOP, fill=X)
    #endregion

    #region Create buttons and info at the top
    #print(csvName)
    openTargetCSVButton = ttk.Button(outputTopFrame, text="Open target CSV", command=lambda: openFile('"' + os.getcwd() + "\\" + csvName + '"'))
    openTargetCSVButton.grid(row=0, column=0)
    outputTopFrame.grid_columnconfigure(0, weight=1)
    
    scoreLabel = ttk.Label(outputTopFrame, text=str(score) + "-" + str(xCount) + "X")
    scoreLabel.grid(row=0, column=1)
    outputTopFrame.grid_columnconfigure(1, weight=1)

    #print('"' + os.getcwd() + "data/data.csv" + '"')
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
def showFolder():
    os.system("explorer " + '"' + os.getcwd() + '"')
    label.config(text="Working directory opened in Explorer")

# Open documentation with associated editor
def openFile(file):
    label.config(text="Opening file " + str(file))
    os.system(file)

# Create a template CSV file
def createCSV():
    with open('data/data.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'Date', 'Target Number', 'Score','X'])
        csvfile.close()
    label.config(text="Created CSV data file")

# Opens and analyzes all files in a folder
def openFolder():
    label.config(text="Opening folder")
    folder = filedialog.askdirectory()
    fileNum = 0
    for file in os.listdir(folder):
        if file.endswith(".jpeg"):
            path = os.getcwd() + "\images\\" + file
            setInfoFromFile(file)
            #print(path)
            fileImage = cv2.imread(path)
            if "left" in file:
                cropLeft(fileImage)
            elif "right" in file:
                cropRight(fileImage)
            fileNum += 1
            if fileNum == 2:
                analyzeTarget()
                fileNum = 0

# Opens and analyzes all files in a folder
def openFolderOrion():
    label.config(text="Opening folder")
    folder = filedialog.askdirectory()
    for file in os.listdir(folder):
        if file.endswith(".jpeg"):
            path = folder + "\\" + file
            setInfoFromFile(file)
            print(path)
            fileImage = cv2.imread(path)
            cropOrion(fileImage)
            analyzeTargetOrion()

# Allows viewing of trends from existing data files
def showTrends():
    label.config(text="Showing trends window")

    #region Create Toplevel window
    trendsWindow = tk.Toplevel(root)
    trendsWindow.minsize(250,100)
    trendsWindow.geometry("250x100")
    trendsWindow.iconbitmap("assets/icon.ico")
    trendsWindow.title("Target Analysis")
    #endregion


    def showMostMissed():
        bulls = [0,0,0,0,0,0,0,0,0,0]
        folder = filedialog.askdirectory()
        for file in os.listdir(folder):
            if not "data.csv" in file and not ".gitkeep" in file:
                with open("data/" + file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        #print(line_count)
                        if line_count != 0 and line_count <= 10:
                            bulls[line_count-1] += int(row[1])
                        line_count += 1
                    csv_file.close()
        #print(bulls)

        frame = ttk.Frame(trendsWindow)
        frame.pack(pady=5)
        trendsWindow.geometry("250x300")

        mostMissedLabel = ttk.Label(frame, text="Most missed is highest number")
        mostMissedLabel.grid(row=0, column=0, columnspan=3)

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
    
    def showTrendGraph():
        dataCSV = filedialog.askopenfilename()

        dates = []
        scores = []
        xCount = []
        with open(dataCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    dates.append(row[1])
                    scores.append(row[3])
                    xCount.append(row[4])
                line_count += 1
            csv_file.close()
        
        sortedZipped = sorted(zip(dates,scores,xCount), key=lambda date: datetime.datetime.strptime(date[0], "%d %B %Y"))

        dates,scores,xCount = map(list,zip(*sortedZipped))

        scores = list(map(int, scores))
        xCount = list(map(int, xCount))

        fig,axs = plt.subplots(2)

        axs[0].plot(dates,scores, marker='o', color = 'blue')

        axs[1].plot(dates,xCount, marker='x', color = 'orange')

        for x,y in zip(dates,scores):
            label = y
            axs[0].annotate(label, # this is the text
                        (x,y), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(-15,0), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center

        for x,y in zip(dates,xCount):
            label = str(y) + "X"
            axs[1].annotate(label, # this is the text
                        (x,y), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(-15,0), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center

        datesNum = matplotlib.dates.datestr2num(dates)

        z = np.polyfit(datesNum, scores, 1)
        p = np.poly1d(z)

        axs[0].plot(dates,p(datesNum), 'r--')

        axs[0].set_xlabel('Date')
        axs[1].set_xlabel('Date')

        axs[0].set_ylabel('Score')
        axs[1].set_ylabel('X Count')

        axs[0].xaxis.set_tick_params(rotation=40)
        axs[1].xaxis.set_tick_params(rotation=40)

        plt.subplots_adjust(hspace=0.8)

        plt.show()

    loadFolderButton = ttk.Button(trendsWindow, text="Load Folder (for most missed)", command=showMostMissed)
    loadFolderButton.pack(padx=10, pady=10)

    loadCSVButton = ttk.Button(trendsWindow, text="Load CSV (for graph)", command=showTrendGraph)
    loadCSVButton.pack(padx=10, pady=0)

# Sets file options by parsing a correctly-named target         
def setInfoFromFile(file):
    filename = os.path.basename(file)
    #print(filename)

    dayVar.set(filename[0:2])

    yearVar.set(filename[5:9])

    month = filename[2:5]
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
    
    for short, full in months.items():
        month = month.replace(short, full)

    monthVar.set(month)

    targetNumVar.set(filename[-6])

    if tabControl.tab(tabControl.select(), "text") == "NRA/USAS-50":
        nameVar.set(filename[9:-6])

    label.config(text="Set date to: " + monthVar.get() + " " + dayVar.get() + " " + yearVar.get() + " with target number " + targetNumVar.get())

# Sets file options from today's date
def setInfoFromToday():
    today = datetime.datetime.now()
    monthVar.set(today.strftime("%B"))
    dayVar.set(today.strftime("%d"))
    yearVar.set(today.strftime("%Y"))
    targetNumVar.set("1")
    label.config(text="Set date to: " + monthVar.get() + " " + dayVar.get() + " " + yearVar.get() + " with target number " + targetNumVar.get())

# Delete all files in the data folder
def clearData():
    path = str(os.getcwd()) + "\data"
    #print(path)
    for file in os.listdir(path):
        if file.endswith(".csv"):
            os.remove(path + "\\" + file)
    
    path = str(os.getcwd()) + "\images\output"
    #print(path)
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            os.remove(path + "\\" + file)

    label.config(text="/data and /images/output directories cleared")

# Create a settings window
def openSettings():
    def updateConfig():
        config = ConfigParser()
        config.read('config.ini')
        config.set('settings', 'dpi', str(dpiVar.get()))

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
        config.set('orion', 'orionMaxContourAreaDpi2', str(orionmaxHoleRadiusDpi2.get()))
        config.set('orion', 'orionmaxHoleRadiusDpi1', str(orionmaxHoleRadiusDpi1.get()))
        config.set('orion', 'orionmaxHoleRadiusDpi2', str(orionmaxHoleRadiusDpi2.get()))

        with open('config.ini', 'w') as f:
            config.write(f)

    def onCloseSettings():
        updateConfig()
        settingsWindow.destroy()

    label.config(text="Showing settings window")

    #region Create toplevel window
    settingsWindow = tk.Toplevel(root)
    settingsWindow.title("Target Analysis")
    settingsWindow.minsize(width=400, height=750)
    settingsWindow.geometry("400x750")
    settingsWindow.iconbitmap("assets/icon.ico")
    #endregion

    #region Create frames
    settingsTopFrame = ttk.Frame(settingsWindow)
    settingsTopFrame.pack(side=TOP, expand=False, pady=5, fill=X)

    settingsDpiFrame = ttk.Frame(settingsWindow)
    settingsDpiFrame.pack(side=TOP, fill=X)

    # TTK Notebook allows for a tabbed view
    tabControl = ttk.Notebook(root)

    tab1indoor = ttk.Frame(tabControl)
    tab2orion = ttk.Frame(tabControl)

    tabControl.add(tab1indoor, text ='NRA A-17')
    tabControl.add(tab2orion, text ='NRA/USAS-50')

    tabControl.pack(side=tk.TOP)

    dpiSeparator = ttk.Separator(settingsWindow, orient=HORIZONTAL)
    dpiSeparator.pack(side=TOP, fill=X, pady=5)

    settingsBottomFrame = ttk.Frame(settingsWindow)
    settingsBottomFrame.pack(side=TOP, expand=True, fill=BOTH)

    # TTK Notebook allows for a tabbed view
    settingsTabControl = ttk.Notebook(settingsBottomFrame)

    settingstab1NRAA17 = ttk.Frame(settingsTabControl)
    settingstab2orion = ttk.Frame(settingsTabControl)

    settingsTabControl.add(settingstab1NRAA17, text ='NRA A-17 Settings')
    settingsTabControl.add(settingstab2orion, text ='NRA/USAS-50 Orion Settings')

    settingsTabControl.pack(side=tk.TOP, expand=True, fill=BOTH, padx=10, pady=5)

    saveSeparator = ttk.Separator(settingsWindow, orient=HORIZONTAL)
    saveSeparator.pack(side=TOP, fill=X)

    saveButton = ttk.Button(settingsWindow, text="Save Settings", command=updateConfig)
    saveButton.pack(side=TOP, pady=5)
    #endregion

    #region Create top label
    settingsLabel1 = ttk.Label(settingsTopFrame, text="Settings", font='bold')
    settingsLabel1.pack(side=TOP)
    settingsLabel2 = ttk.Label(settingsTopFrame, text="⚠️ Change these only if the software does not work properly ⚠️")
    settingsLabel2.pack(side=TOP)
    labelSeparator = ttk.Separator(settingsTopFrame, orient=HORIZONTAL)
    labelSeparator.pack(side=TOP, fill=X, pady=10)
    #endregion

    #region Create dpi widgets
    settingsLabel1 = ttk.Label(settingsDpiFrame, text="Global settings", font = 'bold')
    settingsLabel1.grid(row=0, column=0)
    dpiButton300 = ttk.Radiobutton(settingsDpiFrame, text="300 dpi scanner", variable=dpiVar, value=1)
    dpiButton300.grid(row=1, column=0)
    dpiButton600 = ttk.Radiobutton(settingsDpiFrame, text="600 dpi scanner", variable=dpiVar, value=2)
    dpiButton600.grid(row=1, column=1)
    #endregion

    #region Create NRA A-17 widgets
    settingsLabel2 = ttk.Label(settingstab1NRAA17, text="NRA A-17 settings" , font='bold')
    settingsLabel2.grid(row=0, column=0, columnspan=2)
    #endregion

    #region Create Orion widgets
    settingsLabel1 = ttk.Label(settingstab2orion, text="Orion settings" , font='bold')
    settingsLabel1.grid(row=0, column=0, columnspan=2)

    orionKernelSizeDpi1Label = ttk.Label(settingstab2orion, text="Orion Kernel Size dpi 1")
    orionKernelSizeDpi1Label.grid(row=1, column=0)
    orionKernelSizeDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionKernelSizeDpi1)
    orionKernelSizeDpi1Entry.grid(row=1, column=1)

    orionKernelSizeDpi2Label = ttk.Label(settingstab2orion, text="Orion Kernel Size dpi 2")
    orionKernelSizeDpi2Label.grid(row=2, column=0)
    orionKernelSizeDpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionKernelSizeDpi2)
    orionKernelSizeDpi2Entry.grid(row=2, column=1)

    orionParam1Dpi1Label = ttk.Label(settingstab2orion, text="Orion Param1 dpi 1")
    orionParam1Dpi1Label.grid(row=3, column=0)
    orionParam1Dpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionParam1Dpi1)
    orionParam1Dpi1Entry.grid(row=3, column=1)

    orionParam2Dpi1Label = ttk.Label(settingstab2orion, text="Orion Param2 dpi 1")
    orionParam2Dpi1Label.grid(row=4, column=0)
    orionParam2Dpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionParam2Dpi1)
    orionParam2Dpi1Entry.grid(row=4, column=1)

    orionParam1Dpi2Label = ttk.Label(settingstab2orion, text="Orion Param1 dpi 2")
    orionParam1Dpi2Label.grid(row=5, column=0)
    orionParam1Dpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionParam1Dpi2)
    orionParam1Dpi2Entry.grid(row=5, column=1)

    orionParam2Dpi2Label = ttk.Label(settingstab2orion, text="Orion Param2 dpi 2")
    orionParam2Dpi2Label.grid(row=6, column=0)
    orionParam2Dpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionParam2Dpi2)
    orionParam2Dpi2Entry.grid(row=6, column=1)

    orionMinRadiusDpi1Label = ttk.Label(settingstab2orion, text="Orion MinRadius dpi 1")
    orionMinRadiusDpi1Label.grid(row=7, column=0)
    orionMinRadiusDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionMinRadiusDpi1)
    orionMinRadiusDpi1Entry.grid(row=7, column=1)

    orionMinRadiusDpi2Label = ttk.Label(settingstab2orion, text="Orion MinRadius dpi 2")
    orionMinRadiusDpi2Label.grid(row=8, column=0)
    orionMinRadiusDpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionMinRadiusDpi2)
    orionMinRadiusDpi2Entry.grid(row=8, column=1)

    orionThreshMinLabel = ttk.Label(settingstab2orion, text="Orion thresh min")
    orionThreshMinLabel.grid(row=9, column=0)
    orionThreshMinEntry = ttk.Entry(settingstab2orion, textvariable=orionThreshMin)
    orionThreshMinEntry.grid(row=9, column=1)

    orionThreshMaxLabel = ttk.Label(settingstab2orion, text="Orion thresh max")
    orionThreshMaxLabel.grid(row=10, column=0)
    orionThreshMaxEntry = ttk.Entry(settingstab2orion, textvariable=orionThreshMax)
    orionThreshMaxEntry.grid(row=10, column=1)

    orionMinContourAreaDpi1Label = ttk.Label(settingstab2orion, text="Orion min cnt area dpi 1")
    orionMinContourAreaDpi1Label.grid(row=11, column=0)
    orionMinContourAreaDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionMinContourAreaDpi1)
    orionMinContourAreaDpi1Entry.grid(row=11, column=1)

    orionMaxContourAreaDpi1Label = ttk.Label(settingstab2orion, text="Orion max cnt area dpi 1")
    orionMaxContourAreaDpi1Label.grid(row=12, column=0)
    orionMaxContourAreaDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionMaxContourAreaDpi1)
    orionMaxContourAreaDpi1Entry.grid(row=12, column=1)

    orionMinContourAreaDpi2Label = ttk.Label(settingstab2orion, text="Orion min cnt area dpi 2")
    orionMinContourAreaDpi2Label.grid(row=13, column=0)
    orionMinContourAreaDpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionMinContourAreaDpi2)
    orionMinContourAreaDpi2Entry.grid(row=13, column=1)

    orionMaxContourAreaDpi2Label = ttk.Label(settingstab2orion, text="Orion max cnt area dpi 2")
    orionMaxContourAreaDpi2Label.grid(row=14, column=0)
    orionMaxContourAreaDpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionMaxContourAreaDpi2)
    orionMaxContourAreaDpi2Entry.grid(row=14, column=1)

    orionmaxHoleRadiusDpi1Label = ttk.Label(settingstab2orion, text="Orion min hole rad dpi 1")
    orionmaxHoleRadiusDpi1Label.grid(row=15, column=0)
    orionmaxHoleRadiusDpi1Entry = ttk.Entry(settingstab2orion, textvariable=orionmaxHoleRadiusDpi1)
    orionmaxHoleRadiusDpi1Entry.grid(row=15, column=1)

    orionmaxHoleRadiusDpi2Label = ttk.Label(settingstab2orion, text="Orion min hole rad dpi 2")
    orionmaxHoleRadiusDpi2Label.grid(row=16, column=0)
    orionmaxHoleRadiusDpi2Entry = ttk.Entry(settingstab2orion, textvariable=orionmaxHoleRadiusDpi2)
    orionmaxHoleRadiusDpi2Entry.grid(row=16, column=1)
    #endregion

    settingsWindow.protocol("WM_DELETE_WINDOW", onCloseSettings)

# Ensures that an image/output directory is available to save images
def checkOutputDir():
    path = os.getcwd() + "\images\output"
    #print(path)
    if os.path.isdir(path) == False:
        os.mkdir(path)

# (CURRENTLY DISABLED)
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

    droppedPoints = 0
    xCount = 0

    img = cv2.imread(image)
    output = img.copy()

    #region Identify the target's outer ring
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
        print(area)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000
        if area<1500 and area>200:

            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
            holeCenter = (int(holeX),int(holeY))
            holeRadius = int(holeRadius)
            #print(holeRadius)
            if holeRadius < 40:
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

    cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
    cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output)

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

    droppedPoints = 0
    xCount = 0

    img = cv2.imread(image)
    output = img.copy()

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if dpiVar.get() == 1:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orionKernelSizeDpi1.get(), orionKernelSizeDpi1.get()))
        #cv2.imshow("gray_blurred", gray_blurred)

    if dpiVar.get() == 2:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orionKernelSizeDpi2.get(), orionKernelSizeDpi2.get()))

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
    if dpiVar.get == 1:
        kernel = np.ones((orionMorphologyOpeningKernelSizeDpi1.get(),orionMorphologyOpeningKernelSizeDpi1.get()),np.uint8)
    else:
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

            if dpiVar.get == 1:
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

    cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
    cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output)

#region Initialize tkinter
#root = tk.Tk()
root = ThemedTk(theme="breeze")
root.minsize(500,300)
root.geometry("500x300")
root.iconbitmap("assets/icon.ico")
root.title("Target Analysis")
#endregion

#region Global variables
# DPI is consistent across all targets that would be scanned. Therefore, it only needs to be set once for all of them.
dpiVar = tk.IntVar(root, 1)

#region While many similar parameters exist for non-Orion targets, each has been tuned for its use case and therefore are unique to Orion scanning.
orionKernelSizeDpi1 = tk.IntVar(root, 2)
orionKernelSizeDpi2 = tk.IntVar(root, 5)
orionParam1Dpi1 = tk.IntVar(root, 1.4)
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
orionMinContourAreaDpi2 = tk.IntVar(root, 5000)
orionMaxContourAreaDpi1 = tk.IntVar(root, 400)
orionMaxContourAreaDpi2 = tk.IntVar(root, 12000)
orionmaxHoleRadiusDpi1 = tk.IntVar(root, 40)
orionmaxHoleRadiusDpi2 = tk.IntVar(root, 90)
#endregion

# Create a ConfigParser object to read the config file
config = ConfigParser()
if os.path.isfile("config.ini"):
    # If the file exists, read it
    config.read('config.ini')
    dpiVar.set(config.getint("settings", "dpi"))

    orionKernelSizeDpi1.set(config.getint("orion", "orionKernelSizeDpi1"))
    orionKernelSizeDpi2.set(config.getint("orion", "orionKernelSizeDpi2"))
    orionParam1Dpi1.set(config.getint("orion", "orionParam1Dpi1"))
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
else:
    # If the file does not exist, create it and set the default values
    config.read('config.ini')
    config.add_section('settings')
    config.set('settings', 'dpi', str(dpiVar.get()))

    config.add_section('orion')
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

    with open('config.ini', 'w') as f:
        config.write(f)
#endregion

#region Menubar with File and Help menus
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="📁 Load left image", command=loadImageLeft)
#filemenu.add_command(label="📁 Load right image", command=loadImageRight)
#filemenu.add_command(label="📷 Load single image", command=loadSingleImage)
#filemenu.add_command(label="🎯 Analyze target", command=analyzeTarget)
#filemenu.add_command(label="🗃 Open Folder", command=openFolder)
filemenu.add_command(label="🗂 Show in Explorer", command=showFolder)
filemenu.add_command(label="💯 Show Output", command=showOutput, state=DISABLED)
filemenu.add_command(label="📈 Show Trends", command=showTrends)
#filemenu.add_command(label="(Experimental) Load Outdoor", command=loadOutdoorBull)
filemenu.add_separator()
filemenu.add_command(label="⚙️ Settings", command=openSettings)
filemenu.add_separator()
filemenu.add_command(label="⚠ Clear data", command=clearData)
filemenu.add_separator()
filemenu.add_command(label="❌ Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Usage", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "usage.txt" + '"'))
helpmenu.add_command(label="Scanning", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "scanning.txt" + '"'))
helpmenu.add_command(label="Scanning diagram", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "scanner-digital.png" + '"'))
helpmenu.add_command(label="Measurements", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "measurements.txt" + '"'))
helpmenu.add_command(label="Information", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "information.txt" + '"'))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
#endregion

#region Set up frames
topFrame = ttk.Frame(root)
topFrame.pack(fill=X)

optionsFrame = ttk.Frame(root)
optionsFrame.pack(side=tk.TOP, pady=10)

# TTK Notebook allows for a tabbed view
tabControl = ttk.Notebook(root)

tab1indoor = ttk.Frame(tabControl)
tab2orion = ttk.Frame(tabControl)

tabControl.add(tab1indoor, text ='NRA A-17')
tabControl.add(tab2orion, text ='NRA/USAS-50')

tabControl.pack(side=tk.TOP)

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
label = ttk.Label(topFrame, text="Click File -> Load Image to get started")
label.pack(side=tk.TOP, padx=10, pady=5)

labelSeparator = ttk.Separator(topFrame, orient=HORIZONTAL)
labelSeparator.pack(side=TOP, fill=X)
#endregion

#region Options area uses optionsFrame

# Month, day, year, and target number on same line
monthVar = tk.StringVar()
monthVar.set("Month")
monthEntry = ttk.Entry(optionsFrame, textvariable=monthVar, width=10)
monthEntry.grid(column = 0, row = 0, sticky=NSEW)

dayVar = tk.StringVar()
dayVar.set("Day")
dateEntry = ttk.Entry(optionsFrame, textvariable=dayVar, width=5)
dateEntry.grid(column = 1, row = 0, sticky=NSEW)

yearVar = tk.StringVar()
yearVar.set("Year")
yearEntry = ttk.Entry(optionsFrame, textvariable=yearVar, width=5)
yearEntry.grid(column = 2, row = 0, sticky=NSEW)

targetNumVar = tk.StringVar()
targetNumVar.set("Num")
targetNumEntry = ttk.Entry(optionsFrame, textvariable=targetNumVar, width=5)
targetNumEntry.grid(column = 3, row = 0, sticky=NSEW)

# Name goes below
nameVar = tk.StringVar()
nameVar.set("Name")
nameEntry = ttk.Entry(optionsFrame, textvariable=nameVar, width=30)
nameEntry.grid(column = 0, row = 1, columnspan = 4, sticky=NSEW)

# Today button and use file info checkbox are placed to the right of the name and date
todayButton = ttk.Button(optionsFrame, text="Use Today", command=setInfoFromToday)
todayButton.grid(column=4, row=0, rowspan=2, padx=10)

useFileInfo = tk.BooleanVar()
useFileInfo.set(True)
useFileInfoCheckbutton = ttk.Checkbutton(optionsFrame, text="Use info from file", variable=useFileInfo, onvalue=True, offvalue=False)
useFileInfoCheckbutton.grid(column=5, row=0, rowspan=2, padx=5)
#endregion

#region Buttons for NRA A-17 target loading and analysis
leftImageButton = ttk.Button(buttonsFrame, text = "Select left image", command = loadImageLeft)
leftImageButton.grid(row=0, column=0, padx=5, pady=5)

analyzeTargetButton = ttk.Button(buttonsFrame, text = "Analyze target", command = analyzeTarget)
analyzeTargetButton.grid(row=0, column=1, padx=5, pady=5)

rightImageButton = ttk.Button(buttonsFrame, text = "Select right image", command = loadImageRight)
rightImageButton.grid(row=0, column=2, padx=5, pady=5)

rightImageButton = ttk.Button(buttonsFrame, text = "Open folder", command = openFolder)
rightImageButton.grid(row=0, column=3, padx=5, pady=5)
#endregion

#region Buttons for Orion NRA/USAS-50 target loading and analysis
loadImageButton = ttk.Button(orionButtonsFrame, text = "Select image", command = loadImageOrion)
loadImageButton.grid(row=0, column=0, padx=5, pady=5)

analyzeOrionTargetButton = ttk.Button(orionButtonsFrame, text = "Analyze target", command = analyzeTargetOrion)
analyzeOrionTargetButton.grid(row=0, column=1, padx=5, pady=5)

analyzeOrionTargetButton = ttk.Button(orionButtonsFrame, text = "Open folder", command = openFolderOrion)
analyzeOrionTargetButton.grid(row=0, column=2, padx=5, pady=5)
#endregion

#region Add canvases for NRA A-17 target preview
leftCanvas = tk.Canvas(bottomFrame, width=230,height=300)
leftCanvas.grid(row = 0, column = 0)

rightCanvas = tk.Canvas(bottomFrame, width=230,height=300)
rightCanvas.grid(row = 0, column = 1)
#endregion

#region Add a single canvas for Orion NRA/USAS-50 target preview
orionSingleCanvas = tk.Canvas(orionBottomFrame, width=230,height=300)
orionSingleCanvas.grid(row = 0, column = 0)
#endregion

tk.mainloop()