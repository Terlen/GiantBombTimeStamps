# Apply tophat morphological operation to highlight text
# Image pre-processing code heavily utilizes code from Adrian Rosebrock at https://www.pyimagesearch.com/2015/11/30/detecting-machine-readable-zones-in-passport-images/
import cv2
import argparse
import os
import numpy as np
import imutils
import pytesseract
import csv

imagefiles = os.listdir(".\\thumbs\\")
#print(imagefiles)
results = []
for frame in imagefiles:

    #print(frame)
    image = cv2.imread("C:\\Users\\aidan\\Programming Projects\\GiantBombTimeStamps\\thumbs\\"+frame)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,5))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) [1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=2)  

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # loop over the contours
    for c in cnts:
            # compute the bounding box of the contour and use the contour to
            # compute the aspect ratio and coverage ratio of the bounding box
            # width to the width of the image
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            crWidth = w / float(gray.shape[1])
            # check to see if the aspect ratio and coverage width are within
            # acceptable criteria
            if ar > 3:
                # pad the bounding box since we applied erosions and now need
                # to re-grow it
                pX = int((x + w) * 0.03)
                pY = int((y + h) * 0.03)
                (x, y) = (x - pX, y - pY)
                (w, h) = (w + (pX * 2), h + (pY * 2))
                # extract the ROI from the image and draw a bounding box
                # surrounding the MRZ
                roi = image[y:y + h, x:x + w].copy()
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break

    config = ("-l eng --oem 1 --psm 7")
    # cv2.imshow("Original", image)
    # cv2.waitKey(0)
    # cv2.imshow("GradX", gradX)
    # cv2.waitKey(0)
    # cv2.imshow("Tophat", roi)
    # cv2.waitKey(0)
    results.append(pytesseract.image_to_string(roi, config=config))

for text in results:
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
with open("results.csv", "x") as csv_file:
    i = 0
    writer = csv.writer(csv_file, delimiter=',')
    for text in results:
        writer.writerow((text+ "," + str(i*2)).split(','))
        i+=1
    
