#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#region Information
############################################################
## Target Analysis                                        ##
############################################################
## Copyright (c) 2022 Sigmond Kukla, All Rights Reserved  ##
############################################################
## Author: Sigmond Kukla                                  ##
## Copyright: Copyright 2022, Sigmond Kukla               ##
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
from enum import Enum
#import traceback # For debugging - Usage: traceback.print_stack()
#endregion

# --------------------------- Load image functions --------------------------- #

# Load an image for any target type
def load_image(target_type, image_selector="ask"):
    """Prompts the user to select an image from their computer, adds it to the preview, and calls the appropriate function to crop the image

    Args:
        target_type (TargetType): The type of target to load the image for
        image_selector (str): The image to load. If "ask" is passed, the user will be prompted to select an image.
    """

    #region Type-specific changes
    if target_type == TargetTypes.NRA_LEFT:
        canvas = left_canvas
    if target_type == TargetTypes.NRA_RIGHT:
        canvas = right_canvas
    if target_type == TargetTypes.ORION_USAS_50 or target_type == TargetTypes.ORION_USAS_50_NRA_SCORING:
        canvas = orion_single_canvas
    if target_type == TargetTypes.ORION_50FT_CONVENTIONAL:
        canvas = orion_50ft_conventional_canvas
    #endregion

    main_label.config(text="Loading image...") # Update the main label

    canvas.delete("all") # Clear the left canvas in case it already has an image

    if image_selector == "ask": image_file = filedialog.askopenfilename() # Open a tkinter file dialog to select an image
    else: image_file = image_selector # Use the image passed in
    image = cv2.imread(image_file) # Load the image for OpenCV image

    # If the user wants to use information from the file name, do so
    if use_file_info_var.get(): set_info_from_file(image_file)

    if (target_type == TargetTypes.NRA_LEFT or
            target_type == TargetTypes.ORION_USAS_50 or
            target_type == TargetTypes.ORION_USAS_50_NRA_SCORING or
            target_type == TargetTypes.ORION_50FT_CONVENTIONAL):
        canvas.grid(row = 0, column = 0) # Refresh the canvas
    
    if target_type == TargetTypes.NRA_RIGHT:
        canvas.grid(row = 0, column = 1) # Refresh the canvas, placing it in the correct column
    
    global target_preview # Images must be stored globally to be show on the canvas
    target_preview = ImageTk.PhotoImage(Image.open(image_file).resize((230, 350), Image.Resampling.LANCZOS)) # Store the image as a tkinter photo image and resize it
    canvas.create_image(0, 0, anchor="nw", image=target_preview) # Place the image on the canvas

    main_label.config(text="Image loaded") # Update the main label

    root.minsize(550,540) # Increase the window size to accomodate the image

    crop_image(image, target_type) # Crop the image to prepare for analysis

# --------------------------- Crop image functions --------------------------- #

# Crop the image based on the given target_type and saves the bulls to images/output
def crop_image(image, target_type):
    """Crops the given image based on the given target_type and saves the bulls to images/output

    Args:
        image (cv2 image): The image to crop
        target_type (TargetTypes): The type of target to crop
    """

    main_label.config(text="Cropping image...") # Update main label
    check_output_dir()

    # Pixel measurements were taken from 300dpi targets, so use the same ratio where necessary
    ratio_height = 3507
    ratio_width = 2550

    # Crop left side of NRA target
    if target_type == TargetTypes.NRA_LEFT:
        # Flip the image vertically and horizontally before cropping
        verticalFlippedImage = cv2.flip(image, -1)
        cv2.imwrite("images/output/vertical-flipped.jpg", verticalFlippedImage)

        # Set the bull size for NRA A-17 targets and calculate the height and width of the cropped images
        bull_size = 580
        h=int((bull_size/ratio_height)*image.shape[0])
        w=int((bull_size/ratio_width)*image.shape[1])

        leftX = 185

        y=int((240/ratio_height)*image.shape[0])
        x=int((leftX/ratio_width)*image.shape[1])
        crop2 = verticalFlippedImage[y:y+h, x:x+w]

        y=int((1040/ratio_height)*image.shape[0])
        x=int((leftX/ratio_width)*image.shape[1])
        crop3 = verticalFlippedImage[y:y+h, x:x+w]

        y=int((1840/ratio_height)*image.shape[0])
        x=int((leftX/ratio_width)*image.shape[1])
        crop4 = verticalFlippedImage[y:y+h, x:x+w]

        y=int((2645/ratio_height)*image.shape[0])
        x=int((leftX/ratio_width)*image.shape[1])
        crop5 = verticalFlippedImage[y:y+h, x:x+w]

        # Save the cropped sections
        cv2.imwrite("images/output/top-left.jpg", crop2)
        cv2.imwrite("images/output/upper-left.jpg", crop3)
        cv2.imwrite("images/output/lower-left.jpg", crop4)
        cv2.imwrite("images/output/bottom-left.jpg", crop5)
    
    # Crop right side of NRA target
    if target_type == TargetTypes.NRA_RIGHT:
        # Set the bull size for NRA A-17 targets and calculate the height and width of the cropped images
        bull_size = 580
        h=int((bull_size/ratio_height)*image.shape[0])
        w=int((bull_size/ratio_width)*image.shape[1])

        midX = 720
        rightX = 1760

        topY = 275
        upperY = 1070
        lowerY = 1880
        bottomY = 2680

        y=int((topY/ratio_height)*image.shape[0])
        x=int((midX/ratio_width)*image.shape[1])
        crop1 = image[y:y+h, x:x+w]

        y=int((topY/ratio_height)*image.shape[0])
        x=int((rightX/ratio_width)*image.shape[1])
        crop2 = image[y:y+h, x:x+w]

        y=int((upperY/ratio_height)*image.shape[0])
        x=int((rightX/ratio_width)*image.shape[1])
        crop3 = image[y:y+h, x:x+w]

        y=int((lowerY/ratio_height)*image.shape[0])
        x=int((rightX/ratio_width)*image.shape[1])
        crop4 = image[y:y+h, x:x+w]

        y=int((bottomY/ratio_height)*image.shape[0])
        x=int((rightX/ratio_width)*image.shape[1])
        crop5 = image[y:y+h, x:x+w]

        y=int((bottomY/ratio_height)*image.shape[0])
        x=int((midX/ratio_width)*image.shape[1])
        crop6 = image[y:y+h, x:x+w]

        # Save the cropped sections
        cv2.imwrite("images/output/top-mid.jpg", crop1)
        cv2.imwrite("images/output/top-right.jpg", crop2)
        cv2.imwrite("images/output/upper-right.jpg", crop3)
        cv2.imwrite("images/output/lower-right.jpg", crop4)
        cv2.imwrite("images/output/bottom-right.jpg", crop5)
        cv2.imwrite("images/output/bottom-mid.jpg", crop6)
    
    # Crop Orion target
    if target_type == TargetTypes.ORION_USAS_50 or target_type == TargetTypes.ORION_USAS_50_NRA_SCORING or target_type == TargetTypes.ORION_50FT_CONVENTIONAL:
        # Pixel measurements were taken from 300dpi targets, so use the same ratio where necessary
        ratio_height = 3299
        ratio_width = 2544

        height_to_width_ratio = ratio_height / ratio_width

        bottom_removed = image[0:int(image.shape[0]*height_to_width_ratio), 0:image.shape[1]] # Remove the bottom of the image, keeping proportional height
        # cv2.imwrite("images/output/bottom-removed.jpg", bottom_removed) # for debugging
        
        # Set positions for Orion NRA/USAS-50 targets
        if target_type == TargetTypes.ORION_USAS_50 or target_type == TargetTypes.ORION_USAS_50_NRA_SCORING:
            bull_size = 400
            
            #    (LeftX, TopY)   (MidX, TopY)  (RightX, TopY)
            #  (LeftX, UpperY)                 (RightX, UpperY)
            #  (LeftX, LowerY)                 (RightX, LowerY)
            # (LeftX, BottomY) (MidX, BottomY) (RightX, BottomY)

            leftX = 225
            midX = 1070
            rightX = 1920

            topY = 425
            upperY = 1175
            lowerY = 1925
            bottomY = 2680

        # Set positions for Orion 50ft conventional targets
        if target_type == TargetTypes.ORION_50FT_CONVENTIONAL:
            bull_size = 600

            # (LeftX, TopY) (MidX, TopY) (RightX, TopY)
            # (LeftX, UpperY) (RightX, UpperY)
            # (LeftX, LowerY) (RightX, LowerY)
            # (LeftX, BottomY) (MidX, BottomY) (RightX, BottomY)

            leftX = 115
            midX = 965
            rightX = 1805

            topY = 355
            upperY = 1090
            lowerY = 1850
            bottomY = 2600
        
        # Set the same height and width for all cropped images
        h=int((bull_size/ratio_height)*bottom_removed.shape[0])
        w=int((bull_size/ratio_width)*bottom_removed.shape[1])

        y=int((topY/ratio_height)*bottom_removed.shape[0])
        x=int((midX/ratio_width)*bottom_removed.shape[1])

        crop1 = bottom_removed[y:y+h, x:x+w]

        y=int((topY/ratio_height)*bottom_removed.shape[0])
        x=int((rightX/ratio_width)*bottom_removed.shape[1])

        crop2 = bottom_removed[y:y+h, x:x+w]

        y=int((upperY/ratio_height)*bottom_removed.shape[0])
        x=int((rightX/ratio_width)*bottom_removed.shape[1])

        crop3 = bottom_removed[y:y+h, x:x+w]

        y=int((lowerY/ratio_height)*bottom_removed.shape[0])
        x=int((rightX/ratio_width)*bottom_removed.shape[1])
        crop4 = bottom_removed[y:y+h, x:x+w]

        y=int((bottomY/ratio_height)*bottom_removed.shape[0])
        x=int((rightX/ratio_width)*bottom_removed.shape[1])

        crop5 = bottom_removed[y:y+h, x:x+w]

        y=int((bottomY/ratio_height)*bottom_removed.shape[0])
        x=int((midX/ratio_width)*bottom_removed.shape[1])

        crop6 = bottom_removed[y:y+h, x:x+w]

        # NOTE: STUFF BELOW IS STRANGE
        # crop7 represents the top-left corner of the bull
        # and the following go DOWN the left side
        # now this is illogical, but apparently I do it
        # throughout the program and is a leftover from
        # the left/right cropping of NRA targets
        # Therefore, I'm just going to leave it as is

        y=int((topY/ratio_height)*bottom_removed.shape[0])
        x=int((leftX/ratio_width)*bottom_removed.shape[1])

        crop7 = bottom_removed[y:y+h, x:x+w]

        y=int((upperY/ratio_height)*bottom_removed.shape[0])
        x=int((leftX/ratio_width)*bottom_removed.shape[1])

        crop8 = bottom_removed[y:y+h, x:x+w]

        y=int((lowerY/ratio_height)*bottom_removed.shape[0])
        x=int((leftX/ratio_width)*bottom_removed.shape[1])

        crop9 = bottom_removed[y:y+h, x:x+w]

        y=int((bottomY/ratio_height)*bottom_removed.shape[0])
        x=int((leftX/ratio_width)*bottom_removed.shape[1])

        crop10 = bottom_removed[y:y+h, x:x+w]

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

    # Get name from bubbles if enabled
    if use_bubbles_var.get() and (tab_control.index("current") == 1 or tab_control.index("current") == 2):
        main_label.config(text="Setting name from bubbles...")
        set_name_from_bubbles(image, target_type)
    
    main_label.config(text="Cropped image") # Update the main label

