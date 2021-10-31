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
##          +1 (412)-287-0463 (mobile phone)              ##
## Status: Released, active development                   ##
############################################################
#endregion

#region Import libraries
from tkinter.constants import BOTH, BOTTOM, DISABLED, HORIZONTAL, LEFT, NORMAL, NSEW, RIDGE, RIGHT, TOP, X
from tkinter.font import BOLD
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

# --------------------------- Load image functions --------------------------- #

# Loads an image for the left side of the target
def load_image_left():
    """
    Prompts the user to select an image from their computer which is used for the left scan of the NRA A-17 target.
    """
    main_label.config(text="Loading left image...") # Update the main label

    left_canvas.delete("all") # Clear the left canvas in case it already has an image

    image_file = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    left_image = cv2.imread(image_file) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if use_file_info_var.get() is True:
        set_info_from_file(image_file)

    left_canvas.grid(row = 0, column = 0) # Refresh the canvas
    
    global left_preview # Images must be stored globally to be show on the canvas
    left_preview = ImageTk.PhotoImage(Image.open(image_file).resize((230, 350), Image.ANTIALIAS)) # Store the image as a tkinter photo image and resize it
    left_canvas.create_image(0, 0, anchor="nw", image=left_preview) # Place the image on the canvas

    main_label.config(text="Right image loaded") # Update the main label

    root.minsize(550,540) # Increase the window size to accomodate the image

    crop_left(left_image) # Crop the image to prepare for analysis

# Loads an image for the right side of the target
def load_image_right():
    """
    Prompts the user to select an image from their computer which is used for the right scan of the NRA A-17 target.
    """
    main_label.config(text="Loading right image...") # Update the main label

    right_canvas.delete("all") # Clear the right canvas in case it already has an image

    image_file = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    right_image = cv2.imread(image_file) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if use_file_info_var.get() is True:
        set_info_from_file(image_file)

    right_canvas.grid(row = 0, column = 1) # Refresh the canvas
    
    global right_preview # Images must be stored globally to be show on the canvas
    right_preview = ImageTk.PhotoImage(Image.open(image_file).resize((230, 350), Image.ANTIALIAS)) # Store the image as a tkinter photo image and resize it
    right_canvas.create_image(0, 0, anchor="nw", image=right_preview) # Place the image on the canvas

    main_label.config(text="Left image loaded") # Update the main label

    root.minsize(550,540) # Increase the window size to accomodate the image

    crop_right(right_image) # Crop the image to prepare for analysis

# Loads an image taken by a smartphone camera that includes the entire target (CURRENTLY DISABLED)
def load_image_single():
    image_file = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    single_image = cv2.imread(image_file) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if use_file_info_var.get() is True:
        set_info_from_file(image_file)

    main_label.config(text="Single image loaded") # Update the main label

    crop_single(single_image) # Crop the image to prepare for analysis

# Loads an image for an Orion target
def load_image_orion(target_type):
    """Loads an image for an Orion target. and displays it on the preview canvas.

    Args:
        target_type (str): 'orion' or 'orion-nrascoring'
    """
    main_label.config(text="Loading image...") # Update the main label

    if target_type == "orion": canvas = orion_single_canvas
    elif target_type == "orion-nrascoring": canvas = orion_single_canvas_nra

    canvas.delete("all") # Clear the orion single canvas in case it already has an image

    image_file = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    single_image = cv2.imread(image_file) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if use_file_info_var.get() is True:
        set_info_from_file(image_file)

    canvas.grid(row = 0, column = 1) # Refresh the canvas
    
    global orion_preview # Images must be stored globally to be show on the canvas
    orion_preview = ImageTk.PhotoImage(Image.open(image_file).resize((230, 350), Image.ANTIALIAS)) # Store the image as a tkinter photo image and resize it
    canvas.create_image(0, 0, anchor="nw", image=orion_preview) # Place the image on the canvas

    main_label.config(text="Orion image loaded") # Update the main label

    root.minsize(550,540) # Increase the window size to accomodate the image

    crop_orion(single_image) # Crop the image to prepare for analysis

# Somewhat derived from load_image_single (CURRENTLY DISABLED)
def load_image_outdoor():
    image_file = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    single_image = cv2.imread(image_file) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if use_file_info_var.get() is True:
        set_info_from_file(image_file)

    main_label.config(text="Outdoor image loaded") # Update the main label

    # Perform the cropping and analysis automatically
    check_output_dir()

    dsize = (int(single_image.shape[1] * 0.2), int(single_image.shape[0] * 0.2))
    resized = cv2.resize(single_image, dsize)

    cv2.imwrite("images/output/outdoorBull.jpg", resized)

    global csv_name
    csv_name = "data/data-" + name_var.get() + day_var.get() + month_var.get() + year_var.get() + target_num_var.get() + ".csv"

    analyze_outdoor_image("images/output/outdoorBull.jpg")

# --------------------------- Crop image functions --------------------------- #

# Crop image for an Orion target
def crop_orion(image):
    """Crops the given image for an Orion NRA/USAS-50 target. Stores the cropped images in the images/output folder.

    Args:
        image (cv2 image): [description]
    """    
    main_label.config(text="Cropping image...") # Update the main label
    check_output_dir() # Make sure the output directory exists

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

    if use_bubbles_var.get() and (tab_control.index("current") == 1 or tab_control.index("current") == 2):
        main_label.config(text="Setting name from bubbles...")
        set_name_from_bubbles(image)

    main_label.config(text="Cropped image") # Update the main label

