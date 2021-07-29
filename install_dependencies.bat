REM This will install Python 3.9.6, add it to PATH and install the required packages for Target Analysis

REM Downloading Python 3.9.6
bitsadmin /transfer mydownloadjob /download /priority FOREGROUND "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" "C:\temp\python-3.9.6-amd64.exe"

REM Installing Python 3.9.6
REM Please check the box to "Add Python to PATH"
"C:\temp\python-3.9.6-amd64.exe"

REM Ensuring Python 3.9.6 is in PATH
SET PYTHONPATH="%USERPROFILE%\AppData\LOcal\Programs\Python\Python39\python.exe"
ECHO %PYTHONPATH%

REM Removing the Python installer
del "C:\temp\python-3.9.6-amd64.exe"

REM Installing dependencies
pip install opencv-python --upgrade
pip install pillow --upgrade
pip install numpy --upgrade
pip install matplotlib --upgrade
pip install ttkthemes --upgrade
pip install configparser --upgrade