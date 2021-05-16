import cv2
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()

image = cv2.imread(filedialog.askopenfilename())

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

cv2.imwrite("images/top-mid.jpg", crop1)
cv2.imwrite("images/top-right.jpg", crop2)
cv2.imwrite("images/upper-right.jpg", crop3)
cv2.imwrite("images/lower-right.jpg", crop4)
cv2.imwrite("images/bottom-right.jpg", crop5)
cv2.imwrite("images/bottom-mid.jpg", crop6)

# Open Explorer to the location of the images
#os.system("explorer " + '"' + os.getcwd() + "\images" + '"')

# Run the analysis program on all of the images
os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\top-mid.jpg" + '"')
os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\top-right.jpg" + '"')
os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\upper-right.jpg" + '"')
os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\lower-right.jpg" + '"')
os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\bottom-right.jpg" + '"')
os.system("python " + '"' + os.getcwd() + "\improved.py" + '"' + " --image " + '"' + os.getcwd() + "\images\\bottom-mid.jpg" + '"')