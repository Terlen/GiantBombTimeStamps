# Process output strings from Tesseract to filter out erroneous results and identify initial timestamps of each unique string

from collections import Counter
import csv
import os.path

# Debugging function to generate data object from csv file stored to disk so I don't have to regenerate it each time I test!
def debugReadResults():
    data = []
    try :
        with open('results.csv', newline='') as results:
            reader = csv.reader(results)
            data = list(reader)
            return data
    except:
        print('No valid results.csv found.')
    



# Receive list of strings from OCR process and store in a Counter object to determine frequencies of each unique string
def listToCounter(results):
    stringCounter = Counter(results)