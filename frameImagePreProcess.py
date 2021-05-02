# Apply tophat morphological operation to highlight text
import cv2
import argparse
import os

imagefiles = os.listdir(".\\thumbs\\")
#print(imagefiles)

for frame in imagefiles:

    print(frame)
    image = cv2.imread("C:\\Users\\aidan\\Programming Projects\\GiantBombTimeStamps\\thumbs\\"+frame)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13,5))

    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

    #cv2.imshow("Original", image)
    cv2.imshow("Tophat", tophat)
    cv2.waitKey(0)
