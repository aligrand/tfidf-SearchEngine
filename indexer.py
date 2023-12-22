import json
import lib

def dataIndexer(dataDict):
    iDict = {}
    idfDict= {}

    ddLen = len(dataDict)

    for key in dataDict:
        for word in dataDict[key].split(" "):
            if word not in idfDict:
                idfDict[word] = lib.idf(ddLen, lib.df(word, dataDict))
                print("idf..." + key + "..." + word)

    for key in dataDict:
        iDict[key] = {}
        for word in dataDict[key].split(" "):
            if word not in iDict[key]:
                iDict[key][word] = lib.tf(word, dataDict[key]) * idfDict[word]
                print("tf-idf..." + key + "..." + word)

    return iDict


datasetDict = {}
indexDict = {}

with open("dataset.json", encoding='utf8', errors='ignore') as file:
    jsonData = json.load(file)

    for i in jsonData["docs"]:
        datasetDict[i["id"]] = i["question"]

datasetDict = lib.dataCleaner(datasetDict)

with open("datasetClean.json", encoding='utf8', mode='w') as file:
    json.dump(datasetDict, file, ensure_ascii=False)

indexDict = dataIndexer(datasetDict)

with open("datalist.json", encoding='utf8', mode='w') as file:
    json.dump(indexDict, file, ensure_ascii=False)

