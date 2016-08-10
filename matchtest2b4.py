
#Import packages
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import matplotlib.image
import numpy as np
import cv2
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

#Import homemade modules
import differencecalc1
import image_align2

Tk().withdraw()

#Write user-chosen filepaths to variables
template1 = askopenfilename(title="Choose a template image")
sample1 = askopenfilename(title="Choose an image to compare to template")

#Read the template and actual image and write the images to variables
plantemp = cv2.imread(template1) #template
shot = cv2.imread(sample1) #actual

#Align the actual image with the template image
image_align2.align_images(plantemp, shot)

#Re-read the actual image (now-aligned with template) and re-write the image to variable
shot = cv2.imread(sample1) #actual

#Create a visual of the difference between the two images using cv2.subtract
diff = cv2.subtract(shot, plantemp) #difference between the two

#Write the 'diff image to file
cv2.imwrite("/home/pi/Desktop/Planogram/output/matchtest2b_output/planoutput2.jpg", diff)

#Convert the 'diff' image to B&W
diff2 = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) #converting the 'diff' image to black and white

#Find the contours of the image
# [FUNCTION NOT IN USE CURRENTLY] ret, thresh = cv2.threshold(diff2,127,255,0)
# [FUNCTION NOT IN USE CURRENTLY] im2,contours,hierarchy = cv2.findContours(thresh, 1, 2) #find the border of the 'diff' image

# [NOT IN USE] cnt = contours[0]

# [NOT IN USE] area = cv2.contourArea(cnt)

# [FUNCTION NOT IN USE CURRENTLY] epsilon = 0.1*cv2.arcLength(cnt,True)
# [FUNCTION NOT IN USE CURRENTLY] approx = cv2.approxPolyDP(cnt,epsilon,True) #approximate the border to a rectangle

#Create 50/50 overlay of original image & difference image
diff3 = cv2.addWeighted(diff,0.5,plantemp,0.5,0)

save1 = asksaveasfilename(defaultextension=".jpg", title="Save the B&W difference image")
#save2 = asksaveasfilename(defaultextension=".jpg")
save3 = asksaveasfilename(defaultextension=".jpg", title="Save the RGB difference image")

#Write 'diff3' variable to file
#cv2.imwrite(save2, diff3)

#Run Zero_norm function on images to calculate per pixel and agg pixel density difference
percent_difference = round(float(differencecalc1.compare_images(plantemp, shot)),5)

#Actualize to a percentage value
percent_difference = round((percent_difference*(.05/.00003))*10,2)

#Convert the percent_difference variable to string so it can be printed with diff3
pct_diff = str(percent_difference)

pct_diff = "Shelf is " + pct_diff + "% different from planogram"

#Overlay difference calc over result image
result1 = cv2.putText(diff2, pct_diff, (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 3)

#Write 'diff2' variable to file
cv2.imwrite(save1, result1)

#Overlay difference calc over result image
result2 = cv2.putText(diff3, pct_diff, (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,255,0), 5)

#Write output image to file
cv2.imwrite(save3, result2)