# Runs perspective transform to the image and crops it to 10 output images (CURRENTLY DISABLED)
def crop_single(image):
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
    # Helper function for crop_single - Calculates perspective transform for an image
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
    # Helper function for crop_single - Appends to list clicked points on the image
    def singleImageClicked(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            singleImageClickPosition.append((x*5,y*5))
            #print("Appended position " + str(x) + "," + str(y))

    copy = image.copy()

    main_label.config(text="Cropping single image...")

    check_output_dir()

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
    resized_image = cv2.resize(warped, dsize, interpolation = cv2.INTER_AREA)

    cv2.imwrite("images/output/resized.jpg", resized_image)

    y=250
    x=1215
    h=540
    w=540
    crop1 = resized_image[y:y+h, x:x+w]

    y=250
    x=2215
    h=540
    w=540
    crop2 = resized_image[y:y+h, x:x+w]

    y=1010
    x=2215
    h=540
    w=540
    crop3 = resized_image[y:y+h, x:x+w]

    y=1785
    x=2215
    h=540
    w=540
    crop4 = resized_image[y:y+h, x:x+w]

    y=2550
    x=2215
    h=540
    w=540
    crop5 = resized_image[y:y+h, x:x+w]

    y=2550
    x=1210
    h=540
    w=540
    crop6 = resized_image[y:y+h, x:x+w]

    y=2550
    x=205
    h=540
    w=540
    crop7 = resized_image[y:y+h, x:x+w]

    y=1785
    x=205
    h=540
    w=540
    crop8 = resized_image[y:y+h, x:x+w]

    y=1010
    x=205
    h=540
    w=540
    crop9 = resized_image[y:y+h, x:x+w]

    y=250
    x=205
    h=540
    w=540
    crop10 = resized_image[y:y+h, x:x+w]

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
def crop_right(image):
    """Crops the given image for the right side of an NRA A-17 target. Stores the cropped images in the images/output folder.

    Args:
        image (cv2 image): [description]
    """ 
    main_label.config(text="Cropping right image...") # Update main label

    check_output_dir() # Make sure that output directory exists

    #region Crop the image
    # if dpi_var.get() == 2:
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

    main_label.config(text="Cropped right image") # Update the main label

# Crop image for left side of the target and start analysis process
def crop_left(image):
    """Crops the given image for the left side of an NRA A-17 target, which includes flipping the image. Stores the cropped images in the images/output folder.

    Args:
        image (cv2 image): [description]
    """ 
    main_label.config(text="Cropping left image...") # Update main label

    check_output_dir() # Make sure that output directory exists

    # Flips the image vertically and horizontally before cropping
    verticalFlippedImage = cv2.flip(image, -1)
    cv2.imwrite("images/output/vertical-flipped.jpg", verticalFlippedImage)

    #region Crop each image
    # if dpi_var.get() == 2:
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

    main_label.config(text="Cropped image") # Update the main label

# -------------------- Target processing control functions ------------------- #

# Runs the analyze_image function for every image that has been cropped out
def analyze_target(type):
    """Runs the appropriate analyze_image function for every image that has been cropped and saved.

    Args:
        type (str): 'nra' or 'orion' or 'orion-nrascoring'
    """    
    main_label.config(text="Analyzing target...") # Update main label

    # Create and store a name for the target output file
    global csv_name
    csv_name = "data/data-" + name_var.get() + day_var.get() + month_var.get() + year_var.get() + target_num_var.get() + ".csv"

    # If the CSV file already exists, delete it
    if os.path.exists(str(os.getcwd()) +"/" + csv_name):
        print("CSV already exists. Removing old version")
        os.remove(os.getcwd() + "/" + csv_name)
    
    # Create the CSV file template
    with open(csv_name, 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Image", "Dropped", "X", "hole_x", "hole_y", "Distance", "hole_ratio_x", "hole_ratio_y"])
        csvfile.close()

    # Analyze each cropped image
    if type == "nra":
        analyze_image("images/output/top-mid.jpg")
        analyze_image("images/output/top-right.jpg")
        analyze_image("images/output/upper-right.jpg")
        analyze_image("images/output/lower-right.jpg")
        analyze_image("images/output/bottom-right.jpg")
        analyze_image("images/output/bottom-mid.jpg")
        analyze_image("images/output/bottom-left.jpg")
        analyze_image("images/output/lower-left.jpg")
        analyze_image("images/output/upper-left.jpg")
        analyze_image("images/output/top-left.jpg")
    elif type == "orion":
        analyze_orion_image("images/output/top-mid.jpg")
        analyze_orion_image("images/output/top-right.jpg")
        analyze_orion_image("images/output/upper-right.jpg")
        analyze_orion_image("images/output/lower-right.jpg")
        analyze_orion_image("images/output/bottom-right.jpg")
        analyze_orion_image("images/output/bottom-mid.jpg")
        analyze_orion_image("images/output/bottom-left.jpg")
        analyze_orion_image("images/output/lower-left.jpg")
        analyze_orion_image("images/output/upper-left.jpg")
        analyze_orion_image("images/output/top-left.jpg")
    elif type == "orion-nrascoring":
        analyze_orion_image_nra_scoring("images/output/top-mid.jpg")
        analyze_orion_image_nra_scoring("images/output/top-right.jpg")
        analyze_orion_image_nra_scoring("images/output/upper-right.jpg")
        analyze_orion_image_nra_scoring("images/output/lower-right.jpg")
        analyze_orion_image_nra_scoring("images/output/bottom-right.jpg")
        analyze_orion_image_nra_scoring("images/output/bottom-mid.jpg")
        analyze_orion_image_nra_scoring("images/output/bottom-left.jpg")
        analyze_orion_image_nra_scoring("images/output/lower-left.jpg")
        analyze_orion_image_nra_scoring("images/output/upper-left.jpg")
        analyze_orion_image_nra_scoring("images/output/top-left.jpg")
    # Create variables to store the score and x count
    global score, x_count
    score = 100
    x_count = 0

    # Update the score and x count from the saved target CSV file
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                score -= int(row[1])
                x_count += int(row[2])
            line_count += 1
    
    # If a global data CSV doesn't exist, create it
    if not os.path.exists(str(os.getcwd()) +"/data/data.csv"):
        create_csv()

    # Save the target's basic info to the global data CSV
    with open("data/data.csv", 'a', newline="") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([name_var.get(), day_var.get() + " " + month_var.get() + " " + year_var.get(), target_num_var.get(), score, x_count])
                csvfile.close()

    main_label.config(text="Done") # Update main label

    # Enable the "Show Output" menu item
    # If any menu items have been added above this, make sure to recount them to get the correct index
    # Counting starts at zero.
    filemenu.entryconfigure(1, state=NORMAL)
    
    if not is_opening_folder:
        if individual_output_type_var.get() == "tkinter":
            # If the user uses the new analysis window, open it
            # There is no need to show the output here, instead, if it is needed,
            # it will be shown when the Finish button is pressed in the analysis window
            open_analysis_window()
        elif show_output_when_finished_var.get():
            show_output() # Otherwise, show the output now that analysis has finished

# Shows the results of the program in a separate window and provides buttons for opening CSV files
def show_output():
    """Shows the most recently saved results of the analysis in a new window."""
    main_label.config(text="Showing output") # Update main label

    #region Create window
    show_output_window = tk.Toplevel(root)
    show_output_window.minsize(525,750)
    show_output_window.geometry("525x750")
    show_output_window.tk.call('wm', 'iconphoto', show_output_window._w, tk.PhotoImage(file='assets/icon.png'))
    show_output_window.title("Target Analysis")
    #endregion

    #region Create frames
    # Only buttons and labels go in the top frame
    output_top_frame = ttk.Frame(show_output_window)
    output_top_frame.pack(side=TOP, fill=X, expand=True, pady=10)

    # Target images are shown in the bottom frame
    output_bottom_frame = ttk.Frame(show_output_window)
    output_bottom_frame.pack(side=TOP, fill=X)
    #endregion

    #region Create buttons and info at the top
    # Create a button to open the target CSV file
    open_target_csv_button = ttk.Button(output_top_frame, text="Open target CSV", command=lambda: open_file('"' + os.getcwd() + "/" + csv_name + '"'))
    open_target_csv_button.grid(row=0, column=0)
    output_top_frame.grid_columnconfigure(0, weight=1)
    
    # Create a label for the score
    score_label = ttk.Label(output_top_frame, text=str(score) + "-" + str(x_count) + "X", font='bold')
    score_label.grid(row=0, column=1)
    output_top_frame.grid_columnconfigure(1, weight=1)

    # Create a button to open the global data CSV file
    open_data_csv_button = ttk.Button(output_top_frame, text="Open data CSV", command=lambda: open_file('"' + os.getcwd() + "/data/data.csv" + '"'))
    open_data_csv_button.grid(row=0, column=2)
    output_top_frame.grid_columnconfigure(2, weight=1)
    #endregion

    #region Create canvases and images for each bull
    top_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    top_left_canvas.grid(row = 0, column = 0)

    global top_left_output
    top_left_output = ImageTk.PhotoImage(Image.open("images/output/top-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    top_left_canvas.create_image(0, 0, anchor="nw", image=top_left_output)

    upper_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    upper_left_canvas.grid(row = 1, column = 0)

    global upper_left_output
    upper_left_output = ImageTk.PhotoImage(Image.open("images/output/upper-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    upper_left_canvas.create_image(0, 0, anchor="nw", image=upper_left_output)

    lower_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    lower_left_canvas.grid(row = 2, column = 0)

    global lower_left_output
    lower_left_output = ImageTk.PhotoImage(Image.open("images/output/lower-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    lower_left_canvas.create_image(0, 0, anchor="nw", image=lower_left_output)

    bottom_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    bottom_left_canvas.grid(row = 3, column = 0)

    global bottom_left_output
    bottom_left_output = ImageTk.PhotoImage(Image.open("images/output/bottom-left.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    bottom_left_canvas.create_image(0, 0, anchor="nw", image=bottom_left_output)

    top_mid_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    top_mid_canvas.grid(row = 0, column = 1)

    global top_mid_output
    top_mid_output = ImageTk.PhotoImage(Image.open("images/output/top-mid.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    top_mid_canvas.create_image(0, 0, anchor="nw", image=top_mid_output)

    bottom_mid_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    bottom_mid_canvas.grid(row = 3, column = 1)

    global bottom_mid_output
    bottom_mid_output = ImageTk.PhotoImage(Image.open("images/output/bottom-mid.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    bottom_mid_canvas.create_image(0, 0, anchor="nw", image=bottom_mid_output)

    top_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    top_right_canvas.grid(row = 0, column = 2)

    global top_right_output
    top_right_output = ImageTk.PhotoImage(Image.open("images/output/top-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    top_right_canvas.create_image(0, 0, anchor="nw", image=top_right_output)

    upper_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    upper_right_canvas.grid(row = 1, column = 2)

    global upper_right_output
    upper_right_output = ImageTk.PhotoImage(Image.open("images/output/upper-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    upper_right_canvas.create_image(0, 0, anchor="nw", image=upper_right_output)

    lower_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    lower_right_canvas.grid(row = 2, column = 2)

    global lower_right_output
    lower_right_output = ImageTk.PhotoImage(Image.open("images/output/lower-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    lower_right_canvas.create_image(0, 0, anchor="nw", image=lower_right_output)

    bottom_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    bottom_right_canvas.grid(row = 3, column = 2)

    global bottom_right_output
    bottom_right_output = ImageTk.PhotoImage(Image.open("images/output/bottom-right.jpg-output.jpg").resize((170, 170), Image.ANTIALIAS))
    bottom_right_canvas.create_image(0, 0, anchor="nw", image=bottom_right_output)
    #endregion

# Open the working folder in Explorer
# TODO Make this work on any operating system
def show_folder(path):
    """Runs the explorer to the path given

    Args:
        path (str): where to navigate to in explorer
    """    
    print("Opening folder: " + path)
    main_label.config(text="Opening folder... ONLY WORKS ON WINDOWS")
    os.system("explorer " + '"' + path + '"') # Run a system command to open the folder using Explorer (Windows only)
    main_label.config(text="Working directory opened in Explorer") # Update the main label

# Open documentation with associated viewer
def open_file(file):
    main_label.config(text="Opening file " + str(file)) # Update the main label
    os.system(file) # Run a system command to open the file using the default viewer (should work on any operating system)

# Ensures that an image/output directory is available to save images
def check_output_dir():
    path = os.getcwd() + "/images/output" # Store the path to the output directory
    # If the output directory does not exist, create it
    if os.path.isdir(path) == False:
        os.mkdir(path)
    # Otherwise, nothing needs to be done

# Show analysis output for each image
def open_analysis_window():
    # Load all of the images that have been saved from analysis
    def load_images():
        # Create a list of images
        global output_images
        global output_image_names
        output_images = []
        output_image_names = []
        # os.listdir returns a list of the files in the directory
        for file in os.listdir("images/output"):
            # Output images are saved as such: <original image name>-output.png
            if file.endswith("output.jpg"):
                output_images.append(ImageTk.PhotoImage(Image.open("images/output/" + file).resize((600, 600), Image.ANTIALIAS))) # Load the image as a tkinter photo image and add it to the list
                output_image_names.append(file) # Add the image name to the list
        
        # Prepare image names lists for use by ordering them in a clockwise fashion, starting with the top middle target image.
        # Define the correct order for the list
        clockwise_order = {"top-mid.jpg-output.jpg" : 0, 
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
        sorted_zipped = sorted(zip(output_images, output_image_names), key=lambda d: clockwise_order[d[1]])
        # Unzip the sorted list into images and image names
        output_images = [x for x, y in sorted_zipped]
        output_image_names = [y for x, y in sorted_zipped]
        # Create friendly names for use in the GUI by removing the file extension and "-output" from the image name,
        # replacing the hyphens with spaces and capitalizing the first letter of each word.
        global output_friendly_names
        output_friendly_names = [(y.split(".jpg-output.jpg")[0]).replace("-", " ").capitalize() for x, y in sorted_zipped]

    # Delete everything on the analysis canvas
    def clear_canvas():
        analysis_canvas.delete("all")

    # Shows the indexth image in the output_images list
    def show_image(index):
        analysis_canvas.create_image(0, 0, anchor="nw", image=output_images[index]) # Create the image on the canvas
        analysis_top_label.config(text=output_friendly_names[index]) # Update the top label with the friendly name of the image

    # Advance to the next image in the output_images list if allowed
    def on_next_button_pressed():
        global image_index
        if image_index < len(output_images) - 1:
            image_index += 1
            clear_canvas()
            show_image(image_index)
        update_buttons()

    # Move back to the previous image in the output_images list if allowed
    def on_back_button_pressed():
        global image_index
        if image_index > 0:
            image_index -= 1
            clear_canvas()
            show_image(image_index)
        update_buttons()

    # Close the analysis window and show the output window if enabled
    def on_finish_button_pressed():
        analysis_window.destroy()
        if show_output_when_finished_var.get():
            show_output()

    # Update the buttons to show the correct state based on the current image index
    def update_buttons():
        if image_index == 0:
            analysis_back_button.config(state=DISABLED) # Disable the back button if the first image is showing
        else:
            analysis_back_button.config(state=NORMAL) # Enable the back button if the first image is not showing

        if image_index == len(output_images)-1:
            analysis_next_button.config(text="Finish", style="Accent.TButton", command=on_finish_button_pressed) # If the last image is showing, change the next button to say "Finish" and make it an accent button (blue) for emphasis
        else:
            analysis_next_button.config(state=NORMAL, text="Next", style="Button.TButton") # If the last image is not showing, change the next button to say "Next" and make it a normal button

    #region Create the analysis window
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Target Analysis")
    analysis_window.minsize(width=600, height=690)
    analysis_window.geometry("600x690")
    analysis_window.tk.call('wm', 'iconphoto', analysis_window._w, tk.PhotoImage(file='assets/icon.png'))
    #endregion

    #region Create frames
    # Top frame shows the image name
    analysis_top_frame = ttk.Frame(analysis_window)
    analysis_top_frame.pack(side=TOP, fill=X)

    # Images frame holds the canvas with the images
    analysis_images_frame = ttk.Frame(analysis_window)
    analysis_images_frame.pack(side=TOP, fill=X)

    # Bottom frame holds the buttons
    analysis_bottom_frame = ttk.Frame(analysis_window)
    analysis_bottom_frame.pack(side=BOTTOM, fill=X)
    #endregion

    #region Create top label
    analysis_top_label = ttk.Label(analysis_top_frame, text="Analysis", font="bold")
    analysis_top_label.pack(pady=10)
    #endregion

    #region Create canvas
    analysis_canvas = tk.Canvas(analysis_images_frame, width=600, height=600)
    analysis_canvas.pack()
    #endregion

    #region Create buttons
    analysis_next_button = ttk.Button(analysis_bottom_frame, text="Next", command=on_next_button_pressed)#, style="Accent.TButton")
    analysis_next_button.pack(side=RIGHT, padx=5, pady=5)

    analysis_back_button = ttk.Button(analysis_bottom_frame, text="Back", command=on_back_button_pressed)#, style="Accent.TButton")
    analysis_back_button.pack(side=LEFT, padx=5, pady=5)
    #endregion

    #Show first image
    global image_index
    image_index = 0
    load_images()
    clear_canvas()
    show_image(image_index)
    update_buttons()

# Create CSV file set up for the global data csv
def create_csv():
    # Open the CSV file
    with open('data/data.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) # Create a filewriter
        filewriter.writerow(['Name', 'Date', 'Target Number', 'Score','X']) # Write the header row
        csvfile.close() # Close the file
    main_label.config(text="Created CSV data file") # Update the main label

# --------------------------- Open folder functions -------------------------- #

# Opens and analyzes all files in a folder (more complex than Orion because it has to distinguish between left and right images)
def open_folder():
    global is_opening_folder
    is_opening_folder = True # Set a flag to indicate that the folder is being opened
    # Temporarily save the show_output_when_finished_var to restore after the function is done
    # Then set it to false so that the output is not shown (because for large folders it could take a while)
    show_output_when_finished_backup = show_output_when_finished_var.get()
    show_output_when_finished_var.set(False)

    main_label.config(text="Analyzing folder. This could take a while.") # Update the main label

    folder = filedialog.askdirectory() # Get the folder to open
    file_num = 0 # Keep track of how many files have been opened
    
    # os.listdir() returns a list of all files in the folder
    for file in os.listdir(folder):
        # Ignore files that are not images
        if file.endswith(".jpeg") or file.endswith(".jpg"):
            path = folder + "/" + file # Get the path to the file
            set_info_from_file(file) # Set the info from the file (correct naming is important for this operation)
            file_image = cv2.imread(path) # Open the image
            # Check if the image is a left or right image
            if "left" in file:
                crop_left(file_image)
            elif "right" in file:
                crop_right(file_image)
            
            file_num += 1 # Increment the file number

            # For every two files opened, analyze the target
            # Again, it is imperative that the naming convention is correct
            # See the README for more information
            if file_num == 2:
                analyze_target("nra")
                file_num = 0 # Reset the file number and continue
    main_label.config(text="Done. Open the /data folder to view results") # Update the main label
    show_output_when_finished_var.set(show_output_when_finished_backup) # Revert the show_output_when_finished_var to its original value
    is_opening_folder = False # Set a flag to indicate that the folder is being opened
    show_folder(os.getcwd() + "\data") # Open the data folder in Explorer

# Opens and analyzes all files in a folder
def open_folder_orion():
    global tab_control
    global is_opening_folder
    is_opening_folder = True # Keep track of whether or not the folder is being opened
    # Temporarily save the show_output_when_finished_var to restore after the function is done
    # Then set it to false so that the output is not shown (because for large folders it could take a while)
    show_output_when_finished_backup = show_output_when_finished_var.get()
    show_output_when_finished_var.set(False)

    main_label.config(text="Analyzing folder. This could take a while.") # Update the main label

    folder = filedialog.askdirectory() # Get the folder to open
    
    # os.listdir() returns a list of all files in the folder
    for file in os.listdir(folder):
        # Ignore files that are not images
        if file.endswith(".jpeg") or file.endswith(".jpg"):
            path = folder + "/" + file # Get the path to the file
            set_info_from_file(file) # Set the info from the file (correct naming is important for this operation)
            file_image = cv2.imread(path) # Open the image for OpenCV
            crop_orion(file_image) # Crop the image
            if tab_control.index("current") == 1: # If the tab is the Orion tab
                analyze_target("orion") # Analyze the target
            elif tab_control.index("current") == 2: # If the tab is the Orion as NRA tab
                analyze_target("orion-nrascoring") # Analyze the target
    
    show_output_when_finished_var.set(show_output_when_finished_backup) # Revert the show_output_when_finished_var to its original value
    is_opening_folder = False # Keep track of whether or not the folder is being opened
    show_folder(os.getcwd() + "\data") # Open the data folder in Explorer

# Allows viewing of trends from existing data files
def show_trends():
    main_label.config(text="Showing trends window") # Update the main label

    #region Create window
    trends_window = tk.Toplevel(root)
    trends_window.minsize(250,100)
    trends_window.geometry("250x100")
    trends_window.tk.call('wm', 'iconphoto', trends_window._w, tk.PhotoImage(file='assets/icon.png'))
    trends_window.title("Target Analysis")
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
        frame = ttk.Frame(trends_window)
        frame.pack(pady=5)

        trends_window.geometry("250x300") # Resize the window to accomodate the data display

        # Create a label for a header
        most_missed_label = ttk.Label(frame, text="Most missed is highest number")
        most_missed_label.grid(row=0, column=0, columnspan=3)

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
        data_csv = filedialog.askopenfilename() # Get the CSV file to open (this can be a backup to accomodate for multiple shooters)

        # Create some arrays for relevant data
        dates = []
        scores = []
        x_count = []

        # Open the CSV file
        with open(data_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',') # Create a CSV reader
            line_count = 0 # Keep track of the line number
            for row in csv_reader:
                # Ignore the header row
                if line_count != 0:
                    dates.append(row[1]) # The dates are in the second column
                    scores.append(row[3]) # The scores are in the fourth column
                    x_count.append(row[4]) # The x_count are in the fifth column
                line_count += 1 # Increment the line number
            csv_file.close() # Close the file
        
        # Zip the data together, with the dates first
        # Then sort the data using the date as the key
        sorted_zipped = sorted(zip(dates,scores,x_count), key=lambda date: datetime.datetime.strptime(date[0], "%d %B %Y"))

        # Unpack the data back into separate lists
        dates,scores,x_count = map(list,zip(*sorted_zipped))

        # Convert the scores and x_count back
        scores = list(map(int, scores))
        x_count = list(map(int, x_count))

        # Create some matplotlib plots to show data
        fig,axs = plt.subplots(2)

        # Plot the scores and x_count on separate graphs
        axs[0].plot(dates,scores, marker='o', color = 'blue')
        axs[1].plot(dates,x_count, marker='x', color = 'orange')

        # Create a label for each point for the scores graph
        for x,y in zip(dates,scores):
            label = y
            axs[0].annotate(label, # this is the text
                        (x,y), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(-15,0), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center

        # Create a label for each point for the x_count graph
        for x,y in zip(dates,x_count):
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
    load_folder_button = ttk.Button(trends_window, text="Load Folder (for most missed)", command=showMostMissed)
    load_folder_button.pack(padx=10, pady=10)

    # Create a button to load a global data CSV (for one shooter) to show improvement over time
    load_csv_button = ttk.Button(trends_window, text="Load CSV (for graph)", command=showTrendGraph)
    load_csv_button.pack(padx=10, pady=0)

# ---------------------------- File info funtions ---------------------------- #

# Sets file options by parsing a correctly-named target         
def set_info_from_file(file):
    filename = os.path.basename(file) # Get the filename alone in case it is given a full path
    
    filename_without_extension = os.path.splitext(filename)[0] # get the filename without the extension

    day_var.set(filename[0:2]) # Set the day

    year_var.set(filename[5:9]) # Set the year

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

    month_var.set(month) # Set the month

    target_num_var.set(filename_without_extension[-1]) # Set the target number

    # The final section of the filename can be any length and it is "left" or "right" for NRA A-17 targets
    # However, Orion targets use only one scan so that space can hold the shooter's name
    # This is a kind of hacky way to determine if this is an Orion target
    if tab_control.index("current") == 1 or tab_control.index("current") == 2:
        name_var.set(filename[9:-6])

    # Update the main label
    main_label.config(text="Set date to: " + month_var.get() + " " + day_var.get() + ", " + year_var.get() + " and target number " + target_num_var.get())

# Sets file options from today's date
def set_info_from_today():
    today = datetime.datetime.now() # Get today's date

    month_var.set(today.strftime("%B")) # Set the month from the date
    day_var.set(today.strftime("%d")) # Set the day from the date
    year_var.set(today.strftime("%Y")) # Set the year from the date

    target_num_var.set("1") # Default the target number to 1

    # Update the main label
    main_label.config(text="Set date to: " + month_var.get() + " " + day_var.get() + ", " + year_var.get() + " and target number 1")

# ----------------------------- Bubbles functions ---------------------------- #

# Sets shooter name from bubbled in initials on Orion targets
def set_name_from_bubbles(image):
    check_output_dir()

    DEFAULT_RADIUS = 15

    #region Crop image to only include the bubble zones
    h=int((250/3507)*image.shape[0])
    w=int((1135/2550)*image.shape[1])
    y=0
    x=int((1415/2550)*image.shape[1])
    crop = image[y:y+h, x:x+w]

    def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        image (cv2 image): image to be resized
        width (int): width of resized image, None for automatic
        height (int): height of resized image, None for automatic
        inter (cv2 interpolation): interpolation method
        """
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=inter)
        return resized

    crop = image_resize(crop, width=1135, height=250) # Resize image to fit the coordinate system that the algorithm uses later
    output = crop.copy() # Make a copy for later
    #endregion

    #region Preprocess the image for circle detection
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    #endregion

    #region Identify circles in the image
    circles = cv2.HoughCircles(opening, cv2.HOUGH_GRADIENT, 1, 10, param1=30, param2=20, minRadius=10, maxRadius=50) # Detect circles
    circles = np.uint16(np.around(circles)) # Dunno what this does but it works
    #endregion

    # Draw circle and center of circle on image
    def draw_circle_points(image, a, b, r):
        cv2.circle(image, (a, b), r, (0, 255, 0), 2)
        cv2.circle(image, (a, b), 1, (0, 0, 255), 2)

    # Based on coordinates of the circle, return a capital letter A-Z
    def classify_letter(x, y):
        # Letters 
        # A B C D E F G H I J K L M on top row
        # N O P Q R S T U V W X Y Z on bottom row

        letter_x_positions = {
            0: (60,100),
            1: (105, 140),
            2: (145, 180),
            3: (190, 225),
            4: (230, 270),
            5: (275, 305),
            6: (310, 350),
            7: (355, 395),
            8: (400, 435),
            9: (440, 475),
            10: (480, 520),
            11: (525, 560),
            12: (565, 600)
        }

        y_positions = {
            0: (95,135),
            1: (145, 185),
        }

        letter_key = None
        for key, value in letter_x_positions.items():
            if(value[0] <= x and x <= value[1]):
                letter_key = key
        
        y_position_key = None
        for key, value in y_positions.items():
            if(value[0] <= y and y <= value[1]):
                y_position_key = key
        
        if(letter_key is None or y_position_key is None):
            return None

        letters_dictionary = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H",
            8: "I",
            9: "J",
            10: "K",
            11: "L",
            12: "M",
            13: "N",
            14: "O",
            15: "P",
            16: "Q",
            17: "R",
            18: "S",
            19: "T",
            20: "U",
            21: "V",
            22: "W",
            23: "X",
            24: "Y",
            25: "Z"
        }

        both_rows_key = letter_key + (y_position_key * 13)
        letter = letters_dictionary[both_rows_key]
        return letter

    # Check if region around point is filled
    def check_if_filled(x, y, r):
        check_points_x = range(x-r, x+r)
        check_points_y = range(y-r, y+r)
        values = []
        for x in check_points_x:
            for y in check_points_y:
                values.append(thresh[y][x])
        total = sum(values) / len(values)
        if total <= 100:
            return True
        return False

    letters = []

    for pt in circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        draw_circle_points(output, a, b, r)

        if check_if_filled(a, b, DEFAULT_RADIUS):
            letter = classify_letter(a, b)
            # Optionally put the detected letter on the image
            if letter is not None:
                cv2.putText(output, letter, (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            letters.append(letter)
            #print(letter)

    cv2.imwrite("images/output/bubbles.jpg", output)

    #print(letters)

    def initals_to_name(letter_list):
        letters = sorted(letter_list) # Sort the given list of letters
        letters_string = "".join(letters) # and convert it to a string

        initals_list, names_list = load_names_config()

        for i in range(len(initals_list)):
            initals_list[i] = "".join(sorted(initals_list[i]))

        name_index = initals_list.index(letters_string)
        name = names_list[name_index]
        return name

    name = initals_to_name(letters)

    if name != None: name_var.set(name)

# Creates a default names config file
def create_names_config():
    config =  ConfigParser()

    config.read('names.ini')

    config.add_section('index')
    config.set('index', 'index', '1')

    config.add_section('initials')
    config.set('initials', '0', 'SK')

    config.add_section('names')
    config.set('names', '0', 'Sigmond')

    # Write the changes to the config file
    with open('names.ini', 'w') as f:
        config.write(f)

# Loads initials and names from names.ini config file and and puts them into respective lists
def load_names_config():
    config =  ConfigParser()
    config.read('names.ini')

    index = config.getint('index', 'index')

    initials_list = []
    names_list = []
    for i in range(index):
        initials_list.append(config.get('initials', str(i)))
        names_list.append(config.get('names', str(i)))
    
    return initials_list, names_list

# -------------------------- Miscellaneous functions ------------------------- #

# Delete all files in the data folder
def clear_data():
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

    main_label.config(text="/data and /images/output directories cleared") # Update the main label

# Open the settings window
def open_settings():
    # If the settings window is going to be closed, save the changes and destroy the window
    def on_close_settings():
        update_config()
        settings_window.destroy()

    # Update the settings using the config-backup.ini file, which should never be changed
    def revert_settings():
        update_settings_from_config("config-backup.ini")
        update_config()

    def open_names_file():
        path = "'" + str(os.getcwd()) + '/' + 'names.ini' + "'"
        print(path)
        os.system("notepad " + path)

    main_label.config(text="Showing settings window") # Update the main label

    #region Create settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Target Analysis")
    settings_window.minsize(width=600, height=640)
    settings_window.geometry("600x640")
    settings_window.tk.call('wm', 'iconphoto', settings_window._w, tk.PhotoImage(file='assets/icon.png'))
    #endregion

    #region Create frames
    # Each global setting has its own frame
    settings_top_frame = ttk.Frame(settings_window)
    settings_top_frame.pack(side=TOP, expand=False, pady=5, fill=X)

    settings_global_label_frame = ttk.Frame(settings_window)
    settings_global_label_frame.pack(side=TOP, fill=X)

    settings_dpi_frame = ttk.Frame(settings_window)
    settings_dpi_frame.pack(side=TOP, fill=X, padx=5)

    settings_show_output_frame = ttk.Frame(settings_window)
    settings_show_output_frame.pack(side=TOP, fill=X, padx=5)

    settings_indivdual_output_frame = ttk.Frame(settings_window)
    settings_indivdual_output_frame.pack(side=TOP, fill=X, padx=5)

    settings_dark_mode_frame = ttk.Frame(settings_window)
    settings_dark_mode_frame.pack(side=TOP, fill=X, padx=5)

    settings_global_separator = ttk.Separator(settings_window, orient=HORIZONTAL)
    settings_global_separator.pack(side=TOP, fill=X, pady=5)

    settings_bottom_frame = ttk.Frame(settings_window)
    settings_bottom_frame.pack(side=TOP, fill=X)

    settings_buttons_frame = ttk.Frame(settings_window)
    settings_buttons_frame.pack(side=BOTTOM, fill=X)

    # Notebook allows for a tabbed view
    settings_tab_control = ttk.Notebook(settings_bottom_frame)

    settingstab1nraa17 = ttk.Frame(settings_tab_control)
    settingstab2orion = ttk.Frame(settings_tab_control)
    settingstab3orionDPI2 = ttk.Frame(settings_tab_control)
    settingstab4names = ttk.Frame(settings_tab_control)

    settings_tab_control.add(settingstab1nraa17, text ='NRA A-17')
    settings_tab_control.add(settingstab2orion, text ='NRA/USAS-50 Orion 300dpi')
    settings_tab_control.add(settingstab3orionDPI2, text ='NRA/USAS-50 Orion 600dpi')
    settings_tab_control.add(settingstab4names, text ='Names')

    settings_tab_control.pack(side=TOP, fill=X, padx=10, pady=5)

    save_separator = ttk.Separator(settings_buttons_frame, orient=HORIZONTAL)
    save_separator.pack(side=TOP, fill=X)

    revert_button = ttk.Button(settings_buttons_frame, text="Revert settings to default", command=revert_settings)
    revert_button.pack(side=LEFT, pady=5, padx=5)

    save_button = ttk.Button(settings_buttons_frame, text="Save Settings", command=update_config)
    save_button.pack(side=RIGHT, pady=5, padx=5)
    #endregion

    #region Create top label
    # Header label
    settings_label1 = ttk.Label(settings_top_frame, text="Settings", font='bold')
    settings_label1.pack(side=TOP)
    # Warning label
    settings_label2 = ttk.Label(settings_top_frame, text="⚠️ Change these only if the software does not work properly ⚠️")
    settings_label2.pack(side=TOP)
    # Separator
    label_separator = ttk.Separator(settings_top_frame, orient=HORIZONTAL)
    label_separator.pack(side=TOP, fill=X, pady=(5, 0))
    #endregion

    #region Create top widgets
    # Global settings label
    settings_label1 = ttk.Label(settings_global_label_frame, text="Global settings", font = 'bold')
    settings_label1.pack()

    # 300dpi / 600dpi selection buttons
    dpi_button300 = ttk.Radiobutton(settings_dpi_frame, text="300 dpi scanner", variable=dpi_var, value=1)
    dpi_button300.grid(row=1, column=0)
    dpi_button600 = ttk.Radiobutton(settings_dpi_frame, text="600 dpi scanner", variable=dpi_var, value=2)
    dpi_button600.grid(row=1, column=1)

    # Show output when finished switch
    global show_output_when_finished_var
    show_output_when_finished_check_button_settings = ttk.Checkbutton(settings_show_output_frame, text='Show output when finished', style='Switch.TCheckbutton', variable=show_output_when_finished_var, onvalue=True, offvalue=False)
    show_output_when_finished_check_button_settings.grid(column=0, row=0)

    # Use new analysis display switch (tkinter version)
    global individual_output_type_var
    individual_output_type_check_button_settings = ttk.Checkbutton(settings_indivdual_output_frame, text='Use new analysis display', style='Switch.TCheckbutton', variable=individual_output_type_var, onvalue="tkinter", offvalue="legacy")
    individual_output_type_check_button_settings.grid(column=0, row=0)

    # Dark mode switch
    # TODO: Figure out why dark mode makes labels more padded
    global dark_mode_var
    dark_mode_checkbutton = ttk.Checkbutton(settings_dark_mode_frame, text='Use dark theme', style='Switch.TCheckbutton', variable=dark_mode_var, onvalue=True, offvalue=False, command=update_dark_mode)
    dark_mode_checkbutton.grid(column=0, row=0)
    #endregion

    #region Create NRA A-17 widgets
    # Create a header label
    settings_label2 = ttk.Label(settingstab1nraa17, text="NRA A-17 settings" , font='bold')
    settings_label2.grid(row=0, column=0, columnspan=2)

    # The settings should be self explanatory
    # But if you aren't sure, check the **Tuning Overview** in README.md
    nra_kernal_size_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Kernel Size")
    nra_kernal_size_label.grid(row=1, column=0)
    nra_kernal_size_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_kernal_size)
    nra_kernal_size_entry.grid(row=1, column=1)

    nra_param1_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Param 1")
    nra_param1_label.grid(row=2, column=0)
    nra_param1_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_param1)
    nra_param1_entry.grid(row=2, column=1)

    nra_param2_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Param 2")
    nra_param2_label.grid(row=3, column=0)
    nra_param2_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_param2)
    nra_param2_entry.grid(row=3, column=1)

    nra_min_radius_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Min Circle Radius")
    nra_min_radius_label.grid(row=4, column=0)
    nra_min_radius_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_min_radius)
    nra_min_radius_entry.grid(row=4, column=1)

    nra_thresh_min_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Thresh Min")
    nra_thresh_min_label.grid(row=5, column=0)
    nra_thresh_min_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_thresh_min)
    nra_thresh_min_entry.grid(row=5, column=1)

    nra_thresh_max_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Thresh Max")
    nra_thresh_max_label.grid(row=6, column=0)
    nra_thresh_max_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_thresh_max)
    nra_thresh_max_entry.grid(row=6, column=1)

    nra_morphology_opening_kernel_size_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Morph Kernal Size")
    nra_morphology_opening_kernel_size_label.grid(row=7, column=0)
    nra_morphology_opening_kernel_size_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_morphology_opening_kernel_size)
    nra_morphology_opening_kernel_size_entry.grid(row=7, column=1)

    nra_min_contour_area_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Min cnt area")
    nra_min_contour_area_label.grid(row=8, column=0)
    nra_min_contour_area_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_min_contour_area)
    nra_min_contour_area_entry.grid(row=8, column=1)

    nra_max_contour_area_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Max cnt area")
    nra_max_contour_area_label.grid(row=9, column=0)
    nra_max_contour_area_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_max_contour_area)
    nra_max_contour_area_entry.grid(row=9, column=1)

    nramax_hole_radius_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Max hole radius")
    nramax_hole_radius_label.grid(row=10, column=0)
    nramax_hole_radius_entry = ttk.Entry(settingstab1nraa17, textvariable=nramax_hole_radius)
    nramax_hole_radius_entry.grid(row=10, column=1)
    #endregion

    #region Create Orion widgets
    # Create a header label
    settings_label1 = ttk.Label(settingstab2orion, text="Orion settings (300dpi)" , font='bold')
    settings_label1.grid(row=0, column=0, columnspan=2)

    # Create a header label for the Orion 600dpi settigs
    settings_label_orion600 = ttk.Label(settingstab3orionDPI2, text="Orion settings (600dpi)" , font='bold')
    settings_label_orion600.grid(row=0, column=0, columnspan=2)

    # The settings should be self explanatory
    # But if you aren't sure, check the **Tuning Overview** in README.md
    # Settings below include both 300dpi (dpi1) and 600dpi (dpi2) settings
    # They are simply sorted into either settingstab2orion (dpi1) or settingstab3orionDPI2 (dpi2)

    orion_kernel_size_dpi1_label = ttk.Label(settingstab2orion, text="Orion Kernel Size dpi 1")
    orion_kernel_size_dpi1_label.grid(row=1, column=0)
    orion_kernel_size_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_kernel_size_dpi1)
    orion_kernel_size_dpi1_entry.grid(row=1, column=1)

    orion_kernel_size_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion Kernel Size dpi 2")
    orion_kernel_size_dpi2_label.grid(row=2, column=0)
    orion_kernel_size_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_kernel_size_dpi2)
    orion_kernel_size_dpi2_entry.grid(row=2, column=1)

    orion_param1_dpi1_label = ttk.Label(settingstab2orion, text="Orion Param1 dpi 1")
    orion_param1_dpi1_label.grid(row=3, column=0)
    orion_param1_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_param1_dpi1)
    orion_param1_dpi1_entry.grid(row=3, column=1)

    orion_param2_dpi1_label = ttk.Label(settingstab2orion, text="Orion Param2 dpi 1")
    orion_param2_dpi1_label.grid(row=4, column=0)
    orion_param2_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_param2_dpi1)
    orion_param2_dpi1_entry.grid(row=4, column=1)

    orion_param1_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion Param1 dpi 2")
    orion_param1_dpi2_label.grid(row=5, column=0)
    orion_param1_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_param1_dpi2)
    orion_param1_dpi2_entry.grid(row=5, column=1)

    orion_param2_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion Param2 dpi 2")
    orion_param2_dpi2_label.grid(row=6, column=0)
    orion_param2_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_param2_dpi2)
    orion_param2_dpi2_entry.grid(row=6, column=1)

    orion_min_radius_dpi1_label = ttk.Label(settingstab2orion, text="Orion MinRadius dpi 1")
    orion_min_radius_dpi1_label.grid(row=7, column=0)
    orion_min_radius_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_min_radius_dpi1)
    orion_min_radius_dpi1_entry.grid(row=7, column=1)

    orion_min_radius_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion MinRadius dpi 2")
    orion_min_radius_dpi2_label.grid(row=8, column=0)
    orion_min_radius_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_min_radius_dpi2)
    orion_min_radius_dpi2_entry.grid(row=8, column=1)

    orion_thresh_min_label = ttk.Label(settingstab2orion, text="Orion thresh min")
    orion_thresh_min_label.grid(row=9, column=0)
    orion_thresh_min_entry = ttk.Entry(settingstab2orion, textvariable=orion_thresh_min)
    orion_thresh_min_entry.grid(row=9, column=1)

    orion_thresh_max_label = ttk.Label(settingstab2orion, text="Orion thresh max")
    orion_thresh_max_label.grid(row=10, column=0)
    orion_thresh_max_entry = ttk.Entry(settingstab2orion, textvariable=orion_thresh_max)
    orion_thresh_max_entry.grid(row=10, column=1)

    orion_thresh_min_label_dpi2 = ttk.Label(settingstab3orionDPI2, text="Orion thresh min")
    orion_thresh_min_label_dpi2.grid(row=9, column=0)
    orion_thresh_min_entry_dpi2 = ttk.Entry(settingstab3orionDPI2, textvariable=orion_thresh_min)
    orion_thresh_min_entry_dpi2.grid(row=9, column=1)

    orion_thresh_max_label_dpi2 = ttk.Label(settingstab3orionDPI2, text="Orion thresh max")
    orion_thresh_max_label_dpi2.grid(row=10, column=0)
    orion_thresh_max_entry_dpi2 = ttk.Entry(settingstab3orionDPI2, textvariable=orion_thresh_max)
    orion_thresh_max_entry_dpi2.grid(row=10, column=1)

    orion_min_contour_area_dpi1_label = ttk.Label(settingstab2orion, text="Orion min cnt area dpi 1")
    orion_min_contour_area_dpi1_label.grid(row=11, column=0)
    orion_min_contour_area_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_min_contour_area_dpi1)
    orion_min_contour_area_dpi1_entry.grid(row=11, column=1)

    orion_max_contour_area_dpi1_label = ttk.Label(settingstab2orion, text="Orion max cnt area dpi 1")
    orion_max_contour_area_dpi1_label.grid(row=12, column=0)
    orion_max_contour_area_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_max_contour_area_dpi1)
    orion_max_contour_area_dpi1_entry.grid(row=12, column=1)

    orion_min_contour_area_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion min cnt area dpi 2")
    orion_min_contour_area_dpi2_label.grid(row=13, column=0)
    orion_min_contour_area_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_min_contour_area_dpi2)
    orion_min_contour_area_dpi2_entry.grid(row=13, column=1)

    orion_max_contour_area_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion max cnt area dpi 2")
    orion_max_contour_area_dpi2_label.grid(row=14, column=0)
    orion_max_contour_area_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_max_contour_area_dpi2)
    orion_max_contour_area_dpi2_entry.grid(row=14, column=1)

    orionmax_hole_radius_dpi1_label = ttk.Label(settingstab2orion, text="Orion min hole rad dpi 1")
    orionmax_hole_radius_dpi1_label.grid(row=15, column=0)
    orionmax_hole_radius_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orionmax_hole_radius_dpi1)
    orionmax_hole_radius_dpi1_entry.grid(row=15, column=1)

    orionmax_hole_radius_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion min hole rad dpi 2")
    orionmax_hole_radius_dpi2_label.grid(row=16, column=0)
    orionmax_hole_radius_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionmax_hole_radius_dpi2)
    orionmax_hole_radius_dpi2_entry.grid(row=16, column=1)
    #endregion

    #region Create names
    # Frame is named 'settingstab4names'
    # TODO: Add built in support for editing names file
    names_label = ttk.Label(settingstab4names, text="Initials to Names mapping", font=BOLD)
    names_label.pack(padx=5, pady=5, fill=X)
    description_label = ttk.Label(settingstab4names, text="Initials and Names are stored in an INI file which must be manually edited.")
    description_label.pack(padx=5, pady=5, fill=X)
    namesButton = ttk.Button(settingstab4names, text="Open names file", command=open_names_file)
    namesButton.pack(padx=5, pady=5)
    names_info_label = ttk.Label(settingstab4names, text="Make sure to set the index to the number of names in the list (key + 1)")
    names_info_label.pack(padx=5, pady=5, fill=X)
    names_info_label2 = ttk.Label(settingstab4names, text="So if the last entry is '5 = Sigmond' set 'index = 6'")
    names_info_label2.pack(padx=5, pady=5, fill=X)
    #endregion

    settings_window.protocol("WM_DELETE_WINDOW", on_close_settings) # If the settings window is closing, run the on_close_settings function

# Enables/Disables dark theme UI based on dark_mode boolean variable state
def update_dark_mode():
    # If dark mode is enabled, set the theme to dark
    if dark_mode_var.get() == True:
        root.tk.call("set_theme", "dark") # Set the theme to dark
    else:
        root.tk.call("set_theme", "light") # Set the theme to light

# --------------------------- Settings functions -------------------------- #

# Open the settings window
def open_settings():
    # If the settings window is going to be closed, save the changes and destroy the window
    def on_close_settings():
        update_config()
        settings_window.destroy()

    # Update the settings using the config-backup.ini file, which should never be changed
    def revert_settings():
        update_settings_from_config("config-backup.ini")
        update_config()

    def open_names_file():
        path = "'" + str(os.getcwd()) + '/' + 'names.ini' + "'"
        print(path)
        os.system("notepad " + path)

    main_label.config(text="Showing settings window") # Update the main label

    #region Create settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Target Analysis")
    settings_window.minsize(width=600, height=640)
    settings_window.geometry("600x640")
    settings_window.tk.call('wm', 'iconphoto', settings_window._w, tk.PhotoImage(file='assets/icon.png'))
    #endregion

    #region Create frames
    # Each global setting has its own frame
    settings_top_frame = ttk.Frame(settings_window)
    settings_top_frame.pack(side=TOP, expand=False, pady=5, fill=X)

    settings_global_label_frame = ttk.Frame(settings_window)
    settings_global_label_frame.pack(side=TOP, fill=X)

    settings_dpi_frame = ttk.Frame(settings_window)
    settings_dpi_frame.pack(side=TOP, fill=X, padx=5)

    settings_show_output_frame = ttk.Frame(settings_window)
    settings_show_output_frame.pack(side=TOP, fill=X, padx=5)

    settings_indivdual_output_frame = ttk.Frame(settings_window)
    settings_indivdual_output_frame.pack(side=TOP, fill=X, padx=5)

    settings_dark_mode_frame = ttk.Frame(settings_window)
    settings_dark_mode_frame.pack(side=TOP, fill=X, padx=5)

    settings_global_separator = ttk.Separator(settings_window, orient=HORIZONTAL)
    settings_global_separator.pack(side=TOP, fill=X, pady=5)

    settings_bottom_frame = ttk.Frame(settings_window)
    settings_bottom_frame.pack(side=TOP, fill=X)

    settings_buttons_frame = ttk.Frame(settings_window)
    settings_buttons_frame.pack(side=BOTTOM, fill=X)

    # Notebook allows for a tabbed view
    settings_tab_control = ttk.Notebook(settings_bottom_frame)

    settingstab1nraa17 = ttk.Frame(settings_tab_control)
    settingstab2orion = ttk.Frame(settings_tab_control)
    settingstab3orionDPI2 = ttk.Frame(settings_tab_control)
    settingstab4names = ttk.Frame(settings_tab_control)

    settings_tab_control.add(settingstab1nraa17, text ='NRA A-17')
    settings_tab_control.add(settingstab2orion, text ='NRA/USAS-50 Orion 300dpi')
    settings_tab_control.add(settingstab3orionDPI2, text ='NRA/USAS-50 Orion 600dpi')
    settings_tab_control.add(settingstab4names, text ='Names')

    settings_tab_control.pack(side=TOP, fill=X, padx=10, pady=5)

    save_separator = ttk.Separator(settings_buttons_frame, orient=HORIZONTAL)
    save_separator.pack(side=TOP, fill=X)

    revert_button = ttk.Button(settings_buttons_frame, text="Revert settings to default", command=revert_settings)
    revert_button.pack(side=LEFT, pady=5, padx=5)

    save_button = ttk.Button(settings_buttons_frame, text="Save Settings", command=update_config)
    save_button.pack(side=RIGHT, pady=5, padx=5)
    #endregion

    #region Create top label
    # Header label
    settings_label1 = ttk.Label(settings_top_frame, text="Settings", font='bold')
    settings_label1.pack(side=TOP)
    # Warning label
    settings_label2 = ttk.Label(settings_top_frame, text="⚠️ Change these only if the software does not work properly ⚠️")
    settings_label2.pack(side=TOP)
    # Separator
    label_separator = ttk.Separator(settings_top_frame, orient=HORIZONTAL)
    label_separator.pack(side=TOP, fill=X, pady=(5, 0))
    #endregion

    #region Create top widgets
    # Global settings label
    settings_label1 = ttk.Label(settings_global_label_frame, text="Global settings", font = 'bold')
    settings_label1.pack()

    # 300dpi / 600dpi selection buttons
    dpi_button300 = ttk.Radiobutton(settings_dpi_frame, text="300 dpi scanner", variable=dpi_var, value=1)
    dpi_button300.grid(row=1, column=0)
    dpi_button600 = ttk.Radiobutton(settings_dpi_frame, text="600 dpi scanner", variable=dpi_var, value=2)
    dpi_button600.grid(row=1, column=1)

    # Show output when finished switch
    global show_output_when_finished_var
    show_output_when_finished_check_button_settings = ttk.Checkbutton(settings_show_output_frame, text='Show output when finished', style='Switch.TCheckbutton', variable=show_output_when_finished_var, onvalue=True, offvalue=False)
    show_output_when_finished_check_button_settings.grid(column=0, row=0)

    # Use new analysis display switch (tkinter version)
    global individual_output_type_var
    individual_output_type_check_button_settings = ttk.Checkbutton(settings_indivdual_output_frame, text='Use new analysis display', style='Switch.TCheckbutton', variable=individual_output_type_var, onvalue="tkinter", offvalue="legacy")
    individual_output_type_check_button_settings.grid(column=0, row=0)

    # Dark mode switch
    # TODO: Figure out why dark mode makes labels more padded
    global dark_mode_var
    dark_mode_checkbutton = ttk.Checkbutton(settings_dark_mode_frame, text='Use dark theme', style='Switch.TCheckbutton', variable=dark_mode_var, onvalue=True, offvalue=False, command=update_dark_mode)
    dark_mode_checkbutton.grid(column=0, row=0)
    #endregion

    #region Create NRA A-17 widgets
    # Create a header label
    settings_label2 = ttk.Label(settingstab1nraa17, text="NRA A-17 settings" , font='bold')
    settings_label2.grid(row=0, column=0, columnspan=2)

    # The settings should be self explanatory
    # But if you aren't sure, check the **Tuning Overview** in README.md
    nra_kernal_size_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Kernel Size")
    nra_kernal_size_label.grid(row=1, column=0)
    nra_kernal_size_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_kernal_size)
    nra_kernal_size_entry.grid(row=1, column=1)

    nra_param1_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Param 1")
    nra_param1_label.grid(row=2, column=0)
    nra_param1_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_param1)
    nra_param1_entry.grid(row=2, column=1)

    nra_param2_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Param 2")
    nra_param2_label.grid(row=3, column=0)
    nra_param2_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_param2)
    nra_param2_entry.grid(row=3, column=1)

    nra_min_radius_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Min Circle Radius")
    nra_min_radius_label.grid(row=4, column=0)
    nra_min_radius_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_min_radius)
    nra_min_radius_entry.grid(row=4, column=1)

    nra_thresh_min_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Thresh Min")
    nra_thresh_min_label.grid(row=5, column=0)
    nra_thresh_min_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_thresh_min)
    nra_thresh_min_entry.grid(row=5, column=1)

    nra_thresh_max_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Thresh Max")
    nra_thresh_max_label.grid(row=6, column=0)
    nra_thresh_max_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_thresh_max)
    nra_thresh_max_entry.grid(row=6, column=1)

    nra_morphology_opening_kernel_size_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Morph Kernal Size")
    nra_morphology_opening_kernel_size_label.grid(row=7, column=0)
    nra_morphology_opening_kernel_size_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_morphology_opening_kernel_size)
    nra_morphology_opening_kernel_size_entry.grid(row=7, column=1)

    nra_min_contour_area_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Min cnt area")
    nra_min_contour_area_label.grid(row=8, column=0)
    nra_min_contour_area_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_min_contour_area)
    nra_min_contour_area_entry.grid(row=8, column=1)

    nra_max_contour_area_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Max cnt area")
    nra_max_contour_area_label.grid(row=9, column=0)
    nra_max_contour_area_entry = ttk.Entry(settingstab1nraa17, textvariable=nra_max_contour_area)
    nra_max_contour_area_entry.grid(row=9, column=1)

    nramax_hole_radius_label = ttk.Label(settingstab1nraa17, text="NRA A-17 Max hole radius")
    nramax_hole_radius_label.grid(row=10, column=0)
    nramax_hole_radius_entry = ttk.Entry(settingstab1nraa17, textvariable=nramax_hole_radius)
    nramax_hole_radius_entry.grid(row=10, column=1)
    #endregion

    #region Create Orion widgets
    # Create a header label
    settings_label1 = ttk.Label(settingstab2orion, text="Orion settings (300dpi)" , font='bold')
    settings_label1.grid(row=0, column=0, columnspan=2)

    # Create a header label for the Orion 600dpi settigs
    settings_label_orion600 = ttk.Label(settingstab3orionDPI2, text="Orion settings (600dpi)" , font='bold')
    settings_label_orion600.grid(row=0, column=0, columnspan=2)

    # The settings should be self explanatory
    # But if you aren't sure, check the **Tuning Overview** in README.md
    # Settings below include both 300dpi (dpi1) and 600dpi (dpi2) settings
    # They are simply sorted into either settingstab2orion (dpi1) or settingstab3orionDPI2 (dpi2)

    orion_kernel_size_dpi1_label = ttk.Label(settingstab2orion, text="Orion Kernel Size dpi 1")
    orion_kernel_size_dpi1_label.grid(row=1, column=0)
    orion_kernel_size_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_kernel_size_dpi1)
    orion_kernel_size_dpi1_entry.grid(row=1, column=1)

    orion_kernel_size_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion Kernel Size dpi 2")
    orion_kernel_size_dpi2_label.grid(row=2, column=0)
    orion_kernel_size_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_kernel_size_dpi2)
    orion_kernel_size_dpi2_entry.grid(row=2, column=1)

    orion_param1_dpi1_label = ttk.Label(settingstab2orion, text="Orion Param1 dpi 1")
    orion_param1_dpi1_label.grid(row=3, column=0)
    orion_param1_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_param1_dpi1)
    orion_param1_dpi1_entry.grid(row=3, column=1)

    orion_param2_dpi1_label = ttk.Label(settingstab2orion, text="Orion Param2 dpi 1")
    orion_param2_dpi1_label.grid(row=4, column=0)
    orion_param2_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_param2_dpi1)
    orion_param2_dpi1_entry.grid(row=4, column=1)

    orion_param1_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion Param1 dpi 2")
    orion_param1_dpi2_label.grid(row=5, column=0)
    orion_param1_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_param1_dpi2)
    orion_param1_dpi2_entry.grid(row=5, column=1)

    orion_param2_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion Param2 dpi 2")
    orion_param2_dpi2_label.grid(row=6, column=0)
    orion_param2_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_param2_dpi2)
    orion_param2_dpi2_entry.grid(row=6, column=1)

    orion_min_radius_dpi1_label = ttk.Label(settingstab2orion, text="Orion MinRadius dpi 1")
    orion_min_radius_dpi1_label.grid(row=7, column=0)
    orion_min_radius_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_min_radius_dpi1)
    orion_min_radius_dpi1_entry.grid(row=7, column=1)

    orion_min_radius_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion MinRadius dpi 2")
    orion_min_radius_dpi2_label.grid(row=8, column=0)
    orion_min_radius_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_min_radius_dpi2)
    orion_min_radius_dpi2_entry.grid(row=8, column=1)

    orion_thresh_min_label = ttk.Label(settingstab2orion, text="Orion thresh min")
    orion_thresh_min_label.grid(row=9, column=0)
    orion_thresh_min_entry = ttk.Entry(settingstab2orion, textvariable=orion_thresh_min)
    orion_thresh_min_entry.grid(row=9, column=1)

    orion_thresh_max_label = ttk.Label(settingstab2orion, text="Orion thresh max")
    orion_thresh_max_label.grid(row=10, column=0)
    orion_thresh_max_entry = ttk.Entry(settingstab2orion, textvariable=orion_thresh_max)
    orion_thresh_max_entry.grid(row=10, column=1)

    orion_thresh_min_label_dpi2 = ttk.Label(settingstab3orionDPI2, text="Orion thresh min")
    orion_thresh_min_label_dpi2.grid(row=9, column=0)
    orion_thresh_min_entry_dpi2 = ttk.Entry(settingstab3orionDPI2, textvariable=orion_thresh_min)
    orion_thresh_min_entry_dpi2.grid(row=9, column=1)

    orion_thresh_max_label_dpi2 = ttk.Label(settingstab3orionDPI2, text="Orion thresh max")
    orion_thresh_max_label_dpi2.grid(row=10, column=0)
    orion_thresh_max_entry_dpi2 = ttk.Entry(settingstab3orionDPI2, textvariable=orion_thresh_max)
    orion_thresh_max_entry_dpi2.grid(row=10, column=1)

    orion_min_contour_area_dpi1_label = ttk.Label(settingstab2orion, text="Orion min cnt area dpi 1")
    orion_min_contour_area_dpi1_label.grid(row=11, column=0)
    orion_min_contour_area_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_min_contour_area_dpi1)
    orion_min_contour_area_dpi1_entry.grid(row=11, column=1)

    orion_max_contour_area_dpi1_label = ttk.Label(settingstab2orion, text="Orion max cnt area dpi 1")
    orion_max_contour_area_dpi1_label.grid(row=12, column=0)
    orion_max_contour_area_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orion_max_contour_area_dpi1)
    orion_max_contour_area_dpi1_entry.grid(row=12, column=1)

    orion_min_contour_area_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion min cnt area dpi 2")
    orion_min_contour_area_dpi2_label.grid(row=13, column=0)
    orion_min_contour_area_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_min_contour_area_dpi2)
    orion_min_contour_area_dpi2_entry.grid(row=13, column=1)

    orion_max_contour_area_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion max cnt area dpi 2")
    orion_max_contour_area_dpi2_label.grid(row=14, column=0)
    orion_max_contour_area_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orion_max_contour_area_dpi2)
    orion_max_contour_area_dpi2_entry.grid(row=14, column=1)

    orionmax_hole_radius_dpi1_label = ttk.Label(settingstab2orion, text="Orion min hole rad dpi 1")
    orionmax_hole_radius_dpi1_label.grid(row=15, column=0)
    orionmax_hole_radius_dpi1_entry = ttk.Entry(settingstab2orion, textvariable=orionmax_hole_radius_dpi1)
    orionmax_hole_radius_dpi1_entry.grid(row=15, column=1)

    orionmax_hole_radius_dpi2_label = ttk.Label(settingstab3orionDPI2, text="Orion min hole rad dpi 2")
    orionmax_hole_radius_dpi2_label.grid(row=16, column=0)
    orionmax_hole_radius_dpi2_entry = ttk.Entry(settingstab3orionDPI2, textvariable=orionmax_hole_radius_dpi2)
    orionmax_hole_radius_dpi2_entry.grid(row=16, column=1)
    #endregion

    #region Create names
    # Frame is named 'settingstab4names'
    # TODO: Add built in support for editing names file
    names_label = ttk.Label(settingstab4names, text="Initials to Names mapping", font=BOLD)
    names_label.pack(padx=5, pady=5, fill=X)
    description_label = ttk.Label(settingstab4names, text="Initials and Names are stored in an INI file which must be manually edited.")
    description_label.pack(padx=5, pady=5, fill=X)
    namesButton = ttk.Button(settingstab4names, text="Open names file", command=open_names_file)
    namesButton.pack(padx=5, pady=5)
    names_info_label = ttk.Label(settingstab4names, text="Make sure to set the index to the number of names in the list (key + 1)")
    names_info_label.pack(padx=5, pady=5, fill=X)
    names_info_label2 = ttk.Label(settingstab4names, text="So if the last entry is '5 = Sigmond' set 'index = 6'")
    names_info_label2.pack(padx=5, pady=5, fill=X)
    #endregion

    settings_window.protocol("WM_DELETE_WINDOW", on_close_settings) # If the settings window is closing, run the on_close_settings function

# Read settings from config file and apply them to the necessary tk vars
def update_settings_from_config(file):
    # Create a config parser
    config = ConfigParser()

    config.read(file) # Read the given config file
    
    # Set variables to the values in the config file
    dpi_var.set(config.getint("settings", "dpi"))
    dark_mode_var.set(config.getboolean("settings", "dark_mode"))
    show_output_when_finished_var.set(config.getboolean("settings", "show_output_when_finished"))
    individual_output_type_var.set(config.get('settings', 'individual_output_type'))
    use_file_info_var.set(config.getboolean("settings", "use_file_info"))
    update_dark_mode() # Apply the dark mode setting

    # Continue setting variables for the Orion targets
    orion_kernel_size_dpi1.set(config.getint("orion", "orion_kernel_size_dpi1"))
    orion_kernel_size_dpi2.set(config.getint("orion", "orion_kernel_size_dpi2"))
    orion_param1_dpi1.set(config.getfloat("orion", "orion_param1_dpi1"))
    orion_param2_dpi1.set(config.getint("orion", "orion_param2_dpi1"))
    orion_min_radius_dpi1.set(config.getint("orion", "orion_min_radius_dpi1"))
    orion_param1_dpi2.set(config.getint("orion", "orion_param1_dpi2"))
    orion_param2_dpi2.set(config.getint("orion", "orion_param2_dpi2"))
    orion_min_radius_dpi2.set(config.getint("orion", "orion_min_radius_dpi2"))
    orion_thresh_min.set(config.getint("orion", "orion_thresh_min"))
    orion_thresh_max.set(config.getint("orion", "orion_thresh_max"))
    orion_morphology_opening_kernel_size_dpi1.set(config.getint("orion", "orion_morphology_opening_kernel_size_dpi1"))
    orion_morphology_opening_kernel_size_dpi2.set(config.getint("orion", "orion_morphology_opening_kernel_size_dpi2"))
    orion_min_contour_area_dpi1.set(config.getint("orion", "orion_min_contour_area_dpi1"))
    orion_min_contour_area_dpi2.set(config.getint("orion", "orion_min_contour_area_dpi2"))
    orion_max_contour_area_dpi1.set(config.getint("orion", "orion_max_contour_area_dpi1"))
    orion_max_contour_area_dpi2.set(config.getint("orion", "orion_max_contour_area_dpi2"))
    orionmax_hole_radius_dpi1.set(config.getint("orion", "orionmax_hole_radius_dpi1"))
    orionmax_hole_radius_dpi2.set(config.getint("orion", "orionmax_hole_radius_dpi2"))
    use_bubbles_var.set(config.getboolean("orion", "name_from_bubbles"))

    # Continue setting variables for the NRA A-17
    nra_kernal_size.set(config.getint("nra", "nra_kernal_size"))
    nra_param1.set(config.getfloat("nra", "nra_param1"))
    nra_param2.set(config.getint("nra", "nra_param2"))
    nra_min_radius.set(config.getint("nra", "nra_min_radius"))
    nra_thresh_min.set(config.getint("nra", "nra_thresh_min"))
    nra_thresh_max.set(config.getint("nra", "nra_thresh_max"))
    nra_morphology_opening_kernel_size.set(config.getint("nra", "nra_morphology_opening_kernel_size"))
    nra_min_contour_area.set(config.getint("nra", "nra_min_contour_area"))
    nra_max_contour_area.set(config.getint("nra", "nra_max_contour_area"))
    nramax_hole_radius.set(config.getint("nra", "nramax_hole_radius"))

# Save settings to config file
def create_default_config(file):
    # Create a config parser
    config = ConfigParser()

    config.read(file) # Read the given config file

    config.add_section('settings') # Add the settings section to the config file

    # Add the settings to the config file
    config.set('settings', 'dpi', str(dpi_var.get()))
    config.set('settings', 'dark_mode', str(dark_mode_var.get()))
    config.set('settings', 'show_output_when_finished', str(show_output_when_finished_var.get()))
    config.set('settings', 'individual_output_type', str(individual_output_type_var.get()))
    config.set('settings', 'use_file_info', str(use_file_info_var.get()))

    # Add the orion section to the config file
    config.add_section('orion')
    # Settings for the orion targets
    config.set('orion', 'orion_kernel_size_dpi1', str(orion_kernel_size_dpi1.get()))
    config.set('orion', 'orion_kernel_size_dpi2', str(orion_kernel_size_dpi2.get()))
    config.set('orion', 'orion_param1_dpi1', str(orion_param1_dpi1.get()))
    config.set('orion', 'orion_param2_dpi1', str(orion_param2_dpi1.get()))
    config.set('orion', 'orion_min_radius_dpi1', str(orion_min_radius_dpi1.get()))
    config.set('orion', 'orion_param1_dpi2', str(orion_param1_dpi2.get()))
    config.set('orion', 'orion_param2_dpi2', str(orion_param2_dpi2.get()))
    config.set('orion', 'orion_min_radius_dpi2', str(orion_min_radius_dpi2.get()))
    config.set('orion', 'orion_thresh_min', str(orion_thresh_min.get()))
    config.set('orion', 'orion_thresh_max', str(orion_thresh_max.get()))
    config.set('orion', 'orion_morphology_opening_kernel_size_dpi1', str(orion_morphology_opening_kernel_size_dpi1.get()))
    config.set('orion', 'orion_morphology_opening_kernel_size_dpi2', str(orion_morphology_opening_kernel_size_dpi2.get()))
    config.set('orion', 'orion_min_contour_area_dpi1', str(orion_min_contour_area_dpi1.get()))
    config.set('orion', 'orion_min_contour_area_dpi2', str(orion_min_contour_area_dpi2.get()))
    config.set('orion', 'orion_max_contour_area_dpi1', str(orion_max_contour_area_dpi1.get()))
    config.set('orion', 'orion_max_contour_area_dpi2', str(orion_max_contour_area_dpi2.get()))
    config.set('orion', 'orionmax_hole_radius_dpi1', str(orionmax_hole_radius_dpi1.get()))
    config.set('orion', 'orionmax_hole_radius_dpi2', str(orionmax_hole_radius_dpi2.get()))
    config.set('orion', 'name_from_bubbles', str(use_bubbles_var.get()))

    # Add the NRA A-17 section to the config file
    config.add_section('nra')
    # Settings for the NRA A-17 targets
    config.set('nra', 'nra_kernal_size', str(nra_kernal_size.get()))
    config.set('nra', 'nra_param1', str(nra_param1.get()))
    config.set('nra', 'nra_param2', str(nra_param2.get()))
    config.set('nra', 'nra_min_radius', str(nra_min_radius.get()))
    config.set('nra', 'nra_thresh_min', str(nra_thresh_min.get()))
    config.set('nra', 'nra_thresh_max', str(nra_thresh_max.get()))
    config.set('nra', 'nra_morphology_opening_kernel_size', str(nra_morphology_opening_kernel_size.get()))
    config.set('nra', 'nra_min_contour_area', str(nra_min_contour_area.get()))
    config.set('nra', 'nra_max_contour_area', str(nra_max_contour_area.get()))
    config.set('nra', 'nramax_hole_radius', str(nramax_hole_radius.get()))

    # Write the changes to the config file
    with open(file, 'w') as f:
        config.write(f)

# Updates config.ini file with current settings
def update_config():
    config = ConfigParser() # Create a config parser

    config.read('config.ini') # Read the config file

    # Update the settings in the config file
    config.set('settings', 'dpi', str(dpi_var.get()))
    config.set('settings', 'dark_mode', str(dark_mode_var.get()))
    config.set('settings', 'show_output_when_finished', str(show_output_when_finished_var.get()))
    config.set('settings', 'individual_output_type', str(individual_output_type_var.get()))
    config.set('settings', 'use_file_info', str(use_file_info_var.get()))
    # Continue updating the settings for the Orion section
    config.set('orion', 'orion_kernel_size_dpi1', str(orion_kernel_size_dpi1.get()))
    config.set('orion', 'orion_kernel_size_dpi2', str(orion_kernel_size_dpi2.get()))
    config.set('orion', 'orion_param1_dpi1', str(orion_param1_dpi1.get()))
    config.set('orion', 'orion_param2_dpi1', str(orion_param2_dpi1.get()))
    config.set('orion', 'orion_min_radius_dpi1', str(orion_min_radius_dpi1.get()))
    config.set('orion', 'orion_param1_dpi2', str(orion_param1_dpi2.get()))
    config.set('orion', 'orion_param2_dpi2', str(orion_param2_dpi2.get()))
    config.set('orion', 'orion_min_radius_dpi2', str(orion_min_radius_dpi2.get()))
    config.set('orion', 'orion_thresh_min', str(orion_thresh_min.get()))
    config.set('orion', 'orion_thresh_max', str(orion_thresh_max.get()))
    config.set('orion', 'orion_morphology_opening_kernel_size_dpi1', str(orion_morphology_opening_kernel_size_dpi1.get()))
    config.set('orion', 'orion_morphology_opening_kernel_size_dpi2', str(orion_morphology_opening_kernel_size_dpi2.get()))
    config.set('orion', 'orion_min_contour_area_dpi1', str(orion_min_contour_area_dpi1.get()))
    config.set('orion', 'orion_min_contour_area_dpi2', str(orion_min_contour_area_dpi2.get()))
    config.set('orion', 'orion_max_contour_area_dpi1', str(orion_max_contour_area_dpi1.get()))
    config.set('orion', 'orion_max_contour_area_dpi2', str(orion_max_contour_area_dpi2.get()))
    config.set('orion', 'orionmax_hole_radius_dpi1', str(orionmax_hole_radius_dpi1.get()))
    config.set('orion', 'orionmax_hole_radius_dpi2', str(orionmax_hole_radius_dpi2.get()))
    config.set('orion', 'name_from_bubbles', str(use_bubbles_var.get()))
    # Continue updating the settings for the NRA A-17 section
    config.set('nra', 'nra_kernal_size', str(nra_kernal_size.get()))
    config.set('nra', 'nra_param1', str(nra_param1.get()))
    config.set('nra', 'nra_param2', str(nra_param2.get()))
    config.set('nra', 'nra_min_radius', str(nra_min_radius.get()))
    config.set('nra', 'nra_thresh_min', str(nra_thresh_min.get()))
    config.set('nra', 'nra_thresh_max', str(nra_thresh_max.get()))
    config.set('nra', 'nra_morphology_opening_kernel_size', str(nra_morphology_opening_kernel_size.get()))
    config.set('nra', 'nra_min_contour_area', str(nra_min_contour_area.get()))
    config.set('nra', 'nra_max_contour_area', str(nra_max_contour_area.get()))
    config.set('nra', 'nramax_hole_radius', str(nramax_hole_radius.get()))

    # Write the changes to the config file
    with open('config.ini', 'w') as f:
        config.write(f)

# -------------------------- Analyze image functions ------------------------- #

# Analyze an outdoor bull (CURRENTLY DISABLED) (ALSO NOT DOCUMENTED)
def analyze_outdoor_image(image):
    # Basic implementation of the distance formula
    def compute_distance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA A-23 target in inches
    outer = 5.89
    six = 4.89/outer
    seven = 3.89/outer
    eight = 2.89/outer
    nine = 1.89/outer
    ten = 0.89/outer
    x_ring = 0.39/outer

    spindle_radius = 0.11 # These are still in mm oof
    outer_spindle_radius = 0.177 # I might need to fix this
    #endregion

    dropped_points = 0
    x_count = 0

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
            pixel_outer = r

            # Perform a calculation to determine if the system detected the wrong ring, and if so, correct the error
            height, width, channels = img.shape
            # These need to be recalculated for the outdoor targets
            # if r/width < 0.4 and r/width > 0.35:
            #     pixel_outer = outer/37.670 * r
            
            # if r/width < 0.35:
            #     pixel_outer = outer/29.210 * r

            pixel_six = pixel_outer*six
            pixel_seven = pixel_outer*seven
            pixel_eight = pixel_outer*eight
            pixel_nine = pixel_outer*nine
            pixel_ten = pixel_outer*ten
            pixel_x = pixel_outer*x_ring

            spindle_radius = spindle_radius*(pixel_outer/outer)
            #print(spindle_radius)
            outer_spindle_radius = outer_spindle_radius*(pixel_outer/outer)

            cv2.circle(output, (a, b), int(pixel_outer), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_six), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_seven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_eight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_nine), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_ten), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_x), (0, 255, 0), 2)

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
        #print(area)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000
        if area<200 and area>50:
            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (hole_x,hole_y),hole_radius = cv2.minEnclosingCircle(contour)
            hole_center = (int(hole_x),int(hole_y))
            hole_radius = int(hole_radius)
            #print("hole_radius: " + str(hole_radius))
            if hole_radius < 40:
                #cv2.circle(output,hole_center,hole_radius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, hole_center, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,hole_center,int(spindle_radius),(0,255,255),2)
                #cv2.circle(output,hole_center,int(outer_spindle_radius),(0,255,255),2)

                distance = compute_distance(hole_x, hole_y, a, b)

                # Currently only scores target to a 4
                if distance-spindle_radius < pixel_x:
                    print("X")
                    cv2.putText(output, "X", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    x_count += 1

                if distance+spindle_radius < pixel_ten and distance-spindle_radius > pixel_x:
                    print("0")
                    cv2.putText(output, "0", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                if distance-spindle_radius > pixel_ten and distance+spindle_radius < pixel_nine:
                    print("1")
                    cv2.putText(output, "1", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 1

                if distance-spindle_radius > pixel_nine and distance+spindle_radius < pixel_eight:
                    print("2")
                    cv2.putText(output, "2", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 2

                if distance-spindle_radius > pixel_eight and distance+spindle_radius < pixel_seven:
                    print("3")
                    cv2.putText(output, "3", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 3

                if distance-spindle_radius > pixel_seven and distance+spindle_radius < pixel_six:
                    print("4")
                    cv2.putText(output, "4", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 4

                hole_ratio_x = (hole_x-a) / pixel_outer
                hole_ratio_y = (hole_y-a) / pixel_outer

                global csv_name

                with open(csv_name, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
    cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output)

# Derived from improved.py
def analyze_image(image):
    # Basic implementation of the distance formula
    def compute_distance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA A-17 target in millimeters
    outer = 46.150
    five = 37.670/outer
    six = 29.210/outer
    seven = 20.750/outer
    eight = 12.270/outer
    nine = 3.810/outer

    spindle_radius = 2.83
    outer_spindle_radius = 4.5
    #endregion

    # Hold local dropped points and x count variables
    dropped_points = 0
    x_count = 0

    img = cv2.imread(image) # Read in the image for OpenCV
    output = img.copy() # Create a copy of the image to draw on

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur using 3 * 3 kernel
    gray_blurred = cv2.blur(gray, (nra_kernal_size.get(), nra_kernal_size.get()))
    #cv2.imshow("gray_blurred", gray_blurred)

    #threshold_image=cv2.inRange(gray_blurred, 100, 255)
    #cv2.imshow("threshold_image", threshold_image)
    
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, nra_param1.get(), nra_param2.get(), minRadius = nra_min_radius.get())
    
    # Draw circles that are detected
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

            pixel_outer = r

            # Perform a calculation to determine if the system detected the wrong ring, and if so, correct the error
            height, width, channels = img.shape
            if r/width < 0.4 and r/width > 0.35:
                pixel_outer = outer/37.670 * r
            
            if r/width < 0.35:
                pixel_outer = outer/29.210 * r

            pixel_five = pixel_outer*five
            pixel_six = pixel_outer*six
            pixel_seven = pixel_outer*seven
            pixel_eight = pixel_outer*eight
            pixel_nine = pixel_outer*nine

            spindle_radius = spindle_radius*(pixel_outer/outer)
            outer_spindle_radius = outer_spindle_radius*(pixel_outer/outer)

            cv2.circle(output, (a, b), int(pixel_outer), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_five), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_six), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_seven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_eight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_nine), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    # Make the image binary using a threshold
    img_thresholded = cv2.inRange(img, (nra_thresh_min.get(), nra_thresh_min.get(), nra_thresh_min.get()), (nra_thresh_max.get(), nra_thresh_max.get(), nra_thresh_max.get()))
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    kernel = np.ones((nra_morphology_opening_kernel_size.get(),nra_morphology_opening_kernel_size.get()),np.uint8)
    opening = cv2.morphologyEx(img_thresholded, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening',opening)

    # Find contours based on the denoised image
    contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # Get the area of the contours
        area = cv2.contourArea(contour)
        #print(area)
        # Check if area is between max and min values for a bullet hole. Area is usually about 1000
        if area<nra_max_contour_area.get() and area>nra_min_contour_area.get():

            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (hole_x,hole_y),hole_radius = cv2.minEnclosingCircle(contour)
            hole_center = (int(hole_x),int(hole_y))
            hole_radius = int(hole_radius)
            #print(hole_radius)
            if hole_radius < nramax_hole_radius.get():
                #cv2.circle(output,hole_center,hole_radius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, hole_center, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,hole_center,int(spindle_radius),(0,255,255),2)
                #cv2.circle(output,hole_center,int(outer_spindle_radius),(0,255,255),2)

                distance = compute_distance(hole_x, hole_y, a, b)

                # Currently only scores target to a 4
                if distance-spindle_radius < pixel_nine:
                    print("X")
                    cv2.putText(output, "X", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    x_count += 1

                if distance+spindle_radius < pixel_eight and distance-spindle_radius > pixel_nine:
                    print("0")
                    cv2.putText(output, "0", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                if distance+spindle_radius > pixel_eight and distance+spindle_radius < pixel_seven:
                    print("1")
                    cv2.putText(output, "1", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 1

                if distance+spindle_radius > pixel_seven and distance+spindle_radius < pixel_six:
                    print("2")
                    cv2.putText(output, "2", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 2

                if distance+spindle_radius > pixel_six and distance+spindle_radius < pixel_five:
                    print("3")
                    cv2.putText(output, "3", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 3

                if distance+spindle_radius > pixel_five and distance+spindle_radius < pixel_outer:
                    print("4")
                    cv2.putText(output, "4", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 4

                hole_ratio_x = (hole_x-a) / pixel_outer
                hole_ratio_y = (hole_y-a) / pixel_outer

                global csv_name

                with open(csv_name, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Derived from analyze_image
def analyze_orion_image(image):
    # Basic implementation of the distance formula
    def compute_distance(x1, y1, x2, y2):
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

    inner_spindle_radius = 2.83
    outer_spindle_radius = 4.49
    #endregion

    # Hold local dropped points and x count variables
    dropped_points = 0
    x_count = 0

    img = cv2.imread(image) # Read in the image for OpenCV
    output = img.copy() # Create a copy of the image to draw on

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if dpi_var.get() == 1:
        # Blur using specified kernel
        gray_blurred = cv2.blur(gray, (orion_kernel_size_dpi1.get(), orion_kernel_size_dpi1.get()))
        

    if dpi_var.get() == 2:
        # Blur using specified kernel
        gray_blurred = cv2.blur(gray, (orion_kernel_size_dpi2.get(), orion_kernel_size_dpi2.get()))

    #cv2.imshow("gray_blurred", gray_blurred)

    # Currently not performing any threshold operation
    #threshold_image=cv2.inRange(gray_blurred, 100, 255)
    #cv2.imshow("threshold_image", threshold_image)
    
    # Apply Hough transform on the blurred image.
    if dpi_var.get() == 1:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orion_param1_dpi1.get(), orion_param2_dpi1.get(), minRadius = orion_min_radius_dpi1.get())

    if dpi_var.get() == 2:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orion_param1_dpi2.get(), orion_param2_dpi2.get(), minRadius = orion_min_radius_dpi2.get())
    
    # Draw circles that are detected
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

            pixel_outer = r

            # Perform a calculation to determine if the system detected the wrong ring, and if so, correct the error
            height, width, channels = img.shape

            #print(str(r/width))
            if r/width < 0.37 and r/width > 0.32:
                pixel_outer = outer/23.63 * r
                #print("Fixing radius proportions")
            if r/width < 0.43 and r/width > 0.39:
                pixel_outer = outer/28.75 * r

            pixel_four = pixel_outer*four
            pixel_five = pixel_outer*five
            pixel_six = pixel_outer*six
            pixel_seven = pixel_outer*seven
            pixel_eight = pixel_outer*eight
            pixel_nine = pixel_outer*nine
            pixel_ten = pixel_outer*ten

            outer_spindle_radius = outer_spindle_radius*(pixel_outer/outer)
            inner_spindle_radius = inner_spindle_radius*(pixel_outer/outer)

            cv2.circle(output, (a, b), int(pixel_outer), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_four), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_five), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_six), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_seven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_eight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_nine), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_ten), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    
    img_thresholded = cv2.inRange(img, (orion_thresh_min.get(), orion_thresh_min.get(), orion_thresh_min.get()), (orion_thresh_max.get(), orion_thresh_max.get(), orion_thresh_max.get())) # Make the image binary using a threshold
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    if dpi_var.get() == 1:
        kernel = np.ones((orion_morphology_opening_kernel_size_dpi1.get(),orion_morphology_opening_kernel_size_dpi1.get()),np.uint8)
    
    if dpi_var.get() == 2:
        kernel = np.ones((orion_morphology_opening_kernel_size_dpi2.get(),orion_morphology_opening_kernel_size_dpi2.get()),np.uint8)
    
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

        if dpi_var.get() == 1:
            min_area = orion_min_contour_area_dpi1.get()
            max_area = orion_max_contour_area_dpi1.get()
        if dpi_var.get() == 2:
            min_area = orion_min_contour_area_dpi2.get()
            max_area = orion_max_contour_area_dpi2.get()

        if area<=max_area and area>=min_area:
            # Draw the detected contour for debugging
            #cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole
            (hole_x,hole_y),hole_radius = cv2.minEnclosingCircle(contour)
            hole_center = (int(hole_x),int(hole_y))
            hole_radius = int(hole_radius)
            #print("Hole radius: " + str(hole_radius))
            #cv2.circle(output, hole_center, hole_radius, (255,0,0), 2)
            # compute the center of the contour (different way than enclosing circle) (I don't even understand how it works)
            # M = cv2.moments(contour)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])
            
            # hole_x = cX
            # hole_y = cY

            hole_center = (int(hole_x),int(hole_y))

            if dpi_var.get() == 1:
                max_hole_radius = orionmax_hole_radius_dpi1.get()
            if dpi_var.get() == 2:
                max_hole_radius = orionmax_hole_radius_dpi2.get()
            
            if hole_radius < max_hole_radius:
                #cv2.circle(output,hole_center,hole_radius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, hole_center, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,hole_center,int(outer_spindle_radius),(0,255,255),2)
                #cv2.circle(output,hole_center,int(inner_spindle_radius),(255,255,0),2)

                distance = compute_distance(hole_x, hole_y, a, b)
                #print("Distance: " + str(distance))
                #print("Inner Spindle: " + str(inner_spindle_radius))
                # print("D-O: " + str(distance-outer_spindle_radius))
                # print("D+O: " + str(distance+outer_spindle_radius))
                #print("pixel_ten: " + str(pixel_ten))
                # print("pixel_nine: " + str(pixel_nine))
                # print("pixel_eight: " + str(pixel_eight))
                # print("pixel_seven: " + str(pixel_seven))
                #print("hole_radius: " + str(hole_radius))

                if distance-outer_spindle_radius <= pixel_ten or distance+outer_spindle_radius <= pixel_eight:
                    print("X")
                    cv2.putText(output, "X", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    x_count += 1
                else:
                    if distance+outer_spindle_radius <= pixel_seven:
                        print("0")
                        cv2.putText(output, "0", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    else:
                        if distance+outer_spindle_radius <= pixel_six:
                            print("1")
                            cv2.putText(output, "1", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                            dropped_points += 1
                        else:
                            if distance+outer_spindle_radius <= pixel_five:
                                print("2")
                                cv2.putText(output, "2", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                                dropped_points += 2
                            else:
                                if distance+outer_spindle_radius <= pixel_four:
                                    print("3")
                                    cv2.putText(output, "3", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                                    dropped_points += 3
                                else:
                                    print("Score more than 4 or low confidence: CHECK MANUALLY")
                                    main_label.config(text="Bull " + str(image) + " low confidence")
                                    

                hole_ratio_x = (hole_x-a) / pixel_outer
                hole_ratio_y = (hole_y-a) / pixel_outer

                global csv_name

                with open(csv_name, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Derived from analyze_orion_image and analyze_image
def analyze_orion_image_nra_scoring(image):
    # Basic implementation of the distance formula
    def compute_distance(x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2)+((y2 - y1) ** 2))

    #region multipliers are from NRA A-17 target in millimeters
    # because scoring is performed according to the NRA A-17 target
    outer = 46.150
    five = 37.670/outer
    six = 29.210/outer
    seven = 20.750/outer
    eight = 12.270/outer
    nine = 3.810/outer

    spindle_radius = 2.83
    outer_spindle_radius = 4.5
    #endregion

    # Hold local dropped points and x count variables
    dropped_points = 0
    x_count = 0

    img = cv2.imread(image) # Read in the image for OpenCV
    output = img.copy() # Create a copy of the image to draw on

    #region Identify the target's outer ring
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if dpi_var.get() == 1:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orion_kernel_size_dpi1.get(), orion_kernel_size_dpi1.get()))
        

    if dpi_var.get() == 2:
        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (orion_kernel_size_dpi2.get(), orion_kernel_size_dpi2.get()))

    #cv2.imshow("gray_blurred", gray_blurred)

    # Currently not performing any threshold operation
    #threshold_image=cv2.inRange(gray_blurred, 100, 255)
    #cv2.imshow("threshold_image", threshold_image)
    
    # Apply Hough transform on the blurred image.
    if dpi_var.get() == 1:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orion_param1_dpi1.get(), orion_param2_dpi1.get(), minRadius = orion_min_radius_dpi1.get())

    if dpi_var.get() == 2:
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, orion_param1_dpi2.get(), orion_param2_dpi2.get(), minRadius = orion_min_radius_dpi2.get())
    
    # Draw circles that are detected
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

            pixel_outer = r * 1.382564409826243

            # Perform a calculation to determine if the system detected the wrong ring, and if so, correct the error
            height, width, channels = img.shape

            #print(str(r/width))
            if r/width < 0.37 and r/width > 0.32:
                pixel_outer = outer/23.63 * r
                #print("Fixing radius proportions")
            if r/width < 0.43 and r/width > 0.39:
                pixel_outer = outer/28.75 * r

            pixel_five = pixel_outer*five
            pixel_six = pixel_outer*six
            pixel_seven = pixel_outer*seven
            pixel_eight = pixel_outer*eight
            pixel_nine = pixel_outer*nine

            spindle_radius = spindle_radius*(pixel_outer/outer)
            outer_spindle_radius = outer_spindle_radius*(pixel_outer/outer)

            cv2.circle(output, (a, b), int(pixel_outer), (0, 255, 0), 2)
            #cv2.circle(output, (a, b), int(pixel_four), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_five), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_six), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_seven), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_eight), (0, 255, 0), 2)
            cv2.circle(output, (a, b), int(pixel_nine), (0, 255, 0), 2)
            #cv2.circle(output, (a, b), int(pixel_ten), (0, 255, 0), 2)

            # Draw a small circle to show the center.
            cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
    #endregion

    #region Identify the hole in the target
    
    img_thresholded = cv2.inRange(img, (orion_thresh_min.get(), orion_thresh_min.get(), orion_thresh_min.get()), (orion_thresh_max.get(), orion_thresh_max.get(), orion_thresh_max.get())) # Make the image binary using a threshold
    #cv2.imshow('Image Thresholded', img_thresholded)

    # Remove noise from the binary image using the opening operation
    if dpi_var.get() == 1:
        kernel = np.ones((orion_morphology_opening_kernel_size_dpi1.get(),orion_morphology_opening_kernel_size_dpi1.get()),np.uint8)
    
    if dpi_var.get() == 2:
        kernel = np.ones((orion_morphology_opening_kernel_size_dpi2.get(),orion_morphology_opening_kernel_size_dpi2.get()),np.uint8)
    
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

        if dpi_var.get() == 1:
            min_area = orion_min_contour_area_dpi1.get()
            max_area = orion_max_contour_area_dpi1.get()
        if dpi_var.get() == 2:
            min_area = orion_min_contour_area_dpi2.get()
            max_area = orion_max_contour_area_dpi2.get()

        if area<=max_area and area>=min_area:
            # Draw the detected contour for debugging
            #cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole
            (hole_x,hole_y),hole_radius = cv2.minEnclosingCircle(contour)
            hole_center = (int(hole_x),int(hole_y))
            hole_radius = int(hole_radius)
            #print("Hole radius: " + str(hole_radius))
            #cv2.circle(output, hole_center, hole_radius, (255,0,0), 2)
            # compute the center of the contour (different way than enclosing circle) (I don't even understand how it works)
            # M = cv2.moments(contour)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])
            
            # hole_x = cX
            # hole_y = cY

            hole_center = (int(hole_x),int(hole_y))

            if dpi_var.get() == 1:
                max_hole_radius = orionmax_hole_radius_dpi1.get()
            if dpi_var.get() == 2:
                max_hole_radius = orionmax_hole_radius_dpi2.get()
            
            if hole_radius < max_hole_radius:
                #cv2.circle(output,hole_center,hole_radius,(0,255,0),2) # Enclosing circle
                cv2.circle(output, hole_center, 1, (0, 0, 255), 3) # Dot at the center

                # Draw the spindle
                cv2.circle(output,hole_center,int(outer_spindle_radius),(0,255,255),2)
                #cv2.circle(output,hole_center,int(inner_spindle_radius),(255,255,0),2)

                distance = compute_distance(hole_x, hole_y, a, b)

                if distance-spindle_radius < pixel_nine:
                    print("X")
                    cv2.putText(output, "X", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    x_count += 1

                if distance+spindle_radius < pixel_eight and distance-spindle_radius > pixel_nine:
                    print("0")
                    cv2.putText(output, "0", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                if distance+spindle_radius > pixel_eight and distance+spindle_radius < pixel_seven:
                    print("1")
                    cv2.putText(output, "1", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 1

                if distance+spindle_radius > pixel_seven and distance+spindle_radius < pixel_six:
                    print("2")
                    cv2.putText(output, "2", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 2

                if distance+spindle_radius > pixel_six and distance+spindle_radius < pixel_five:
                    print("3")
                    cv2.putText(output, "3", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 3

                if distance+spindle_radius > pixel_five and distance+spindle_radius < pixel_outer:
                    print("4")
                    cv2.putText(output, "4", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    dropped_points += 4
                                    

                hole_ratio_x = (hole_x-a) / pixel_outer
                hole_ratio_y = (hole_y-a) / pixel_outer

                global csv_name

                with open(csv_name, 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# ------------------------------ Driver program ------------------------------ #

#region Initialize tkinter window
root = tk.Tk()
# Set the initial theme
root.tk.call("source", "assets/sun-valley/sun-valley.tcl")
root.tk.call("set_theme", "light")
# Set up the window geometry
root.minsize(600,400)
root.geometry("600x400")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='assets/icon.png'))
root.title("Target Analysis")
#endregion

#region Global variables
# DPI is consistent across all targets that would be scanned. Therefore, it only needs to be set once for all of them.
dpi_var = tk.IntVar(root, 1)
dark_mode_var = tk.BooleanVar(root, False)
show_output_when_finished_var = tk.BooleanVar(root, True)
individual_output_type_var = tk.StringVar(root, "tkinter")
use_file_info_var = tk.BooleanVar(root, True)
use_bubbles_var = tk.BooleanVar(root, False)
is_opening_folder = False

#region While many similar parameters exist for non-Orion targets, each has been tuned for its use case and therefore are unique to Orion scanning.
orion_kernel_size_dpi1 = tk.IntVar(root, 2)
orion_kernel_size_dpi2 = tk.IntVar(root, 5)
orion_param1_dpi1 = tk.DoubleVar(root, 1.4)
orion_param2_dpi1 = tk.IntVar(root, 200)
orion_min_radius_dpi1 = tk.IntVar(root, 130)
orion_param1_dpi2 = tk.IntVar(root, 2)
orion_param2_dpi2 = tk.IntVar(root, 600)
orion_min_radius_dpi2 = tk.IntVar(root, 260)
orion_thresh_min = tk.IntVar(root, 100)
orion_thresh_max = tk.IntVar(root, 255)
orion_morphology_opening_kernel_size_dpi1 = tk.IntVar(root, 2)
orion_morphology_opening_kernel_size_dpi2 = tk.IntVar(root, 2)
orion_min_contour_area_dpi1 = tk.IntVar(root, 200)
orion_max_contour_area_dpi1 = tk.IntVar(root, 5000)
orion_min_contour_area_dpi2 = tk.IntVar(root, 5000)
orion_max_contour_area_dpi2 = tk.IntVar(root, 12000)
orionmax_hole_radius_dpi1 = tk.IntVar(root, 40)
orionmax_hole_radius_dpi2 = tk.IntVar(root, 90)
#endregion

#region Fine tuning settings for non-Orion targets
nra_kernal_size = tk.IntVar(root, 3)
nra_param1 = tk.DoubleVar(root, 1.4)
nra_param2 = tk.IntVar(root, 200)
nra_min_radius = tk.IntVar(root, 130)
nra_thresh_min = tk.IntVar(root, 100)
nra_thresh_max = tk.IntVar(root, 255)
nra_morphology_opening_kernel_size = tk.IntVar(root, 10)
nra_min_contour_area = tk.IntVar(root, 200)
nra_max_contour_area = tk.IntVar(root, 1500)
nramax_hole_radius = tk.IntVar(root, 40)
#endregion

# Check for a config file. If it exists, load the values from it. Otherwise, create a config file frome the defaults.
if os.path.isfile("config.ini"):
    # If the file exists, update settings to match the config file
    update_settings_from_config("config.ini")
else:
    # If the file does not exist, create it and set the default values
    create_default_config("config.ini")

# If there is not config backup, create one now
if not os.path.isfile("config-backup.ini"):
    # If the file does not exist, create it and set the default values
    create_default_config("config-backup.ini")

#region If there is not a names config, create one now
if not os.path.isfile("names.ini"):
    # If the file does not exist, create it and set the default values
    create_names_config()
#endregion
#endregion

#region menubar with File and Help menus
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="Load left image", command=load_image_left)
#filemenu.add_command(label="Load right image", command=load_image_right)
#filemenu.add_command(label="Load single image", command=load_image_single)
#filemenu.add_command(label="Analyze target", command=analyze_target)
#filemenu.add_command(label="Open Folder", command=open_folder)
filemenu.add_command(label="Show in Explorer", command=lambda: show_folder(os.getcwd()))
filemenu.add_command(label="Show Output", command=show_output, state=DISABLED)
filemenu.add_command(label="Show Trends", command=show_trends)
#filemenu.add_command(label="(Experimental) Load Outdoor", command=load_image_outdoor)
filemenu.add_separator()
filemenu.add_command(label="Settings", command=open_settings)
filemenu.add_separator()
filemenu.add_command(label="Clear data", command=clear_data)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
#filemenu.add_command(label="Analysis Window", command=open_analysis_window)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="README", command=lambda: open_file('"' + os.getcwd() + "/README.md" + '"'))
helpmenu.add_command(label="Scanning diagram", command=lambda: open_file('"' + os.getcwd() + "/help/" + "scanner-digital.png" + '"'))
helpmenu.add_command(label="Accuracy screenshot", command=lambda: open_file('"' + os.getcwd() + "/help/" + "accuracy-vs-hand-scored.png" + '"'))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
#endregion

#region Set up frames
# top_frame holds the main label
top_frame = ttk.Frame(root)
top_frame.pack(fill=X)

# Options frame has the settings for name, date, etc
options_frame = ttk.Frame(root)
options_frame.pack(side=tk.TOP, padx=7.5, pady=7.5)

# Notebook allows for a tabbed view of the different target types
tab_control = ttk.Notebook(root)

tab0_indoor = ttk.Frame(tab_control)
tab1_orion = ttk.Frame(tab_control)
tab3_orionnra = ttk.Frame(tab_control)

tab_control.add(tab0_indoor, text ='NRA A-17')
tab_control.add(tab1_orion, text ='NRA/USAS-50')
tab_control.add(tab3_orionnra, text ='NRA/USAS-50 as NRA A-17')

tab_control.pack(side=tk.TOP, fill=BOTH, padx=10, pady=10)

# Buttons frames are a child of the tabs
buttons_frame = ttk.Frame(tab0_indoor)
buttons_frame.pack(side=tk.TOP)

bottom_frame = ttk.Frame(tab0_indoor)
bottom_frame.pack(side=tk.TOP)

orion_buttons_frame = ttk.Frame(tab1_orion)
orion_buttons_frame.pack(side=tk.TOP)

orion_bottom_frame = ttk.Frame(tab1_orion)
orion_bottom_frame.pack(side=tk.TOP)

orion_as_nra_frame = ttk.Frame(tab3_orionnra)
orion_as_nra_frame.pack(side=tk.TOP)

orion_as_nra_bottom_frame = ttk.Frame(tab3_orionnra)
orion_as_nra_bottom_frame.pack(side=tk.TOP)
#endregion

#region Label at top of the frame alerts the user to the program's actions uses top_frame
main_label = ttk.Label(top_frame, text="Load an image to get started")
main_label.pack(side=tk.TOP, padx=10, pady=5)

# Add a separator line
label_separator = ttk.Separator(top_frame, orient=HORIZONTAL)
label_separator.pack(side=TOP, fill=X)
#endregion

#region Options area uses options_frame
# Month entry
month_var = tk.StringVar()
month_var.set("Month")
month_entry = ttk.Entry(options_frame, textvariable=month_var, width=10)
month_entry.grid(column = 0, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Day entry
day_var = tk.StringVar()
day_var.set("Day")
date_entry = ttk.Entry(options_frame, textvariable=day_var, width=5)
date_entry.grid(column = 1, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Year entry
year_var = tk.StringVar()
year_var.set("Year")
year_entry = ttk.Entry(options_frame, textvariable=year_var, width=5)
year_entry.grid(column = 2, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Target number entry
target_num_var = tk.StringVar()
target_num_var.set("Num")
target_num_entry = ttk.Entry(options_frame, textvariable=target_num_var, width=5)
target_num_entry.grid(column = 3, row = 0, sticky=NSEW, padx=2.5, pady=5)

# Name entry
name_var = tk.StringVar()
name_var.set("Name")
name_entry = ttk.Entry(options_frame, textvariable=name_var, width=30)
name_entry.grid(column = 0, row = 1, columnspan = 4, sticky=NSEW, padx=2.5)

# Today button and use file info switch are placed to the right of the name and date
# Use today's date button
today_button = ttk.Button(options_frame, text="Use Today", command=set_info_from_today)
today_button.grid(column=4, row=0, rowspan=2, padx=2.5)

# Use info from file switch
use_file_info_checkbutton = ttk.Checkbutton(options_frame, text='Use info from file', style='Switch.TCheckbutton', variable=use_file_info_var, onvalue=True, offvalue=False, command=update_config)
use_file_info_checkbutton.grid(column=5, row=0, rowspan=2, padx=5)
#endregion

#region Buttons for NRA A-17 target loading and analysis
left_image_button = ttk.Button(buttons_frame, text = "Select left image", command = load_image_left)
left_image_button.grid(row=0, column=0, padx=5, pady=5)

analyze_target_button = ttk.Button(buttons_frame, text = "Analyze target", command = lambda: analyze_target("nra"))
analyze_target_button.grid(row=0, column=1, padx=5, pady=5)

right_image_button = ttk.Button(buttons_frame, text = "Select right image", command = load_image_right)
right_image_button.grid(row=0, column=2, padx=5, pady=5)

open_folder_nra_button = ttk.Button(buttons_frame, text = "Open folder", command = open_folder)
open_folder_nra_button.grid(row=0, column=3, padx=5, pady=5)
#endregion

#region Buttons for Orion NRA/USAS-50 target loading and analysis
load_image_button = ttk.Button(orion_buttons_frame, text = "Select image", command = lambda: load_image_orion("orion"))
load_image_button.grid(row=0, column=0, padx=5, pady=5)

analyze_orion_target_button = ttk.Button(orion_buttons_frame, text = "Analyze target", command = lambda: analyze_target("orion"))
analyze_orion_target_button.grid(row=0, column=1, padx=5, pady=5)

open_folder_orion_target_button = ttk.Button(orion_buttons_frame, text = "Open folder", command = open_folder_orion)
open_folder_orion_target_button.grid(row=0, column=2, padx=5, pady=5)

use_bubbles_checkbutton = ttk.Checkbutton(orion_buttons_frame, text='Name from bubbles', style='Switch.TCheckbutton', variable=use_bubbles_var, onvalue=True, offvalue=False, command=update_config)
use_bubbles_checkbutton.grid(column=3, row=0, padx=5, pady=5)
#endregion

#region Buttons for Orion NRA/USAS-50 scored as NRA A-17 target loading and analysis
load_image_button_orion_nra = ttk.Button(orion_as_nra_frame, text = "Select image", command = lambda: analyze_target("orion-nrascoring"))
load_image_button_orion_nra.grid(row=0, column=0, padx=5, pady=5)

analyze_orion_target_button_nra = ttk.Button(orion_as_nra_frame, text = "Analyze with Orion scoring", command = lambda: analyze_target("orion-nrascoring"))
analyze_orion_target_button_nra.grid(row=0, column=1, padx=5, pady=5)

open_folder_orion_target_button_nra = ttk.Button(orion_as_nra_frame, text = "Open folder", command = open_folder_orion) # works for both orion and orion-nrascoring by checking which tab is active
open_folder_orion_target_button_nra.grid(row=0, column=2, padx=5, pady=5)

use_bubbles_checkbutton_nra = ttk.Checkbutton(orion_as_nra_frame, text='Name from bubbles', style='Switch.TCheckbutton', variable=use_bubbles_var, onvalue=True, offvalue=False, command=update_config)
use_bubbles_checkbutton_nra.grid(column=3, row=0, padx=5, pady=5)
#endregion

#region Add canvases for NRA A-17 target preview
left_canvas = tk.Canvas(bottom_frame, width=230,height=300)
left_canvas.grid(row = 0, column = 0, padx=5, pady=5)

right_canvas = tk.Canvas(bottom_frame, width=230,height=300)
right_canvas.grid(row = 0, column = 1, padx=5, pady=5)
#endregion

#region Add a single canvas for Orion NRA/USAS-50 target preview
orion_single_canvas = tk.Canvas(orion_bottom_frame, width=230,height=300)
orion_single_canvas.grid(row = 0, column = 0)
#endregion

#region Add a single canvas for Orion NRA/USAS-50 scored as NRA A-17 target preview
orion_single_canvas_nra = tk.Canvas(orion_as_nra_bottom_frame, width=230,height=300)
orion_single_canvas_nra.grid(row = 0, column = 0)
#endregion

tk.mainloop()