# --------------------------- Scan image functions --------------------------- #

# Get image from scanner
def scan_image():
    def create_image_name():
        '''Generates a file name compatible with Target Analysis based on the current options'''
        # Create a dictionary to convert the full month name to 3 letters, reverse of the dictionary used in set_info_from_file
        months = {
            'January': 'jan', 
            'February': 'feb',
            'March': 'mar',
            'April': 'apr',
            'May': 'may',
            'June': 'jun',
            'July': 'jul',
            'August': 'aug',
            'September': 'sep',
            'October': 'oct',
            'November': 'nov',
            'December': 'dec',
        }
        # Use a try-except to alert the user if the date is invalid
        try: month = months[month_var.get()] # Get the month as a 3 letter string
        except:
            main_label.config(text="Error: Invalid month entered")
            print("Error: Invalid month entered")
            month = 'err'
        return day_var.get() + month + year_var.get() + name_var.get() + target_num_var.get() + ".jpg" # Create the image name
    
    image_name = create_image_name() # Create the image name

    # Scanning uses WINDOWS ONLY wia-cmd-scanner.exe from https://github.com/nagimov/wia-cmd-scanner
    command = '"' + os.path.abspath('assets\wia-cmd-scanner\wia-cmd-scanner.exe') + '"' + ' /w 0 /h 0 /dpi 300 /color RGB /format JPG /output "' + os.path.abspath(os.path.join('images\\' + image_name) + '"') # Create the command to run the scanner
    os.system('call ' + command) # os.system doesn't work for multiple quoted commands therefore we use call to run the command
    main_label.config(text="Image scanned as " + image_name) # Update the main label
    return image_name # Return the image name to call the load function on it

# Scan and save image, load, crop, and analyze the target
def scan_process(target_type):
    """Scans an image, loads and crops it, and analyzes the target

    Args:
        target_type (TargetTypes): What target type the scanned image is
    """    
    main_label.config(text="Scanning image...") # Update the main label
    image_name = scan_image() # Scan and save an image, getting the image name
    path = os.path.join(os.getcwd(), "images", image_name) # Get the path to the image
    load_image(target_type, path) # Load the image
    # Again, really dumb that I haven't combined the enums yet. So I have to do a hacky thing to convert to the scoring type
    if target_type == TargetTypes.ORION_USAS_50:
        scoring_type = ScoringTypes.ORION_USAS_50
    elif target_type == TargetTypes.ORION_USAS_50_NRA_SCORING:
        scoring_type = ScoringTypes.ORION_USAS_50_NRA_SCORING
    elif target_type == TargetTypes.ORION_50FT_CONVENTIONAL:
        scoring_type = ScoringTypes.ORION_50FT_CONVENTIONAL
    analyze_target(scoring_type) # Analyze the image


# -------------------- Target processing control functions ------------------- #

