# Target Analysis

A target analysis system offering insights into accuracy

Currently, the target analysis Python script allows you to automatically:
- Score a target (NRA A-17 or NRA/USAS-50)
- Batch scoring
- Save data to Excel-ready CSV files
- Show most and least missed bulls
- Show single shooter trends across a range of dates

## License
Please see [LICENSE.md](https://github.com/PicoPlanetDev/Target-Analysis/blob/main/LICENSE.md) for license information. This work is published under exclusive copyright to the developer.

## Comparison to hand scoring
![Excel Spreadsheet](https://github.com/PicoPlanetDev/Target-Analysis/blob/main/help/accuracy-vs-hand-scored.png?raw=true)

## Installation
1. Double click to run ```install_dependencies.bat```
2. Double click to run ```gui.pyw``` to run the analysis software.
3. The images folder includes two scanned targets to test functionality. Run the software (see the Usage section) and click Show Output, ensuring that a score of 94-4X is displayed.

## Documentation
### Information

Created by Sigmond Kukla for the Mt. Lebanon Rifle Team in May, June, and July of 2021.

Future people: Is COVID over yet?

### Measurements

Documentation - Measurements

*Disclaimer: This might not actually be what these rings are called... I'm just going off of what I used in the code.

Measurements are from *NRA Smallbore Rifle Rules* January 2010 booklet.

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

Python 3 and the following Python packages must be installed:

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


Data from the analysis is stored in the data folder as 

data-[Name][Day][Month][Year][Target number].csv

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

**If Target Analysis is not working properly:**

Click File -> Settings to open the settigs menu.

Then, ensure that the DPI setting matches your scanner's selected DPI.
The 300dpi setting is active by default.

Test Target Analysis again. If it still doesn't work, open settings and select the tab corresponding with the targets that you are scanning (either NRA A-17 or NRA/USAS-50). Then, tune the settings shown and retry the software after each change.

If you are unsure what settings to change or cannot make Target Analysis work properly, please email Sigmond at picoplanetdev@gmail.com or skukla61@mtlstudents.net, making sure to include screenshots of the issue.

**Tuning overview**

To tune the target analysis software, open the settings menu by pressing File -> Settings.
Then, select the tab that corresponds with the target that you are trying to tune (NRA A-17 or NRA/USAS-50).

Settings with the DPI 1 notation correspond with the 300dpi scanner setting. Settings with the DPI 2 notation correspond with the 600dpi setting. These are not linked, but I reccomend only changing settings that correspond with your active DPI (at the top of the settings menu). 

Please note that there was not a noticeable accuracy increase when using the 600dpi mode for NRA A-17 targets, so if that mode is enabled, targets will automatically be scaled in accordance with a 300dpi resolution. Using an unecessarily high DPI results in slower target processing with more CPU cost, therefore, it is discouraged. NRA/USAS-50 targets *do* score more accurately when using the 600dpi mode due to their smaller size. Therefore, the 600dpi mode is present in the analysis algorithm for NRA/USAS-50 targets. If your scanner supports 600dpi, I encourage you to take advantage of it for NRA/USAS-50 targets.

**These settings affect the ring detection on each bull**
- Kernel Size: Affects the blur kernel used on the grayscale bull image to smooth it and remove some high-frequency noise. Higher values result in a stronger blur. Because the blur kernel is 2D, this value is passed for both kernel dimensions.
- Param 1: Affects the sensitivity of the Hough Circles detector. Higher values result in stronger edges being detected. If this is set too high, no circles will be detected. If it is set too low, more circles will be detected including false cicles. Aim for only one circle to be detected when tuning this parameter. See this StackExchange answer for more details: https://dsp.stackexchange.com/a/22649
- Param 2: Affects the number of points that must be detected on one circle for it to be used. Higher values result in stronger circles being detected. If this is set too high, no circles will be detected. If it is set too low, more circles will be detected including false cicles. Aim for only one circle to be detected when tuning this parameter. See this StackExchange answer for more details: https://dsp.stackexchange.com/a/22649
- Min Circle Radius: Any circles detected by Hough Circles will be discarded if they are smaller than this radius.
**These settings affect the bullet hole detection**
- Thresh Min: The bullet hole detection system applies a threshold to the image, making it black if below this value or white if above this value and below the max value. This is to make contours more apparent to the contour detector. Range from 0 to 255.
- Thresh Max: This is the max value that the threshold uses. Not reccomended to change this.
- Morphology Opening Kernel Size: An opening morphology filter is applied to the black and white image to reduce noise. This process erodes the image (making white areas smaller), then dilates the image (making white areas larger). Small dots of noise are removed in the erosion and never appear in the dilation, but larger areas remain unchanged by the filter. This kernal size affects the number of pixels that are counted when performing these operations. Similar to the blur kernal size, this value is applied to both axes.
- Min cnt area: This defines the minimum area of a detected contour for it to be kept.
- Max cnt area: This defines the maximum area of a detected contour for it to be kept.
- Max hole radius: If a contour is detected, and it passes the min/max area filter, and its size is smaller than this radius, it is counted as a bullet hole and scored.

### Folder structure
```Target-Analysis
├───assets
├───data
├───help
├───images
│   └───output
└───old
```

**assets** - Do not edit.

**data** - Contains output CSV files. Clear them manually by deleting them, or by using File -> Clear Data inside the software. Files in this folder may be opened in a program such as Excel or Calc. Files in this folder may be copied to another folder to preserve them for future reference.

**help** - Contains documentation files. Not reccomended to edit anything in this folder, although files in this folder may be manually opened in a programs such as Notepad (TXT) or Photos (PNG).

**images** - Put targets that need to be scored here. You can set this as your default scanning directory so that the scanner automatically sends them here.

**images/output** - Do not edit while Target Analysis is running, files inside are automatically overwritten every time a target is scored. Files in this folder may be viewed for debugging or scrutiny. Files in this folder may be copied to another folder to preserve them for future reference.

**old** - Contains older versions of this software that have been superseded by the current version. I do not reccomend using them

### Developer's note

This is getting to be a pretty long readme, so I guess it's best to cut it short here.
I really enjoyed developing Target Analysis (gotta think of a better name maybe) and hope that it can be of use to someone. If you have anything that you would like to see in the software, please let me know. Also, I would appreciate it if you sent me any bugs or issues that you have found. I would be happy to help sort them out.

Thanks for using Target Analysis!
Sigmond