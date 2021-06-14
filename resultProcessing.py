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

# Debug function to unpack CSV data into list with same structure as main program
def debugListUnpack(data):
    results = []
    # remove header
    data.pop(0)
    for record in data:
        results.append((record[0],record[1]))
    return results

def debugData():
    return debugListUnpack(debugReadResults())


# Receive list of strings from OCR process and store in a Counter object to determine frequencies of each unique string
def listToCounter(results):
    stringCounter = Counter(results)