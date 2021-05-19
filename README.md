# Target Analysis

A target analysis system offering insights into accuracy

Currently, the target analysis Python script allows you to automatically:
- Score a target
- Save data to a CSV file

## Documentation
### Information

Created by Sigmond Kukla for the Mt. Lebanon Rifle Team from Thursday, May 6 to Saturday, May 22 of the year 2021.

Future people: Is COVID over yet?

RW1vcnkgaXMgY3V0ZS4=

### Measurements

*Disclaimer: This might not actually be what these rings are called... I'm just going off of what I used in the code.

Measurements used in the target analysis system (radius):
Outer ring   - 46.150 millimeters
Five ring    - 37.670 millimeters
Six ring     - 29.210 millimeters
Seven ring   - 20.750 millimeters
Eight ring   - 12.270 millimeters
Nine ring    - 3.810 millimeters

Scoring spindle on scoring gauge uses radius 2.8 millimeters (equivalent to ⌀5.6mm)

All of these millimeter values are converted to pixel values through calibration to the detected outer ring of the target.
The target analysis system uses Hough Circles to identify a large circle in the scanned image. If the ratio of the detected ring to the image size is incorrect, the circle will be multiplied to adjust it accordingly.

### Requirements

Install Python 3. This project was built using Python 3.9, so that is recommended if possible. When installing Python, be sure to check the "Add Python 3.x to PATH" box.

Ensure that the following Python packages are installed:

- opencv-python
- tkinter
- pillow
- os
- csv
- numpy
- math
- argparse
- datetime
- shutil
- matplotlib
- ttkthemes

You can do this automatically by running the install_dependencies.bat file in the Target-Analysis-main directory.

### Scanning

For a normal-sized scanner glass, two scans must be used.

1. Place the target on the scanner glass with the top left of the back of the target pressed firmly into the back right corner of the glass.
2. Scan the target to the computer, saving it as an IMAGE (jpeg file) in the Target Analysis -> "images" folder.
3. Rotate the target 180° so that the top left of the back of the page is now in the front left corner. Firmly press the top right into the back left of the scanner glass.
4. Scan the target to the computer, saving it as an IMAGE (jpeg file) in the Target Analysis -> "images" folder.

If you would like to use the Open Folder operation or automatic information parsing, make sure to name the scans as such:
<2 number day><3 letter shortened month><Year><left side or right><target number>.jpeg
For example:
"03jan2021left1.jpeg" and "03jan2021right1.jpeg"

**See https://github.com/PicoPlanetDev/Target-Analysis/blob/main/help/scanner-digital.png for a diagram.**

### Usage

To score a target:
1. Click File -> Load left image and select your scanned image for the left side (or click the [Select left image] button at the bottom)
2. Click File -> Load right image and select your scanned image for the right side (or click the [Select right image] button at the bottom)
3. Click File -> Analyze target (or click the [Analyze target] button at the bottom)
4. Click the [X] on the analysis windows to view results for each bull

Data from the analysis is stored in the data folder as data-<Name><Day><Month><Year><Target number>.csv

Alternatively, click File -> Show Output after analyzing a target to see each bull laid out in their real locations. Click the "Open Target CSV" button to open the CSV file for the target. Click the "Open Data CSV" file to open the CSV that contains all scanned targets.
You cannot use File -> Show Output if you analyzed multiple targets using the Open Folder method.

If "Use info from file" is selected, the program will automatically update the date and target number. This will overwrite all data and target number information in the box already. If the file is not named correctly, or you would like to use a different date or target number, make sure to deselect this option.
For this, you must name the target files as such:
<2 number day><3 letter shortened month><Year><left side or right><target number>.jpeg
For example:
"03jan2021left1.jpeg" and "03jan2021right1.jpeg"

You can click [Use Today] to set today's date and use target #1. The target number allows you to score multiple targets from the same person on the same day. When using this option, please make sure to disable "Use info from file" in this scenario.
You can also simply type in a date and target number, but please make sure to disable "Use info from file" in this scenario.

Type in a name that identifies the target. I prefer to use the shooter's name for this. It is preferable to make the name one word only (Sigmond or SigmondKukla for example) to avoid problems related to the path of files that use this name.

To score multiple targets:
1. Place all of the scanned targets into the images folder. Do not place any other files with the JPEG extension in the folder right now. If necessary, create a subfolder and move the extraneous files to that location.
2. Make sure that all targets are named correctly (as per the example above)
3. Click File -> Open folder and select the images folder
4. Wait until the label at the top of the window reads "Done"
5. To view data for an individual target, open Explorer to the data folder. Then, open any CSV file that is named as such:
    data-<name><day><month><year><target number>.csv
    For example:
    data-Sigmond03January20211.csv
6. To view data for all targets, open the data.csv file in the data folder.

To hide the black command prompt that appears when running this program, rename "gui.py" to "gui.pyw"