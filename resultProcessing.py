# Process output strings from Tesseract to filter out erroneous results and identify initial timestamps of each unique string

from collections import Counter, defaultdict
import csv
from difflib import SequenceMatcher

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
def debugListUnpack(csvList):
    results = []
    # remove header
    csvList.pop(0)
    for record in csvList:
        results.append((record[0],int(record[1])))
    return results

def debugData():
    return debugListUnpack(debugReadResults())

def debugListToDict(ocrOutputList):
    debugDict = defaultdict(list)
    for item in ocrOutputList:
        debugDict[item[0]].append(item[1])
    return debugDict

def debugProcessingTest():
    ocrInput = debugData()
    ocrInput = debugListToDict(ocrInput)
    output = combineSimilarTopics(ocrInput)
    print(output)
    output = earliestFrame(output)
    return output

# Receive list of strings from OCR process and store in a Counter object to determine frequencies of each unique string
def listToFilteredCounter(ocrOutputList,occuranceCutoff=2):
    # counter to determine number of occurances for all unique strings, including potential OCR errors
    stringCounter = Counter([item[0] for item in ocrOutputList])
    # create new Counter omitting strings that occur less than number of times specified by occuranceCutoff.
    filteredCounter = Counter({text: instances for text, instances in stringCounter.items() if instances >= occuranceCutoff})
    return filteredCounter

# Determine the earliest frame in which each string occured. Return dict with string:frameNumber
def earliestStringOccurance(Counter,ocrOutput):
    return {
        key: min([int(row[1]) for row in ocrOutput if row[0] == key])
        for key in Counter.keys()
    }

def earliestFrame(ocrOutputDict):
    return {key: min(ocrOutputDict[key]) for key in ocrOutputDict.keys()}


def stringSimilarity(a,b):
    print((SequenceMatcher(None, a, b).ratio())*100)
    return (SequenceMatcher(None, a, b).ratio())*100

# Find topics that appear for 10 seconds (2 frame samples) or less. If these topics are OCR errors of other topics, correct to the most similar topic.
def findInfrequentTopics(ocrOutputDict):
    # topicCount = {key: len(ocrOutputDict[key]) for key in ocrOutputDict.keys()}
    return [key for key in ocrOutputDict.keys() if len(ocrOutputDict[key]) <= 2]
    # infrequentTopics = {}
    # for key in topicCount.keys():
    #     if topicCount[key] <= 2:
    #         infrequentTopics[key] = topicCount[key]

def combineSimilarTopics(ocrOutputDict):
    infrequentTopics = findInfrequentTopics(ocrOutputDict)
    combinedDict = dict(ocrOutputDict)
    #print("Infrequent Topics: ", infrequentTopics)
    #print("CombinedDict: ",combinedDict)
    for topic in infrequentTopics:
        print(topic)
        for key in combinedDict.keys():
            print(key)
            #print(stringSimilarity(topic, key))
            if 95 <= stringSimilarity(topic, key) < 100:
                print("Similarity found: "+topic+key)
                combinedDict[key] += combinedDict.pop(topic, None)
                break
    for key in combinedDict.keys():
        combinedDict[key].sort()
            
    return combinedDict
            
                

