#region Import libraries
from tkinter.constants import BOTTOM, CENTER, FLAT, LEFT, RIGHT, SOLID, SUNKEN, TOP
import cv2
import tkinter as tk
from tkinter import ttk
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
#endregion

#region (OLD) Load an image using a file selection window
# def loadImage():
#     canvas.delete("all")

#     imageFile = filedialog.askopenfilename()
#     print(imageFile)
#     global image
#     image = cv2.imread(imageFile)

#     canvas.grid(row=5,columnspan=3)
    
#     global preview
#     preview = ImageTk.PhotoImage(Image.open(imageFile).resize((230, 300), Image.ANTIALIAS))
#     canvas.create_image(0, 0, anchor="nw", image=preview)

#     label.config(text="Image loaded")

#     root.geometry("400x400")
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

    label.config(text="Image loaded")

    root.geometry("500x400")

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

    label.config(text="Image loaded")

    root.geometry("500x400")

    cropRight(rightImage)

# Crop image for right side of the target and start analysis process
def cropRight(image):
    label.config(text="Analyzing right side...")

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

    #label.config(text="Done")

# Crop image for left side of the target and start analysis process
def cropLeft(image):
    label.config(text="Analyzing left side...")

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
    global csvName
    csvName = "data/data-" + nameVar.get() + dayVar.get() + monthVar.get() + yearVar.get() + targetNumVar.get() + ".csv"
    print(str(os.getcwd())+"\\"+csvName)
    if os.path.exists(str(os.getcwd()) +"\\" + csvName):
        print("CSV already exists. Removing old version")
        os.remove(os.getcwd() + "\\" + csvName)
    with open(csvName, 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Image", "Dropped", "X", "HoleX", "HoleY", "Distance"])
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

# Open the working folder in Explorer
def showFolder():
    os.system("explorer " + '"' + os.getcwd() + "\images" + '"')
    label.config(text="Working directory opened in Explorer")

# Open documentation with associated editor
def showDocumentation(docFile):
    label.config(text="Showing documentation " + str(docFile))
    os.system('"' + os.getcwd() + "\help\\" + docFile + '"')

# Basic implementation of the distance formula
def ComputeDistance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

# Create a template CSV file
def createCSV():
    with open('data.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'Month','Day','Year','Score','X'])
        csvfile.close()
    label.config(text="Created CSV data file")

#region Opens and analyzes all files in a folder
# def openFolder():
#     folder = filedialog.askdirectory()
#     for file in os.listdir(folder):
#         if file.endswith(".jpeg") or file.endswith(".jpg"):
#             path = os.getcwd() + "\images\\" + file
#             setInfoFromFile(file)
#             fileImage = cv2.imread(path)
#             if "left" in file:
#                 cropLeft(fileImage)
#             elif "right" in file:
#                 cropRight(fileImage)
#endregion

# Sets file options by parsing a correctly-named target         
def setInfoFromFile(file):
    filename = os.path.basename(file)
    print(filename)

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

# Sets file options from today's date
def setInfoFromToday():
    today = datetime.datetime.now()
    monthVar.set(today.strftime("%B"))
    dayVar.set(today.strftime("%d"))
    yearVar.set(today.strftime("%Y"))
    targetNumVar.set("1")

# Delete all files in the data folder
def clearData():
    shutil.rmtree(os.getcwd()+"\data")
    os.mkdir(os.getcwd()+"\data")

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

            spindleRadius = 2.794*(pixelOuter/outer)

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

            score = 0
            xCount = 0

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

            global csvName

            with open(csvName, 'a', newline="") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([image, droppedPoints, xCount, holeX, holeY, distance])
                csvfile.close()
    #endregion

    cv2.imshow("output", output)
    cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output)

#region Initialize tkinter
#root = tk.Tk()
root = ThemedTk(theme="breeze")
root.minsize(500,200)
root.geometry("500x200")
root.iconbitmap("assets/icon.ico")
root.title("Target Analysis")
#endregion

#region Menubar with File and Help menus
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="Load Image", command=loadImage)
filemenu.add_command(label="📂 Load left image", command=loadImageLeft)
filemenu.add_command(label="📂 Load right image", command=loadImageRight)
filemenu.add_command(label="🎯 Analyze target", command=analyzeTarget)
#filemenu.add_command(label="Save CSV", command=saveCSV)
#filemenu.add_command(label="Open Folder", command=openFolder)
filemenu.add_command(label="💾 Show in Explorer", command=showFolder)
filemenu.add_command(label="⚠️ Clear data", command=clearData)
#filemenu.add_command(label="Create CSV data file", command=createCSV)
filemenu.add_separator()
filemenu.add_command(label="❌ Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Usage", command=lambda: showDocumentation("usage.txt"))
helpmenu.add_separator()
helpmenu.add_command(label="Scanning", command=lambda: showDocumentation("scanning.txt"))
helpmenu.add_command(label="Scanning diagram", command=lambda: showDocumentation("scanner.jpg"))
helpmenu.add_separator()
helpmenu.add_command(label="Measurements", command=lambda: showDocumentation("measurements.txt"))
helpmenu.add_command(label="Information", command=lambda: showDocumentation("information.txt"))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
#endregion

