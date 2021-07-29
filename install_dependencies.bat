REM https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe

REM Downloading Python 3.9.6
bitsadmin /transfer mydownloadjob /download /priority FOREGROUND "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" "C:\temp\python-3.9.6-amd64.exe"

REM Install Python 3.9.6
REM Make sure to check the box to "Add Python to PATH"
"C:\temp\python-3.9.6-amd64.exe"

SET PYTHONPATH="%USERPROFILE%\AppData\LOcal\Programs\Python\Python39\python.exe"
ECHO %PYTHONPATH%

REM Install dependencies
pip install opencv-python --upgrade
pip install pillow --upgrade
pip install numpy --upgrade
REM pip install argparse --upgrade
pip install matplotlib --upgrade
pip install ttkthemes --upgrade
pip install configparser --upgrade
pause