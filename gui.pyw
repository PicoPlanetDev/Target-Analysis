#region Import libraries
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, FLAT, HORIZONTAL, LEFT, NORMAL, NSEW, RIGHT, SOLID, SUNKEN, TOP, X
import cv2
import tkinter as tk
from tkinter import ttk
from cv2 import data
from numpy.core.numeric import count_nonzero
from ttkthemes import ThemedTk
from tkinter import Frame, filedialog
from PIL import ImageTk,Image
import os
import csv
import numpy as np
import math
import argparse
import datetime
import shutil
from numpy.core.fromnumeric import var
import matplotlib.pyplot as plt
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

    root.geometry("500x470")

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

    root.geometry("500x470")

    cropRight(rightImage)

# Loads an image taken by a smartphone camera that includes the entire target
def loadSingleImage():
    imageFile = filedialog.askopenfilename()
    singleImage = cv2.imread(imageFile)

    if useFileInfo.get() is True:
        setInfoFromFile(imageFile)

    label.config(text="Single image loaded")

    cropSingle(singleImage)

# Helper function for cropSingle - Appends to list clicked points on the image
def singleImageClicked(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        singleImageClickPosition.append((x*5,y*5))
        #print("Appended position " + str(x) + "," + str(y))

# Runs perspective transform to the image and crops it to 10 output images
def cropSingle(image):
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

    y=270
    x=1235
    h=540
    w=540
    crop1 = resizedImage[y:y+h, x:x+w]

    y=270
    x=2230
    h=540
    w=540
    crop2 = resizedImage[y:y+h, x:x+w]

    y=1030
    x=2230
    h=540
    w=540
    crop3 = resizedImage[y:y+h, x:x+w]

    y=1785
    x=2230
    h=540
    w=540
    crop4 = resizedImage[y:y+h, x:x+w]

    y=2550
    x=2230
    h=540
    w=540
    crop5 = resizedImage[y:y+h, x:x+w]

    y=2550
    x=1235
    h=540
    w=540
    crop6 = resizedImage[y:y+h, x:x+w]

    y=2550
    x=250
    h=540
    w=540
    crop7 = resizedImage[y:y+h, x:x+w]

    y=1795
    x=250
    h=540
    w=540
    crop8 = resizedImage[y:y+h, x:x+w]

    y=1050
    x=250
    h=540
    w=540
    crop9 = resizedImage[y:y+h, x:x+w]

    y=270
    x=250
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

# Crop image for right side of the target and start analysis process
def cropRight(image):
    label.config(text="Cropping right side...")

    checkOutputDir()

    #region Crop the image
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

    analyzeImage("images/output/top-left.jpg")
    analyzeImage("images/output/upper-left.jpg")
    analyzeImage("images/output/lower-left.jpg")
    analyzeImage("images/output/bottom-left.jpg")
    analyzeImage("images/output/top-mid.jpg")
    analyzeImage("images/output/top-right.jpg")
    analyzeImage("images/output/upper-right.jpg")
    analyzeImage("images/output/lower-right.jpg")
    analyzeImage("images/output/bottom-right.jpg")
    analyzeImage("images/output/bottom-mid.jpg")

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
    filemenu.entryconfigure(6, state=NORMAL)

    #showOutput()

# Shows the results of the program in a separate window and provides buttons for opening CSV files
def showOutput():
    label.config(text="Showing output")

    #region Create Toplevel window
    targetWindow = tk.Toplevel(root)
    targetWindow.minsize(525,725)
    targetWindow.geometry("525x710")
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

# Basic implementation of the distance formula
def ComputeDistance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

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
            print(path)
            fileImage = cv2.imread(path)
            if "left" in file:
                cropLeft(fileImage)
            elif "right" in file:
                cropRight(fileImage)
            fileNum += 1
            if fileNum == 2:
                analyzeTarget()
                fileNum = 0

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
    shutil.rmtree(os.getcwd()+"\data")
    os.mkdir(os.getcwd()+"\data")

    shutil.rmtree(os.getcwd()+"\images\output")
    os.mkdir(os.getcwd()+"\images\output")

    label.config(text="/data and /images/output directories cleared")

# Ensures that an image/output directory is available to save images
def checkOutputDir():
    path = os.getcwd() + "\images\output"
    print(path)
    if os.path.isdir(path) == False:
        os.mkdir(path)

# Derived from improved.py
def analyzeImage(image):
    #region multipliers are from NRA A-17 target in millimeters
    outer = 46.150
    five = 37.670/outer
    six = 29.210/outer
    seven = 20.750/outer
    eight = 12.270/outer
    nine = 3.810/outer

    spindleRadius = 2.8
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

        # Check if area is between max and min values for a bullet hole. Area is usually about 1000
        if area<1500 and area>200:

            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (holeX,holeY),holeRadius = cv2.minEnclosingCircle(contour)
            holeCenter = (int(holeX),int(holeY))
            holeRadius = int(holeRadius)

            #cv2.circle(output,holeCenter,holeRadius,(0,255,0),2) # Enclosing circle
            cv2.circle(output, holeCenter, 1, (0, 0, 255), 3) # Dot at the center

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

#region Initialize tkinter
#root = tk.Tk()
root = ThemedTk(theme="breeze")
root.minsize(500,170)
root.geometry("500x170")
root.iconbitmap("assets/icon.ico")
root.title("Target Analysis")
#endregion

#region Menubar with File and Help menus
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="📁 Load left image", command=loadImageLeft)
filemenu.add_command(label="📁 Load right image", command=loadImageRight)
filemenu.add_command(label="📷 Load single image", command=loadSingleImage)
filemenu.add_command(label="🎯 Analyze target", command=analyzeTarget)
filemenu.add_command(label="🗃 Open Folder", command=openFolder)
filemenu.add_command(label="🗂 Show in Explorer", command=showFolder)
filemenu.add_command(label="💯 Show Output", command=showOutput, state=DISABLED)
filemenu.add_command(label="⚠ Clear data", command=clearData)
filemenu.add_separator()
filemenu.add_command(label="❌ Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Usage", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "usage.txt" + '"'))
helpmenu.add_command(label="Scanning", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "scanning.txt" + '"'))
helpmenu.add_command(label="Scanning diagram", command=lambda: openFile('"' + os.getcwd() + "\help\\" + "scanner-digital.png" + '"'))
helpmenu.add_separator()
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

buttonsFrame = ttk.Frame(root)
buttonsFrame.pack(side=tk.TOP)

bottomFrame = ttk.Frame(root)
bottomFrame.pack(side=tk.TOP)
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

#region Add buttons for loading images and analyzing the target uses buttonsFrame
leftImageButton = ttk.Button(buttonsFrame, text = "Select left image", command = loadImageLeft)
leftImageButton.grid(row=0, column=0, padx=5, pady=5)

analyzeTargetButton = ttk.Button(buttonsFrame, text = "Analyze target", command = analyzeTarget)
analyzeTargetButton.grid(row=0, column=1, padx=5, pady=5)

rightImageButton = ttk.Button(buttonsFrame, text = "Select right image", command = loadImageRight)
rightImageButton.grid(row=0, column=2, padx=5, pady=5)
#endregion

#region Add canvases uses bottomFrame
leftCanvas = tk.Canvas(bottomFrame, width=230,height=300)
leftCanvas.grid(row = 0, column = 0)

rightCanvas = tk.Canvas(bottomFrame, width=230,height=300)
rightCanvas.grid(row = 0, column = 1)
#endregion

tk.mainloop()