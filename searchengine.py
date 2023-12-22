import lib
import json
import os
from time import process_time_ns

def searcheIt(searchList, indexDict):
    relationRatio = {}

    for key in indexDict:
        relationRatio[key] = 0
        for word in searchList:
            if word in indexDict[key]:
                relationRatio[key] += indexDict[key][word]

    return relationRatio

def nBetter(n, resDict, resList):
    for i in range(n):
        max = ('', 0)
        for key in resDict:
            if resDict[key] >= max[1]:
                max = (key, resDict[key])

        resList.append(max[0])
        resDict.pop(max[0])

    return resDict, resList

indexData = {}
dataset = {}
searchQuery = {}

with open("datalist.json", encoding='utf8', errors='ignore') as file:
    indexData = json.load(file)

with open("dataset.json", encoding='utf8', errors='ignore') as file:
    jsonData = json.load(file)

    for i in jsonData["docs"]:
        dataset[i["id"]] = [i["question"], i["answer"], i["date"]]

while True:
    resultList = []

    os.system('cls' if os.name == 'nt' else 'clear')

    searchQuery["search"] = input("---what do you want?---\n")

    startTime = process_time_ns()

    searchQuery = lib.dataCleaner(searchQuery)

    if not searchQuery:
        del resultList
        continue

    resultDict = searcheIt(searchQuery['search'].split(' '), indexData)

    endTime = process_time_ns()

    print((endTime - startTime) / 1000000, 'milli-sec')

    print("\n")

    resultDict, resultList = nBetter(5, resultDict, resultList)
    count = 0
    turn = 0
    for res in resultList:
        count += 1

        print(dataset[res][0])
        print("****************************************")
        print(dataset[res][1])
        print("****************************************")
        print(dataset[res][2])
        print("___________________________________________________________________")

        if count == 5:
            turn += 1
            if input("{number} items displayed. do you want more? (y:1 - n:0) ... ".format(number=5*turn)) == "1":
                count = 0
                resultDict, resultList = nBetter(5, resultDict, resultList)
            else:
                del resultList
                break

    


