# Target Analysis

A target analysis system offering insights into accuracy

Currently, the target analysis Python script allows you to automatically:
- Score a target (NRA A-17 or NRA/USAS-50)
- Batch scoring
- Save data to Excel-ready CSV files
- Show most and least missed bulls
- Show single shooter trends across a range of dates

## Comparison to hand scoring
![Excel Spreadsheet](https://github.com/PicoPlanetDev/Target-Analysis/blob/main/help/accuracy-vs-hand-scored.png?raw=true)

## Installation
1. Install Python 3.9 from this page: https://www.python.org/downloads/release/python-395/
If the computer used runs Windows, please select the bottom option at the bottom of the page: Windows Installer (64-bit).
2. Run the installer, **making sure to check the "Add Python 3.x to PATH" box**.
3. Click the green ```↓ Code``` button at the top right of this Github page and select Download ZIP.
4. Extract the zipped folder to a prominent location, such as the Desktop or Documents directory.
5. Double click to run ```install_dependencies.bat```
6. Double click to run ```gui.pyw``` to run the analysis software.
7. The images folder includes two scanned targets to test functionality. Run the software (see the Usage section) and click Show Output, ensuring that a score of 94-4X is displayed.

## Documentation
### Information

Created by Sigmond Kukla for the Mt. Lebanon Rifle Team in May and June of 2021.

Future people: Is COVID over yet?

### Measurements

Documentation - Measurements

*Disclaimer: This might not actually be what these rings are called... I'm just going off of what I used in the code.

Measurements are from *NRA Smallbore Rifle Rules*

Measurements used in the target analysis system (radius):
NRA A-17 target:
Outer ring   - 46.150 millimeters
Five ring    - 37.670 millimeters
Six ring     - 29.210 millimeters
Seven ring   - 20.750 millimeters
Eight ring   - 12.270 millimeters
Nine ring    - 3.810 millimeters

NRA/USAS-50 target:
outer (three) = 33.38
four = 28.5
five = 23.63
six = 18.75
seven = 13.87
eight = 9
nine = 4.12
ten = 0.76

Inner scoring spindle on scoring gauge uses radius 2.8 millimeters (equivalent to ⌀5.6mm)
Outer scoring spindle uses radius 4.5 millimeters (equivalent to ⌀9mm)

All of these millimeter values are converted to pixel values through calibration to the detected outer ring of the target.
The target analysis system uses Hough Circles to identify a large circle in the scanned image. If the ratio of the detected ring to the image size is incorrect, the circle will be multiplied to adjust it accordingly.

### Requirements

Install Python 3. This project was built using Python 3.9, so that is recommended if possible. When installing Python, be sure to check the ```"Add Python 3.x to PATH"``` box.

Ensure that the following Python packages are installed:

- opencv-python
- pillow
- numpy
- matplotlib
- ttkthemes

You can do this automatically by running the **install_dependencies.bat** file in the Target-Analysis-main directory.

### Scanning

For a normal-sized scanner glass, two scans must be used for a standard NRA A-17 target.

1. Place the target on the scanner glass with the top left of the back of the target pressed firmly into the back right corner of the glass.
2. Scan the target to the computer, saving it as an IMAGE (jpeg file) in the Target Analysis -> "images" folder.
3. Rotate the target 180° so that the top left of the back of the page is now in the front left corner. Firmly press the top right into the back left of the scanner glass.
4. Scan the target to the computer, saving it as an IMAGE (jpeg file) in the Target Analysis -> "images" folder.

If you would like to use the Open Folder operation or automatic information parsing, make sure to name the scans as such:
<2 number day><3 letter shortened month><Year><left side or right><target number>.jpeg
For example:
"03jan2021left1.jpeg" and "03jan2021right1.jpeg"

![Scanning Diagram](https://github.com/PicoPlanetDev/Target-Analysis/blob/main/help/scanner-digital.png?raw=true)

For an Orion Scoring System NRA/USAS-50 target, only one scan is necessary. 
Make sure that the corner of the target with the barcode is aligned to the front-right corner of the scanner.

### Usage

To score a target:
1. Select a target type by clicking one of the tabs on the main screen: NRA A-17 or NRA/USAS-50. The NRA/USAS-50 is optimized for scoring an ORION target.
2. Click Select Image or Open Folder. If you are scanning an NRA A-17 target, please select an image for both sides of the target.
3. Click Analyze Target. Hit any key on the keyboard or click the [X] in the top right to see the next bull. The bulls are displayed in clockwise order, starting with the top-middle bull. The sighter bull(s) in the center are omitted.
4. a. Click File -> Show Output (as long as you scored a single target as opposed to using Open Folder) to see the score.
   b. Click File -> Show in Explorer, then open the data directory, then open data.csv to view scores for targets analyzed using Open Folder.


Data from the analysis is stored in the data folder as data-<Name><Day><Month><Year><Target number>.csv

If "Use info from file" is selected, the program will automatically update the date and target number. This will overwrite all data and target number information in the box already. If the file is not named correctly, or you would like to use a different date or target number, make sure to deselect this option.
For this to work, you must name the target files as such:
**NRA A-17:**
<2 number day><3 letter shortened month><Year><left/right><target number>.jpeg
For example:
"03jan2021left1.jpeg" and "03jan2021right1.jpeg"
**NRA/USAS-50:**
<2 number day><3 letter shortened month><Year><Shooter's name><target number>.jpeg
For example:
"03jan2021Sigmond1.jpeg"

You can click [Use Today] to set today's date and use target #1. The target number allows you to score multiple targets from the same person on the same day.
You can also simply type in a month, day, year, target number, and name.
When using either option, please make sure to disable "Use info from file" in this scenario.

The name should identify the target easily. I prefer to use the shooter's name for this. It is preferable to make the name one word only (Sigmond or SigmondKukla for example) to avoid problems related to the path of files that use this name.

**To show identified trends for a single shooter across a range of dates:**
1. Click File -> Show Trends.
2. Select Load Folder or Load File, depending on what trend you would like to see:
    a. Load Folder allows you to open the data folder (or another folder with output files in it) to see which bull has the lowest score on average versus the highest score.
    b. Load File allows you to select a CSV data file to see a graph of shooting performance including score and X Count.
Remember, these are designed for a single shooter. Please copy and paste data files / folder to another location to isolate them to score only a single shooter.


**Folder structure**
Target-Analysis
├───assets
├───data
├───help
├───images
│   └───output
└───old

**assets** - do not touch
**data** - contains output CSV files. Clear them manually by deleting them, or by using File -> Clear Data inside the software
**help** - contains some documentation
**images** - put targets that need to be scored here
**output** - do not touch, files inside are automatically overwritten
**old** - contains older versions of this software that have been superseded by the current version. I do not reccomend using them ;-)

### Folder structure
```Target-Analysis
├───assets
├───data
├───help
├───images
│   └───output
└───old
```

**assets** - do not touch
**data** - contains output CSV files. Clear them manually by deleting them, or by using File -> Clear Data inside the software
**help** - contains some documentation
**images** - put targets that need to be scored here
**output** - do not touch, files inside are automatically overwritten
**old** - contains older versions of this software that have been superseded by the current version. I do not reccomend using them ;-)