# Run the analyze_image function for every image that has been cropped out
def analyze_target(target_type): 
    """Runs the appropriate analyze_image function for every image that has been cropped and saved.

    Args:
        target_type (TargetType): The type of target to analyze
    """    
    main_label.config(text="Analyzing target...") # Update main label

    global current_target_type
    current_target_type = target_type # Set the current target type

    # Create and store a name for the target output file
    global csv_name
    csv_name = "data-" + name_var.get() + day_var.get() + month_var.get() + year_var.get() + target_num_var.get() + ".csv"

    # If the CSV file already exists, delete it
    if os.path.exists(os.path.join(os.getcwd(), "data\\", csv_name)):
        print("CSV already exists. Removing old version")
        os.remove(os.path.join(os.getcwd(), "data\\", csv_name))
    
    if target_type == ScoringTypes.ORION_USAS_50:
        # Create the CSV file template
        with open(os.path.join("data\\", csv_name), 'x', newline="") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["Image", "Score", "Decimal", "hole_x", "hole_y", "Distance", "hole_ratio_x", "hole_ratio_y"])
            csvfile.close()
    else:
        # Create the CSV file template
        with open(os.path.join("data\\", csv_name), 'x', newline="") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["Image", "Dropped", "X", "hole_x", "hole_y", "Distance", "hole_ratio_x", "hole_ratio_y"])
            csvfile.close()

    # Analyze each cropped image
    if target_type == ScoringTypes.NRA:
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
    elif target_type == ScoringTypes.ORION_USAS_50:
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
    elif target_type == ScoringTypes.ORION_USAS_50_NRA_SCORING:
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
    elif target_type == ScoringTypes.ORION_50FT_CONVENTIONAL:
        analyze_50ft_conventional("images/output/top-mid.jpg")
        analyze_50ft_conventional("images/output/top-right.jpg")
        analyze_50ft_conventional("images/output/upper-right.jpg")
        analyze_50ft_conventional("images/output/lower-right.jpg")
        analyze_50ft_conventional("images/output/bottom-right.jpg")
        analyze_50ft_conventional("images/output/bottom-mid.jpg")
        analyze_50ft_conventional("images/output/bottom-left.jpg")
        analyze_50ft_conventional("images/output/lower-left.jpg")
        analyze_50ft_conventional("images/output/upper-left.jpg")
        analyze_50ft_conventional("images/output/top-left.jpg")
    
    # Create variables to store the score and x count
    global score, x_count
    score = 100
    x_count = 0

    if target_type == ScoringTypes.ORION_USAS_50: score = 0

    # Update the score and x count from the saved target CSV file
    with open(os.path.join("data\\", csv_name)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if target_type == ScoringTypes.ORION_USAS_50:
                    score += int(row[1])
                    score += int(row[2]) / 10
                else:
                    score -= int(row[1])
                    x_count += int(row[2])
            line_count += 1

    # Round the score to the nearest decimal place to avoid floating point error
    score = round(score, 1)

    # If a global data CSV doesn't exist, create it
    if not os.path.exists(str(os.getcwd()) +"/data/data.csv"):
        create_csv()

    # Save the target's basic info to the global data CSV
    with open("data/data.csv", 'a', newline="") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([name_var.get(), day_var.get() + " " + month_var.get() + " " + year_var.get(), target_num_var.get(), score, x_count])
                csvfile.close()

    if enable_teams_var.get():
        teams_csv_path = os.path.join("data\\", active_team_var.get() + ".csv")
        with open(teams_csv_path, 'a', newline="") as csvfile:
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
            
# Show an overview of the target with the score and x count
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
    open_target_csv_button = ttk.Button(output_top_frame, text="Open target CSV", command=lambda: open_file(os.path.join(os.getcwd(), "data\\" + csv_name)))
    open_target_csv_button.grid(row=0, column=0)
    output_top_frame.grid_columnconfigure(0, weight=1)
    
    # Create a label for the score
    global current_target_type
    if current_target_type == ScoringTypes.ORION_USAS_50: score_label_text = str(score)
    else: score_label_text = str(score) + "-" + str(x_count) + "X"
    score_label = ttk.Label(output_top_frame, text=score_label_text, font='bold')
    score_label.grid(row=0, column=1)
    output_top_frame.grid_columnconfigure(1, weight=1)

    # Create a button to open the global data CSV file
    open_data_csv_button = ttk.Button(output_top_frame, text="Open data CSV", command=lambda: open_file(os.path.join(os.getcwd(), "data\\", "data.csv")))
    open_data_csv_button.grid(row=0, column=2)
    output_top_frame.grid_columnconfigure(2, weight=1)
    #endregion

    #region Create canvases and images for each bull
    top_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    top_left_canvas.grid(row = 0, column = 0)

    global top_left_output
    top_left_output = ImageTk.PhotoImage(Image.open("images/output/top-left.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    top_left_canvas.create_image(0, 0, anchor="nw", image=top_left_output)

    upper_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    upper_left_canvas.grid(row = 1, column = 0)

    global upper_left_output
    upper_left_output = ImageTk.PhotoImage(Image.open("images/output/upper-left.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    upper_left_canvas.create_image(0, 0, anchor="nw", image=upper_left_output)

    lower_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    lower_left_canvas.grid(row = 2, column = 0)

    global lower_left_output
    lower_left_output = ImageTk.PhotoImage(Image.open("images/output/lower-left.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    lower_left_canvas.create_image(0, 0, anchor="nw", image=lower_left_output)

    bottom_left_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    bottom_left_canvas.grid(row = 3, column = 0)

    global bottom_left_output
    bottom_left_output = ImageTk.PhotoImage(Image.open("images/output/bottom-left.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    bottom_left_canvas.create_image(0, 0, anchor="nw", image=bottom_left_output)

    top_mid_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    top_mid_canvas.grid(row = 0, column = 1)

    global top_mid_output
    top_mid_output = ImageTk.PhotoImage(Image.open("images/output/top-mid.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    top_mid_canvas.create_image(0, 0, anchor="nw", image=top_mid_output)

    bottom_mid_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    bottom_mid_canvas.grid(row = 3, column = 1)

    global bottom_mid_output
    bottom_mid_output = ImageTk.PhotoImage(Image.open("images/output/bottom-mid.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    bottom_mid_canvas.create_image(0, 0, anchor="nw", image=bottom_mid_output)

    top_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    top_right_canvas.grid(row = 0, column = 2)

    global top_right_output
    top_right_output = ImageTk.PhotoImage(Image.open("images/output/top-right.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    top_right_canvas.create_image(0, 0, anchor="nw", image=top_right_output)

    upper_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    upper_right_canvas.grid(row = 1, column = 2)

    global upper_right_output
    upper_right_output = ImageTk.PhotoImage(Image.open("images/output/upper-right.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    upper_right_canvas.create_image(0, 0, anchor="nw", image=upper_right_output)

    lower_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    lower_right_canvas.grid(row = 2, column = 2)

    global lower_right_output
    lower_right_output = ImageTk.PhotoImage(Image.open("images/output/lower-right.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    lower_right_canvas.create_image(0, 0, anchor="nw", image=lower_right_output)

    bottom_right_canvas = tk.Canvas(output_bottom_frame, width=170,height=170)
    bottom_right_canvas.grid(row = 3, column = 2)

    global bottom_right_output
    bottom_right_output = ImageTk.PhotoImage(Image.open("images/output/bottom-right.jpg-output.jpg").resize((170, 170), Image.Resampling.LANCZOS))
    bottom_right_canvas.create_image(0, 0, anchor="nw", image=bottom_right_output)
    #endregion

# Open the folder specified in path in windows explorer
def show_folder(path):
    """Runs the explorer to the path given

    Args:
        path (str): where to navigate to in explorer
    """
    print("Opening folder: " + path)
    main_label.config(text="Opening folder... ONLY WORKS ON WINDOWS")
    # TODO: Change to pathlib
    os.system("explorer " + os.path.realpath(path)) # Run a system command to open the folder using Explorer (Windows only)
    main_label.config(text="Working directory opened in Explorer") # Update the main label

# Open file with default viewer
def open_file(file):
    main_label.config(text="Opening file " + str(file)) # Update the main label
    os.system(file) # Run a system command to open the file using the default viewer (should work on any operating system)

# Ensure that an image/output directory is available to save images
def check_output_dir():
    path = os.getcwd() + "/images/output" # Store the path to the output directory
    # If the output directory does not exist, create it
    if os.path.isdir(path) == False:
        os.mkdir(path)
    # Otherwise, nothing needs to be done

# Show tkinter based image viewer for the analysis
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
                output_images.append(ImageTk.PhotoImage(Image.open("images/output/" + file).resize((600, 600), Image.Resampling.LANCZOS))) # Load the image as a tkinter photo image and add it to the list
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

# Create data.csv file
def create_csv():
    # Open the CSV file
    with open('data/data.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) # Create a filewriter
        filewriter.writerow(['Name', 'Date', 'Target Number', 'Score','X']) # Write the header row
        csvfile.close() # Close the file
    main_label.config(text="Created CSV data file") # Update the main label

# --------------------------- Open folder functions -------------------------- #

# Open a folder of images for any scoring type
def open_folder(scoring_type):
    """Loads, crops, and analyzes all files in a user-selected folder

    Args:
        scoring_type (ScoringTypes): The type of target that is in the folder
    
    Special note:
        This function uses ScoringTypes because it automatically distinguishes between left and right NRA targets
    """    
    global is_opening_folder
    is_opening_folder = True # Keep track of whether or not the folder is being opened
    show_output_when_finished_backup = show_output_when_finished_var.get()
    show_output_when_finished_var.set(False)
    main_label.config(text="Opening folder... This could take a while") # Update the main label
    folder = filedialog.askdirectory() # Get the folder to open

    nra_file_num = 0 # Keep track of how many files have been opened

    # os.listdir() returns a list of all files in the folder
    for file in os.listdir(folder):
        # Ignore files that are not images
        if file.endswith(".jpeg") or file.endswith(".jpg"):
            path = folder + "/" + file # Get the path to the file
            set_info_from_file(file) # Set the info from the file (correct naming is important for this operation)
            file_image = cv2.imread(path) # Open the image

            if scoring_type == ScoringTypes.NRA:
                # Check if the image is a left or right image
                if "left" in file:
                    crop_image(file_image, TargetTypes.NRA_LEFT)
                elif "right" in file:
                    crop_image(file_image, TargetTypes.NRA_RIGHT)
                file_num += 1 # Increment the file number
                # For every two files opened, analyze the target
                # Again, it is imperative that the naming convention is correct
                # See the README for more information
                if file_num == 2:
                    analyze_target(ScoringTypes.NRA)
                    file_num = 0 # Reset the file number and continue
            elif scoring_type == ScoringTypes.ORION_USAS_50:
                crop_image(file_image, TargetTypes.ORION_USAS_50)
                analyze_target(ScoringTypes.ORION_USAS_50)
            elif scoring_type == ScoringTypes.ORION_USAS_50_NRA_SCORING:
                crop_image(file_image, TargetTypes.ORION_USAS_50_NRA_SCORING)
                analyze_target(ScoringTypes.ORION_USAS_50_NRA_SCORING)
            elif scoring_type == ScoringTypes.ORION_50FT_CONVENTIONAL:
                crop_image(file_image, TargetTypes.ORION_50FT_CONVENTIONAL)
                analyze_target(ScoringTypes.ORION_50FT_CONVENTIONAL)

    show_output_when_finished_var.set(show_output_when_finished_backup) # Revert the show_output_when_finished_var to its original value
    is_opening_folder = False # Keep track of whether or not the folder is being opened
    show_folder(os.getcwd() + "\data") # Open the data folder in Explorer

# ---------------------------- File info funtions ---------------------------- #

# Set target metadata by parsing the file name
def set_info_from_file(file):
    filename = os.path.basename(file) # Get the filename alone in case it is given a full path
    
    filename_without_extension = os.path.splitext(filename)[0] # get the filename without the extension

    day_var.set(filename_without_extension[0:2]) # Set the day

    year_var.set(filename_without_extension[5:9]) # Set the year

    month = filename_without_extension[2:5] # Get the month

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
        'dec': 'December'
    }
    
    # Replace the 3 letter month with the full name using the dictionary
    for short, full in months.items():
        month = month.replace(short, full)

    month_var.set(month) # Set the month

    target_num_var.set(filename_without_extension[-1]) # Set the target number

    # The final section of the filename can be any length and it is "left" or "right" for NRA A-17 targets
    # However, Orion targets use only one scan so that space can hold the shooter's name
    # This is a kind of hacky way to determine if this is an Orion target
    if tab_control.index("current") == 1 or tab_control.index("current") == 2:
        # 01jan2022sigmond1.jpeg -> sigmond
        name = filename_without_extension[9:-1]
        if capitalize_names_var.get(): name = name.title() # Capitalize the name if the user wants it capitalized
        name_var.set(name)

    # Update the main label
    main_label.config(text="Set date to: " + month_var.get() + " " + day_var.get() + ", " + year_var.get() + " and target number " + target_num_var.get())

# Set target metadata from today's date with target number 1
def set_info_from_today():
    today = datetime.datetime.now() # Get today's date

    month_var.set(today.strftime("%B")) # Set the month from the date
    day_var.set(today.strftime("%d")) # Set the day from the date
    year_var.set(today.strftime("%Y")) # Set the year from the date

    target_num_var.set("1") # Default the target number to 1

    # Update the main label
    main_label.config(text="Set date to: " + month_var.get() + " " + day_var.get() + ", " + year_var.get() + " and target number 1")

# ----------------------------- Bubbles functions ---------------------------- #

# Set shooter name from initials on Orion targets
def set_name_from_bubbles(image, target_type):
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

        # Default positions for Orion USAS-50 targets
        # Positions are represented as such:
        # index: (minPos, maxPos)
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

        # Sligtly different positions for Orion 50ft conventional targets
        if target_type == TargetTypes.ORION_50FT_CONVENTIONAL:
            letter_x_positions = {
            0: (50,90),
            1: (95, 130),
            2: (135, 170),
            3: (180, 215),
            4: (220, 260),
            5: (265, 295),
            6: (300, 340),
            7: (345, 385),
            8: (390, 425),
            9: (430, 465),
            10: (470, 510),
            11: (515, 550),
            12: (555, 590)
            }

            y_positions = {
                0: (125,165),
                1: (175, 210),
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

# Create a default names config file
def create_names_config():
    config = ConfigParser()

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

# Load initials and names from names.ini config file and and puts them into respective lists
def load_names_config():
    config = ConfigParser()
    config.read('names.ini')

    index = config.getint('index', 'index')

    initials_list = []
    names_list = []
    for i in range(index):
        initials_list.append(config.get('initials', str(i)))
        names_list.append(config.get('names', str(i)))
    
    return initials_list, names_list

# No update_names_config here because I haven't implemented GUI names editing yet

# ----------------------------- Barcode functions ---------------------------- #

# Crop the image to the barcode area
def crop_barcode(image):
    ratio_height = 3507
    ratio_width = 2550
    
    h=int((300/ratio_height)*image.shape[0])
    w=int((420/ratio_width)*image.shape[1])

    y=int((0/ratio_height)*image.shape[0])
    x=int((65/ratio_width)*image.shape[1])
    crop = image[y:y+h, x:x+w]

    return crop

# Cursed code that doesn't exist
def read_barcode(image):
    barcode = cv2.barcode_BarcodeDetector()
    ok, decoded_info, decoded_type, corners = barcode.detectAndDecode(image)

# -------------------------- Miscellaneous functions ------------------------- #

# Delete all files in the /data and /images/output folders
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

# Enable/disable dark mode based on the value of dark_mode_var
def update_dark_mode():
    # If dark mode is enabled, set the theme to dark
    if dark_mode_var.get() == True:
        root.tk.call("set_theme", "dark") # Set the theme to dark
    else:
        root.tk.call("set_theme", "light") # Set the theme to light

# Show options for extracting trends from existing data files
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

# ------------------------------ Teams functions ------------------------------ #

# Open teams editor window
def open_teams_window():
    # If the teams window is going to be closed, save the teams info and close the window
    def on_close_teams():
        update_teams_config()
        refresh_team_options()
        teams_window.destroy()

    # When teams are enabled or disabled, save the teams config file and refresh the UI
    def on_teams_switch_toggled():
        update_teams_config()
        refresh_team_options()
        if enable_teams_var.get() == True:
            if not os.path.exists("data/team1.csv") or not os.path.exists("data/team2.csv"):
                create_teams_csv_files()

    # Load scores from teams csv files and update the UI
    def load_scores(team1_score_label, team1_x_count_label, team2_score_label, team2_x_count_label):

        #region (REPLACED BY LIST METHOD BELOW) Iterates through lines in the csv file and adds the scores to the respective variables, returns the total score and x count
        # def get_score(path):
        #     out_score = 0
        #     out_x_count = 0
        #     with open(path) as csv_file:
        #         csv_reader = csv.reader(csv_file, delimiter=',')
        #         line_count = 0
        #         for row in csv_reader:
        #             if line_count != 0:
        #                 out_score += int(row[3])
        #                 out_x_count += int(row[4])
        #             line_count += 1
        #     return out_score, out_x_count
        #endregion

        # Load scores from the CSV file path and put them in a list of tuples (score, x_count)
        def get_score_to_list(path):
            out_scores = []
            with open(path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        out_scores.append(tuple((int(row[3]), int(row[4]))))
                    line_count += 1
            return out_scores

        # Removes the appropriate number of worst scores from the score_list
        def drop_scores(score_list):
            score_list_sorted = sorted(score_list, key=lambda score_tuple: (score_tuple[0], score_tuple[1]))
            scores_to_drop = len(score_list_sorted) - keep_best_var.get()
            if scores_to_drop < 0: scores_to_drop = 0
            score_list_best = score_list_sorted[scores_to_drop:]
            return score_list_best
        
        def sum_scores(score_list):
            score = sum(score_tuple[0] for score_tuple in score_list)
            x_count = sum(score_tuple[1] for score_tuple in score_list)
            return score, x_count

        team1_score_list = get_score_to_list("data/team1.csv")
        team2_score_list = get_score_to_list("data/team2.csv")

        team1_score_list_best = drop_scores(team1_score_list)
        team2_score_list_best = drop_scores(team2_score_list)

        team1_score, team1_x_count = sum_scores(team1_score_list_best)
        team2_score, team2_x_count = sum_scores(team2_score_list_best)

        team1_score_label.config(text="Score: " + str(team1_score) + "-")
        team1_x_count_label.config(text=str(team1_x_count) + "X")
        team2_score_label.config(text="Score: "  + str(team2_score) + "-")
        team2_x_count_label.config(text=str(team2_x_count) + "X")

    #region Create teams window
    teams_window = tk.Toplevel(root)
    teams_window.title("Target Analysis")
    teams_window.minsize(width=600, height=640)
    teams_window.geometry("600x640")
    teams_window.tk.call('wm', 'iconphoto', teams_window._w, tk.PhotoImage(file='assets/icon.png'))
    teams_window.protocol("WM_DELETE_WINDOW", on_close_teams)
    #endregion

    #region Create frames
    teams_top_frame = ttk.Frame(teams_window)
    teams_top_frame.pack(side=TOP, pady=5, padx=5,  fill=X)

    teams_bottom_frame = ttk.Frame(teams_window)
    teams_bottom_frame.pack(side=TOP, pady=5, padx=5, fill=X)

    teams_controls_frame = ttk.Frame(teams_bottom_frame)

    teams_results_frame = ttk.Frame(teams_bottom_frame)
    #endregion

    #region Create enable teams switch
    global enable_teams_var
    enable_teams_switch = ttk.Checkbutton(teams_bottom_frame, text="Enable teams", variable=enable_teams_var, style='Switch.TCheckbutton', command=on_teams_switch_toggled)
    enable_teams_switch.pack(side=TOP, padx=5, pady=5)
    #endregion

    #region Notebook for tabbed view
    teams_notebook = ttk.Notebook(teams_bottom_frame)
    team1_frame = ttk.Frame(teams_notebook)
    team2_frame = ttk.Frame(teams_notebook)
    teams_notebook.add(team1_frame, text="Team 1")
    teams_notebook.add(team2_frame, text="Team 2")
    teams_notebook.pack(side=TOP, fill=X, padx=10, pady=5)
    #endregion

    teams_controls_frame.pack()

    teams_results_frame.pack()
    team1_results_frame = ttk.LabelFrame(teams_results_frame, text="Team 1")
    team2_results_frame = ttk.LabelFrame(teams_results_frame, text="Team 2")
    team1_results_frame.grid(row=2, column=0, padx=(0,15))
    team2_results_frame.grid(row=2, column=1, padx=(0,15))

    # Load scores button in teams_results_frame
    load_scores_button = ttk.Button(teams_controls_frame, text="Load scores", command=lambda: load_scores(team1_score_label, team1_x_count_label, team2_score_label, team2_x_count_label))
    load_scores_button.grid(row=0, column=0, padx=(0,10))
    keep_best_label = ttk.Label(teams_controls_frame, text="Keep best:")
    keep_best_label.grid(row=0, column=1, padx=(10,5))
    keep_best_entry = ttk.Entry(teams_controls_frame, width=5, textvariable=keep_best_var)
    keep_best_entry.grid(row=0, column=2, padx=(5, 0))

    #region Create labels
    teams_label = ttk.Label(teams_top_frame, text="Teams", font=BOLD)
    teams_label.pack()
    #endregion

    #region Create team 1 options
    team1_name_label = ttk.Label(team1_frame, text="Name")
    team1_name_label.grid(row=2, column=0, padx=10, pady=10)
    global team1_name_var
    team1_name_entry = ttk.Entry(team1_frame, textvariable=team1_name_var, width=20)
    team1_name_entry.grid(row=2, column=1, pady=10)
    #endregion

    #region Create team 2 options
    team2_name_label = ttk.Label(team2_frame, text="Name")
    team2_name_label.grid(row=2, column=0, padx=10, pady=10)
    global team2_name_var
    team2_name_entry = ttk.Entry(team2_frame, textvariable=team2_name_var, width=20)
    team2_name_entry.grid(row=2, column=1, pady=10)
    #endregion

    #region Create team 1 results
    team1_results_label = ttk.Label(team1_results_frame, text=team1_name_var.get() + "'s results", font=BOLD)
    team1_results_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    team1_score_label = ttk.Label(team1_results_frame, text="Please load scores")
    team1_score_label.grid(row=1, column=0, padx=10, pady=10)
    team1_x_count_label = ttk.Label(team1_results_frame, text="Please load scores")
    team1_x_count_label.grid(row=1, column=1, padx=10, pady=10)

    team1_open_csv_button = ttk.Button(team1_results_frame, text="Open CSV", command=lambda: open_file(os.path.abspath("data/team1.csv")))
    team1_open_csv_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    #endregion

    #region Create team 2 results
    team2_results_label = ttk.Label(team2_results_frame, text=team2_name_var.get() + "'s results", font=BOLD)
    team2_results_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    team2_score_label = ttk.Label(team2_results_frame, text="Please load scores")
    team2_score_label.grid(row=1, column=0, padx=10, pady=10)
    team2_x_count_label = ttk.Label(team2_results_frame, text="Please load scores")
    team2_x_count_label.grid(row=1, column=1, padx=10, pady=10)

    team2_open_csv_button = ttk.Button(team2_results_frame, text="Open CSV", command=lambda: open_file(os.path.abspath("data/team2.csv")))
    team2_open_csv_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    #endregion

# Create a default teams config file
def create_teams_config():
    config = ConfigParser()

    config.read('teams.ini')

    config.add_section('teams')
    config.set('teams', 'enable', str(enable_teams_var.get()))

    config.set('teams', 'team1_name', team1_name_var.get())
    config.set('teams', 'team2_name', team2_name_var.get())

    config.set('teams', 'keep_best', str(keep_best_var.get()))

    # Write the changes to the config file
    with open('teams.ini', 'w') as f:
        config.write(f)

# Update the teams config file from current state
def update_teams_config():
    config = ConfigParser()

    config.read('teams.ini')

    config.set('teams', 'enable', str(enable_teams_var.get()))
    config.set('teams', 'team1_name', team1_name_var.get())
    config.set('teams', 'team2_name', team2_name_var.get())
    config.set('teams', 'keep_best', str(keep_best_var.get()))

    # Write the changes to the config file
    with open('teams.ini', 'w') as f:
        config.write(f)

# Load teams info from teams.ini config file
def load_teams_config():
    config = ConfigParser()
    config.read('teams.ini')

    enable_teams_var.set(config.getboolean('teams', 'enable'))
    team1_name_var.set(config.get('teams', 'team1_name'))
    team2_name_var.set(config.get('teams', 'team2_name'))
    keep_best_var.set(config.getint('teams', 'keep_best'))

# Refresh the UI for the team selector on the main page
def refresh_team_options():
    global teams_frame
    team1_radio_button = ttk.Radiobutton(teams_frame, text=team1_name_var.get(), variable=active_team_var, value="team1")
    team1_radio_button.grid(row=0, column=0, padx=5, sticky=NSEW)
    team2_radio_button = ttk.Radiobutton(teams_frame, text=team2_name_var.get(), variable=active_team_var, value="team2")
    team2_radio_button.grid(row=0, column=1, padx=5, sticky=NSEW)

    global use_file_info_checkbutton
    global today_button
    if enable_teams_var.get():
        # Grid the teams frame
        teams_frame.grid(column=4, row=1, columnspan=2, padx=5)

        # Cycle the use file info checkbutton and assign it a rowspan of 1
        use_file_info_checkbutton.grid_forget()
        use_file_info_checkbutton.grid(column=5, row=0, padx=5)

        # Cycle the today button and reposition it
        today_button.grid_forget()
        today_button.grid(column=4, row=0, padx=2.5)
    else:
        # Ungrid the teams frame
        teams_frame.grid_forget()

        # Cycle the use file info checkbutton and revert it back to the original rowspan of 2
        use_file_info_checkbutton.grid_forget()
        use_file_info_checkbutton.grid(column=5, row=0, rowspan=2, padx=5)

        # Cycle the today button and revert it back to the original position
        today_button.grid_forget()
        today_button.grid(column=4, row=0, rowspan=2, padx=2.5)

# Create team1.csv and team2.csv files for storing scores
def create_teams_csv_files():
    with open('data/team1.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) # Create a filewriter
        filewriter.writerow(['Name', 'Date', 'Target Number', 'Score','X']) # Write the header row
        csvfile.close() # Close the file

    with open('data/team2.csv', 'x', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) # Create a filewriter
        filewriter.writerow(['Name', 'Date', 'Target Number', 'Score','X']) # Write the header row
        csvfile.close() # Close the file
    
    main_label.config(text="Created teams CSV files") # Update the main label

# ---------------------------- Settings functions ---------------------------- #

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
        #print(path)
        os.system("notepad " + path)

    main_label.config(text="Showing settings window") # Update the main label

    #region Create settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Target Analysis")
    settings_window.minsize(width=800, height=640)
    settings_window.geometry("800x640")
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

    settings_capitalize_frame = ttk.Frame(settings_window)
    settings_capitalize_frame.pack(side=TOP, fill=X, padx=5)

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
    settingstab5orion50ft = ttk.Frame(settings_tab_control)
    settingstab4names = ttk.Frame(settings_tab_control)

    settings_tab_control.add(settingstab1nraa17, text ='NRA A-17')
    settings_tab_control.add(settingstab2orion, text ='NRA/USAS-50 Orion 300dpi')
    settings_tab_control.add(settingstab3orionDPI2, text ='NRA/USAS-50 Orion 600dpi')
    settings_tab_control.add(settingstab5orion50ft, text ='Orion 50ft Conventional')
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
    settings_label2 = ttk.Label(settings_top_frame, text="Change these only if the software does not work properly!")
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
    global dark_mode_var
    dark_mode_checkbutton = ttk.Checkbutton(settings_dark_mode_frame, text='Use dark theme', style='Switch.TCheckbutton', variable=dark_mode_var, onvalue=True, offvalue=False, command=update_dark_mode)
    dark_mode_checkbutton.grid(column=0, row=0)

    # Auto capitalize names switch
    capitalize_names_checkbutton = ttk.Checkbutton(settings_capitalize_frame, text='Auto capitalize names', style='Switch.TCheckbutton', variable=capitalize_names_var, onvalue=True, offvalue=False)
    capitalize_names_checkbutton.grid(column=0, row=0)
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

    #region Create 50ft conventional widgets

    # Header label
    settings_label_50ft = ttk.Label(settingstab5orion50ft, text="50ft Conventional" , font='bold')
    settings_label_50ft.grid(row=0, column=0, columnspan=2)

    # Notes label
    settings_label_50ft_notes = ttk.Label(settingstab5orion50ft, text="Inherits from Orion and NRA for settings that aren't listed")
    settings_label_50ft_notes.grid(row=1, column=0, columnspan=2)

    nra_min_contour_area_label = ttk.Label(settingstab5orion50ft, text="50ft conv Min cnt area")
    nra_min_contour_area_label.grid(row=2, column=0)
    nra_min_contour_area_entry = ttk.Entry(settingstab5orion50ft, textvariable=orion50ftconventional_min_contour_area)
    nra_min_contour_area_entry.grid(row=2, column=1)

    nra_max_contour_area_label = ttk.Label(settingstab5orion50ft, text="50ft conv Max cnt area")
    nra_max_contour_area_label.grid(row=3, column=0)
    nra_max_contour_area_entry = ttk.Entry(settingstab5orion50ft, textvariable=orion50ftconventional_max_contour_area)
    nra_max_contour_area_entry.grid(row=3, column=1)

    nramax_hole_radius_label = ttk.Label(settingstab5orion50ft, text="50ft conv Max hole radius")
    nramax_hole_radius_label.grid(row=4, column=0)
    nramax_hole_radius_entry = ttk.Entry(settingstab5orion50ft, textvariable=orion50ftconventional_max_hole_radius)
    nramax_hole_radius_entry.grid(row=4, column=1)
    #endregion

    #region Create names
    # Frame is named 'settingstab4names'
    # notTODOrightnow: Add built in support for editing names file
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

    #region Create scanner widgets
    # scanner_label = ttk.Label(settingstab5scanner, text="Scanner Settings", font=BOLD)
    # scanner_label.grid(row=0, column=0, columnspan=2)
    # scanner_crop_pixels_label = ttk.Label(settingstab5scanner, text="Crop bottom pixels")
    # scanner_crop_pixels_label.grid(row=1, column=0)
    # scanner_crop_pixels_entry = ttk.Entry(settingstab5scanner, textvariable=scanner_crop_pixels)
    # scanner_crop_pixels_entry.grid(row=1, column=1)

    #endregion

    settings_window.protocol("WM_DELETE_WINDOW", on_close_settings) # If the settings window is closing, run the on_close_settings function

# ----------------------------- Config functions ----------------------------- #

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
    capitalize_names_var.set(config.getboolean("settings", "capitalize_names"))
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

    # 50ft conventional
    orion50ftconventional_min_contour_area.set(config.getint("50ftconventional", "50ftconventional_min_contour_area"))
    orion50ftconventional_max_contour_area.set(config.getint("50ftconventional", "50ftconventional_max_contour_area"))
    orion50ftconventional_max_hole_radius.set(config.getint("50ftconventional", "50ftconventional_max_hole_radius"))

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
    config.set('settings', 'capitalize_names', str(capitalize_names_var.get()))

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

    # Add the 50ft conventional section to the config file
    config.add_section('50ftconventional')
    # Settings for the 50ft convetional targets
    config.set('50ftconventional', '50ftconventional_min_contour_area', str(orion50ftconventional_min_contour_area.get()))
    config.set('50ftconventional', '50ftconventional_max_contour_area', str(orion50ftconventional_max_contour_area.get()))
    config.set('50ftconventional', '50ftconventional_max_hole_radius', str(orion50ftconventional_max_hole_radius.get()))

    # Write the changes to the config file
    with open(file, 'w') as f:
        config.write(f)

# Update config.ini file with current settings
def update_config():
    config = ConfigParser() # Create a config parser

    config.read('config.ini') # Read the config file

    # Update the settings in the config file
    config.set('settings', 'dpi', str(dpi_var.get()))
    config.set('settings', 'dark_mode', str(dark_mode_var.get()))
    config.set('settings', 'show_output_when_finished', str(show_output_when_finished_var.get()))
    config.set('settings', 'individual_output_type', str(individual_output_type_var.get()))
    config.set('settings', 'use_file_info', str(use_file_info_var.get()))
    config.set('settings', "capitalize_names", str(capitalize_names_var.get()))
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
    # Continue updating the settings for the 50ft conventional section
    config.set('nra', '50ftconventional_min_contour_area', str(orion50ftconventional_min_contour_area.get()))
    config.set('nra', '50ftconventional_max_contour_area', str(orion50ftconventional_max_contour_area.get()))
    config.set('nra', '50ftconventional_max_hole_radius', str(orion50ftconventional_max_hole_radius.get()))

    # Write the changes to the config file
    with open('config.ini', 'w') as f:
        config.write(f)

# -------------------------- Analyze image functions ------------------------- #

# Score a single NRA A-17 bull. Derived from improved.py
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

    spindle_radius = 2.83 # Technically 2.835mm based on averages
    outer_spindle_radius = 4.5 # Technically 4.5025mm
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

                with open(os.path.join("data\\", csv_name), 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Score a single Orion NRA/USAS-50 bull. Derived from analyze_image
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

    inner_spindle_radius = 2.835
    outer_spindle_radius = 4.5025
    #endregion

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

                step = outer_spindle_radius / 10               
                multiplier = 1
                while distance >= multiplier * step: multiplier += 1
                ones = 10 - (multiplier // 10)
                decimal = 10 - (multiplier % 10)
                if decimal == 10: decimal == 9 # Just in case
                #print(multiplier, ones, decimal)
                string_score = str(ones) + "." + str(decimal)
                cv2.putText(output, string_score, (int(hole_x-100),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                #region old
                # if distance-outer_spindle_radius <= pixel_ten or distance+outer_spindle_radius <= pixel_eight:
                #     print("X")
                #     cv2.putText(output, "X", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     x_count += 1
                # else:
                #     if distance+outer_spindle_radius <= pixel_seven:
                #         print("0")
                #         cv2.putText(output, "0", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     else:
                #         if distance+outer_spindle_radius <= pixel_six:
                #             print("1")
                #             cv2.putText(output, "1", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #             dropped_points += 1
                #         else:
                #             if distance+outer_spindle_radius <= pixel_five:
                #                 print("2")
                #                 cv2.putText(output, "2", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #                 dropped_points += 2
                #             else:
                #                 if distance+outer_spindle_radius <= pixel_four:
                #                     print("3")
                #                     cv2.putText(output, "3", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #                     dropped_points += 3
                #                 else:
                #                     print("Score more than 4 or low confidence: CHECK MANUALLY")
                #                     main_label.config(text="Bull " + str(image) + " low confidence")
                #endregion

                hole_ratio_x = (hole_x-a) / pixel_outer
                hole_ratio_y = (hole_y-a) / pixel_outer

                global csv_name

                with open(os.path.join("data\\", csv_name), 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, ones, decimal, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Score a single Orion NRA/USAS-50 bull using NRA A-17 scoring. Derived from analyze_orion_image and analyze_image
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

                with open(os.path.join("data\\", csv_name), 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# Score a single Orion 50ft conventional bull. Derived from analyze_image
def analyze_50ft_conventional(image):
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

    spindle_radius = 2.835
    outer_spindle_radius = 4.5025
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
    img_thresholded = cv2.inRange(img, (orion_thresh_min.get(), orion_thresh_min.get(), orion_thresh_min.get()), (orion_thresh_max.get(), orion_thresh_max.get(), orion_thresh_max.get()))
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
        if area<orion50ftconventional_max_contour_area.get() and area>orion50ftconventional_min_contour_area.get():
            #print("Area: " + str(area))
            # Draw the detected contour for debugging
            cv2.drawContours(output,[contour],0,(255,0,0),2)

            # Create an enclosing circle that can represent the bullet hole

            (hole_x,hole_y),hole_radius = cv2.minEnclosingCircle(contour)
            hole_center = (int(hole_x),int(hole_y))
            hole_radius = int(hole_radius)
            #print(hole_radius)
            if hole_radius <= orion50ftconventional_max_hole_radius.get():
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

                # # Touching X but not 0
                # if distance + outer_spindle_radius < pixel_eight and distance - outer_spindle_radius < pixel_nine:
                #     print("X")
                #     cv2.putText(output, "X", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     x_count += 1
                # # Touching X and 0
                # if distance + outer_spindle_radius > pixel_eight and distance - outer_spindle_radius < pixel_nine:
                #     print("0")
                #     cv2.putText(output, "0", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                # # Not touching X but touching 0 --> scores as a 1
                # if distance - outer_spindle_radius > pixel_nine and distance + outer_spindle_radius < pixel_seven:
                #     print("1")
                #     cv2.putText(output, "1", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     dropped_points += 1
                # if distance - outer_spindle_radius > pixel_eight and distance + outer_spindle_radius < pixel_six:
                #     print("2")
                #     cv2.putText(output, "2", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     dropped_points += 2
                # if distance - outer_spindle_radius > pixel_seven and distance + outer_spindle_radius < pixel_five:
                #     print("3")
                #     cv2.putText(output, "3", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     dropped_points += 3
                # if distance - outer_spindle_radius > pixel_six and distance + outer_spindle_radius < pixel_outer:
                #     print("4")
                #     cv2.putText(output, "4", (int(hole_x-50),int(hole_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                #     dropped_points += 4

                hole_ratio_x = (hole_x-a) / pixel_outer
                hole_ratio_y = (hole_y-a) / pixel_outer

                global csv_name

                with open(os.path.join("data\\", csv_name), 'a', newline="") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([image, dropped_points, x_count, hole_x, hole_y, distance, hole_ratio_x, hole_ratio_y])
                    csvfile.close()
    #endregion

    if individual_output_type_var.get() == "legacy":
        cv2.imshow("output", output) # Optional but make sure to use waitkey below if enabled, or else only image will show up.
        cv2.waitKey(0)
    cv2.imwrite(image + "-output.jpg", output) # Save the output image

# --------------------------------- Enums ------------------------------------ #

#region Explanation of the enums:
# TargetTypes has definitions for the left and right image on an NRA-A17 target.
# Scoring types simply has the NRA definition
# TargetTypes is used for load image and crop image
# While ScoringTypes is used for scoring images and opening a folder
# See TODO below for more info
#endregion

class TargetTypes(Enum):
    NRA_LEFT = 'nra-left'
    NRA_RIGHT = 'nra-right'
    ORION_USAS_50 = 'orion-usas-50'
    ORION_USAS_50_NRA_SCORING = 'orion-usas50-nrascoring'
    ORION_50FT_CONVENTIONAL = 'orion-50ft-conventional'

# TODOlater: Replace the separate TargetTypes and ScoringTypes with an optional left and right parameter
class ScoringTypes(Enum):
    NRA = 'nra-a17'
    ORION_USAS_50 = 'orion-usas-50'
    ORION_USAS_50_NRA_SCORING = 'orion-usas-50-as-nra'
    ORION_50FT_CONVENTIONAL = 'orion-50ft-conventional'

# ------------------------------ Driver program ------------------------------ #

#region Initialize tkinter
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
score_as_nra_var = tk.BooleanVar(root, False)

# Auto capitalize the first letter of the file name
capitalize_names_var = tk.BooleanVar(root, True)

# Teams
enable_teams_var = tk.BooleanVar(root, False)
team1_name_var = tk.StringVar(root, "Team 1")
team2_name_var = tk.StringVar(root, "Team 2")
active_team_var = tk.StringVar(root, "team1")
keep_best_var = tk.IntVar(root, 8)

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

#region Fine tuning settings for Orion 50ft conventional targets
orion50ftconventional_min_contour_area = tk.IntVar(root, 1000)
orion50ftconventional_max_contour_area = tk.IntVar(root, 5000)
orion50ftconventional_max_hole_radius = tk.IntVar(root, 40)
#endregion

# Check for a config file. If it exists, load the values from it. Otherwise, create a config file frome the defaults.
if os.path.isfile("config.ini"):
    # If the file exists, update settings to match the config file
    update_settings_from_config("config.ini")
else:
    # If the file does not exist, create it and set the default values
    create_default_config("config.ini")

# If there is not config backup, create one now
if not os.path.isfile("config-backup.ini"): create_default_config("config-backup.ini")    

# If there is not a names config, create one now
if not os.path.isfile("names.ini"): create_names_config()
#endregion

#region Menubar
menubar = tk.Menu(root) # Create the menubar

filemenu = tk.Menu(menubar, tearoff=0) # Create the file menu
filemenu.add_command(label="Show in Explorer", command=lambda: show_folder(os.getcwd()))
filemenu.add_command(label="Show output", command=show_output, state=DISABLED)
filemenu.add_command(label="Show trends", command=show_trends)
filemenu.add_command(label="Teams", command=open_teams_window)
filemenu.add_command(label="Scan image", command=scan_image)
filemenu.add_separator()
filemenu.add_command(label="Settings", command=open_settings)
filemenu.add_separator()
filemenu.add_command(label="Clear data", command=clear_data)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu) # Add the file menu to the menubar

helpmenu = tk.Menu(menubar, tearoff=0) # Create the help menu
helpmenu.add_command(label="README", command=lambda: open_file(os.path.abspath("README.md")))
helpmenu.add_command(label="Scanning diagram", command=lambda: open_file(os.path.abspath("help/scanner-digital.png")))
helpmenu.add_command(label="Accuracy screenshot", command=lambda: open_file(os.path.abspath("help/accuracy-vs-hand-scored.png")))
menubar.add_cascade(label="Help", menu=helpmenu) # Add the help menu to the menubar

root.config(menu=menubar) # Add the menubar to the root window
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

# Tabs for the different target types
tab0_indoor = ttk.Frame(tab_control)
tab1_orion = ttk.Frame(tab_control)
tab3_orion50ftconventional = ttk.Frame(tab_control)

# Add the tabs to the notebook and pack it
tab_control.add(tab0_indoor, text ='NRA A-17')
tab_control.add(tab1_orion, text ='Orion USAS-50')
tab_control.add(tab3_orion50ftconventional, text ='Orion 50ft conventional')
tab_control.pack(side=tk.TOP, fill=BOTH, padx=10, pady=10)

# Buttons frames are a child of the tabs
# Frames for the NRA A-17
buttons_frame = ttk.Frame(tab0_indoor)
buttons_frame.pack(side=tk.TOP)
bottom_frame = ttk.Frame(tab0_indoor)
bottom_frame.pack(side=tk.TOP)

# Frames for Orion USAS-50
orion_buttons_frame = ttk.Frame(tab1_orion)
orion_buttons_frame.pack(side=tk.TOP)
orion_bottom_frame = ttk.Frame(tab1_orion)
orion_bottom_frame.pack(side=tk.TOP)

# Frames for Orion 50ft conventional
orion50ft_buttons_frame = ttk.Frame(tab3_orion50ftconventional)
orion50ft_buttons_frame.pack(side=tk.TOP)
orion50ft_bottom_frame = ttk.Frame(tab3_orion50ftconventional)
orion50ft_bottom_frame.pack(side=tk.TOP)
#endregion

#region Main label
main_label = ttk.Label(top_frame, text="Load an image to get started")
main_label.pack(side=tk.TOP, padx=10, pady=5)

# Add a separator line
label_separator = ttk.Separator(top_frame, orient=HORIZONTAL)
label_separator.pack(side=TOP, fill=X)
#endregion

#region Date and name options
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

# Teams frame enabled only when teams are enabled
teams_frame = ttk.Frame(options_frame)
# Update teams info
if not os.path.exists("teams.ini"):
    create_teams_config()
load_teams_config()
refresh_team_options()

#endregion

#region NRA A-17 tab
# Layout:
# [Select left image] [Analyze target] [Select right image] [Open folder]

left_image_button = ttk.Button(buttons_frame, text = "Select left image", command=lambda: load_image(TargetTypes.NRA_LEFT))
left_image_button.grid(row=0, column=0, padx=5, pady=5)

analyze_target_button = ttk.Button(buttons_frame, text = "Analyze target", command = lambda: analyze_target(ScoringTypes.NRA))
analyze_target_button.grid(row=0, column=1, padx=5, pady=5)

right_image_button = ttk.Button(buttons_frame, text = "Select right image", command =lambda: load_image(TargetTypes.NRA_LEFT))
right_image_button.grid(row=0, column=2, padx=5, pady=5)

open_folder_nra_button = ttk.Button(buttons_frame, text = "Open folder", command=lambda: open_folder(ScoringTypes.NRA))
open_folder_nra_button.grid(row=0, column=3, padx=5, pady=5)

# NRA tab canvases
left_canvas = tk.Canvas(bottom_frame, width=230,height=300)
left_canvas.grid(row = 0, column = 0, padx=5, pady=5)

right_canvas = tk.Canvas(bottom_frame, width=230,height=300)
right_canvas.grid(row = 0, column = 1, padx=5, pady=5)
#endregion

#region Orion NRA/USAS-50 tab
# Layout:
# [Select image] [Analyze target] [Open folder] [Scan]
# (--o) Score as NRA A-17 target (--o) Name from bubbles

def on_load_image_orion_button_pressed():
    if score_as_nra_var.get(): load_image(TargetTypes.ORION_USAS_50_NRA_SCORING)
    else: load_image(TargetTypes.ORION_USAS_50)

def on_analyze_target_orion_button_pressed():
    if score_as_nra_var.get(): analyze_target(ScoringTypes.ORION_USAS_50_NRA_SCORING)
    else: analyze_target(ScoringTypes.ORION_USAS_50)

def on_scan_orion_button_pressed():
    if score_as_nra_var.get(): scan_process(TargetTypes.ORION_USAS_50_NRA_SCORING)
    else: scan_process(TargetTypes.ORION_USAS_50)

orion_tab_upper_buttons_frame = ttk.Frame(orion_buttons_frame)
orion_tab_lower_buttons_frame = ttk.Frame(orion_buttons_frame)
orion_tab_upper_buttons_frame.pack()
orion_tab_lower_buttons_frame.pack()

load_image_button = ttk.Button(orion_tab_upper_buttons_frame, text = "Select image", command=on_load_image_orion_button_pressed)
load_image_button.grid(row=0, column=0, padx=5, pady=5)

analyze_orion_target_button = ttk.Button(orion_tab_upper_buttons_frame, text = "Analyze target", command=on_analyze_target_orion_button_pressed)
analyze_orion_target_button.grid(row=0, column=1, padx=5, pady=5)

open_folder_orion_target_button = ttk.Button(orion_tab_upper_buttons_frame, text = "Open folder", command=lambda: open_folder(TargetTypes.ORION_USAS_50))
open_folder_orion_target_button.grid(row=0, column=2, padx=5, pady=5)

scan_process_orion_target_button = ttk.Button(orion_tab_upper_buttons_frame, text = "Scan", command=lambda: on_scan_orion_button_pressed())
scan_process_orion_target_button.grid(row=0, column=3, padx=5, pady=5)

score_as_nra_checkbutton = ttk.Checkbutton(orion_tab_lower_buttons_frame, text='Score as NRA A-17 target', style='Switch.TCheckbutton', variable=score_as_nra_var, onvalue=True, offvalue=False)
score_as_nra_checkbutton.grid(column=0, row=0, padx=5, pady=5)

use_bubbles_checkbutton = ttk.Checkbutton(orion_tab_lower_buttons_frame, text='Name from bubbles', style='Switch.TCheckbutton', variable=use_bubbles_var, onvalue=True, offvalue=False, command=update_config)
use_bubbles_checkbutton.grid(column=1, row=0, padx=5, pady=5)

# Orion tab canvas
orion_single_canvas = tk.Canvas(orion_bottom_frame, width=230,height=300)
orion_single_canvas.grid(row = 0, column = 0)
#endregion

#region Orion 50ft conventional tab
# Layout:
# [Select image] [Analyze target] [Open folder] [Scan]
#           (--o) Name from bubbles

load_image_conventional_button = ttk.Button(orion50ft_buttons_frame, text = "Select image", command=lambda: load_image(TargetTypes.ORION_50FT_CONVENTIONAL))
load_image_conventional_button.grid(row=0, column=0, padx=5, pady=5)

analyze_50ft_conventional_target_button = ttk.Button(orion50ft_buttons_frame, text = "Analyze target", command=lambda: analyze_target(ScoringTypes.ORION_50FT_CONVENTIONAL))
analyze_50ft_conventional_target_button.grid(row=0, column=1, padx=5, pady=5)

open_folder_conventional_button = ttk.Button(orion50ft_buttons_frame, text = "Open folder", command=lambda: open_folder(ScoringTypes.ORION_50FT_CONVENTIONAL))
open_folder_conventional_button.grid(row=0, column=2, padx=5, pady=5)

scan_process_conventional_target_button = ttk.Button(orion50ft_buttons_frame, text = "Scan", command=lambda: scan_process(TargetTypes.ORION_50FT_CONVENTIONAL))
scan_process_conventional_target_button.grid(row=0, column=3, padx=5, pady=5)

use_bubbles_checkbutton = ttk.Checkbutton(orion50ft_buttons_frame, text='Name from bubbles', style='Switch.TCheckbutton', variable=use_bubbles_var, onvalue=True, offvalue=False, command=update_config)
use_bubbles_checkbutton.grid(column=0, row=1, padx=5, pady=5, columnspan=4)

# Orion 50ft conventional canvas
orion_50ft_conventional_canvas = tk.Canvas(orion50ft_bottom_frame, width=230,height=300)
orion_50ft_conventional_canvas.grid(row = 0, column = 0)
#endregion

tk.mainloop()