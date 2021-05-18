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

Please use pip to ensure that the following Python packages are installed:

opencv-python
tkinter
pillow
os
csv
numpy
math
argparse
datetime
shutil
matplotlib

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

For each target, you can click [Use Today] to set today's date and use target #1. The target number allows you to score multiple targets from the same person on the same day.
If "Use info from file" is selected, the program will automatically update the date and target number.
For this, you must name the target files as such:
<2 number day><3 letter shortened month><Year><left side or right><target number>.jpeg

For example:
"03jan2021left1.jpeg" and "03jan2021right1.jpeg"

To score multiple targets:
1. Place all of the scanned targets into the images folder.
2. Make sure that all targets are named correctly (as per the example above)
3. Click File -> Open folder and select the images folder
4. Wait until the label at the top of the window reads "Done"
5. To view data for an individual target, open Explorer to the data folder. Then, open any CSV file that is named as such:
    data-<name><day><month><year><target number>.csv
    For example:
    data-Sigmond03January20211.csv
6. To view data for all targets, open the data.csv file in the data folder.