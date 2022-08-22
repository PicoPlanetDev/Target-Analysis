REM clone the repo
cd "D:\Libraries\Documents\Programming\"
mkdir "Target-Analysis-Build"
cd "Target-Analysis-Build"
git clone https://github.com/PicoPlanetDev/Target-Analysis

REM build
cd "Target-Analysis"
pyinstaller gui.spec

explorer "D:\Libraries\Documents\Programming\Target-Analysis-Build\Target-Analysis\dist"