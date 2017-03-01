#!/usr/bin/python

import yaml
import sys
import csv

# Global Variable for Dictionary and Product
customerWeekProductDict = {}
productDict = {}
topHouseHoldList = []
bottomHouseHoldList = []

def readCSV():
    global customerWeekProductDict
    global productDict
    with open("/Users/Rick/Desktop/CSV/transaction_data2.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)
	for row in data:

            if row[0] not in customerWeekProductDict:
                customerWeekProductDict[row[0]]= {}

                if row[9] not in customerWeekProductDict[row[0]]:
                    customerWeekProductDict[row[0]][row[9]] = {}
                    customerWeekProductDict[row[0]][row[9]][row[3]] = []
                else:
                    if row[3] not in customerWeekProductDict[row[0]][row[9]]:
                        customerWeekProductDict[row[0]][row[9]][row[3]] = []
            else:
                if row[9] not in customerWeekProductDict[row[0]]:
                    customerWeekProductDict[row[0]][row[9]] = {}
                    customerWeekProductDict[row[0]][row[9]][row[3]] = []
                else:
                    if row[3] not in customerWeekProductDict[row[0]][row[9]]:
                        customerWeekProductDict[row[0]][row[9]][row[3]] = []
    f.close()

    print("3D building is done")

    with open("/Users/Rick/Desktop/CSV/product.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)

        for row in data:
            if row[0] not in productDict:
                productDict[row[0]] = [row[2],row[3],row[4],row[5]]
    f.close()

    print("productDict is done")

    for houseHoldKey, dict1 in customerWeekProductDict.items():
        for weekNo, dict2 in dict1.items():
            for productID, valueList in dict2.items():
                for data in productDict[productID] :
                    valueList.append(data)
    print("Completed")
    with open("/Users/Rick/Desktop/segments/productDict.yaml", 'w' ) as f:
        f.write(yaml.dump(productDict,default_flow_style=False))
    f.close()

    with open("/Users/Rick/Desktop/segments/customerWeekProductDict.yaml", 'w' ) as f:
        f.write(yaml.dump(customerWeekProductDict,default_flow_style=False))
    f.close()

def main():
    readCSV()

if __name__=="__main__":
    main()