#region Set up the top, options, and bottom frames
topFrame = ttk.Frame(root)
topFrame.pack()
optionsFrame = ttk.Frame(root)
optionsFrame.pack(side=tk.TOP)
buttonsFrame = ttk.Frame(root)
buttonsFrame.pack(side=tk.TOP)
bottomFrame = ttk.Frame(root)
bottomFrame.pack(side=tk.TOP)
#endregion

#region Label at top of the frame alerts the user to the program's actions uses topFrame
label = ttk.Label(topFrame, text="Click File -> Load Image to get started")
label.pack(side=tk.TOP, padx=10, pady=5)
#endregion

#region Options area uses optionsFrame
monthVar = tk.StringVar()
monthVar.set("Month")
monthEntry = ttk.Entry(optionsFrame, textvariable=monthVar, width=10)
#monthEntry.pack(side=LEFT)
monthEntry.grid(column = 0, row = 0)

dayVar = tk.StringVar()
dayVar.set("Day")
dateEntry = ttk.Entry(optionsFrame, textvariable=dayVar, width=5)
#dateEntry.pack(side=LEFT)
dateEntry.grid(column = 1, row = 0)

yearVar = tk.StringVar()
yearVar.set("Year")
yearEntry = ttk.Entry(optionsFrame, textvariable=yearVar, width=5)
#yearEntry.pack(side=LEFT)
yearEntry.grid(column = 2, row = 0)

targetNumVar = tk.StringVar()
targetNumVar.set("Num")
targetNumEntry = ttk.Entry(optionsFrame, textvariable=targetNumVar, width=5)
#targetNumEntry.pack(side=LEFT)
targetNumEntry.grid(column = 3, row = 0)

nameVar = tk.StringVar()
nameVar.set("Sigmond")
nameEntry = ttk.Entry(optionsFrame, textvariable=nameVar, width=30)
#nameEntry.pack(side=tk.TOP)
nameEntry.grid(column = 0, row = 1, columnspan = 4)

todayButton = ttk.Button(optionsFrame, text="Use Today", command=setInfoFromToday)
todayButton.grid(column=4, row=0, rowspan=2, padx=10)

useFileInfo = tk.BooleanVar()
useFileInfo.set(True)
useFileInfoCheckbutton = ttk.Checkbutton(optionsFrame, text="Use info from file", variable=useFileInfo, onvalue=True, offvalue=False)
useFileInfoCheckbutton.grid(column=5, row=0, rowspan=2, padx=5)
#endregion

#region Add buttons for loading images and analyzing the target uses buttonsFrame
leftImageButton = ttk.Button(buttonsFrame, text = "Select left image", command = loadImageLeft)
leftImageButton.grid(row=0, column=0, padx=5, pady=10)

analyzeTargetButton = ttk.Button(buttonsFrame, text = "Analyze target", command = analyzeTarget)
analyzeTargetButton.grid(row=0, column=1, padx=5, pady=10)

rightImageButton = ttk.Button(buttonsFrame, text = "Select right image", command = loadImageRight)
rightImageButton.grid(row=0, column=2, padx=5, pady=10)
#endregion

#region Add canvases uses bottomFrame
leftCanvas = tk.Canvas(bottomFrame, width=230,height=300)
leftCanvas.grid(row = 0, column = 0)

rightCanvas = tk.Canvas(bottomFrame, width=230,height=300)
rightCanvas.grid(row = 0, column = 1)
#endregion

tk.mainloop()