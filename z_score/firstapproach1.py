#!/usr/bin/python

import yaml
import sys
import csv

# Global Variable for Dictionary and Product

customerSaleDict = {}
customerOverTimeDict = {}
productDict = {}
topHouseHoldList = []
bottomHouseHoldList = []

def readCSV():
    global customerSaleDict
    global customerOverTimeDict

    with open("/Users/Rick/Desktop/CSV/transaction_data2.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)
	for row in data:

            salesValue = (round(float(row[5])))
            # in this code, row[0] is HOUSEHOLD_KEY  and row[9] is SALES_VALUE

            if row[0] not in customerSaleDict:
                customerSaleDict[row[0]] = salesValue
            else:
                customerSaleDict[row[0]]+= salesValue

            if row[0] not in customerOverTimeDict:
                customerOverTimeDict[row[0]]= {}

                if row[9] not in customerOverTimeDict[row[0]]:
                    customerOverTimeDict[row[0]][row[9]] = salesValue
                else:
                    customerOverTimeDict[row[0]][row[9]] += salesValue
            else:

                if row[9] not in customerOverTimeDict[row[0]]:
                    customerOverTimeDict[row[0]][row[9]]= salesValue

                else:
                    customerOverTimeDict[row[0]][row[9]] += salesValue
    f.close()

    with open("/Users/Rick/Desktop/segments/customerSaleDict.yaml", 'wb' ) as f:
        f.write(yaml.dump(customerSaleDict,default_flow_style=False))
    f.close()

    with open("/Users/Rick/Desktop/segments/customerOverTimeDict.yaml", 'wb' ) as f:
        f.write(yaml.dump(customerOverTimeDict,default_flow_style=False))
    f.close()

def buildTopSaleHouseHoldList():
    global topHouseHoldList
    count = 0

    for houseHoldKey, salesValue in sorted(customerSaleDict.items(), key=lambda k:k[1],reverse=True):
        if count>10:
            break
        topHouseHoldList.append(houseHoldKey)
        count +=1

    print topHouseHoldList

    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'wb' ) as f:
        f.write(yaml.dump(topHouseHoldList,default_flow_style=False))
    f.close()

def buildBottomSaleHouseHoldList():
    global bottomHouseHoldList
    count = 0

    for houseHoldKey, salesValue in sorted(customerSaleDict.items(), key=lambda k:k[1]):
        if count >10:
          break
        bottomHouseHoldList.append(houseHoldKey)
        count +=1
    print bottomHouseHoldList

    with open('/Users/Rick/Desktop/segments/bottomHouseHoldList', 'wb' ) as f:
        f.write(yaml.dump(bottomHouseHoldList,default_flow_style=False))
    f.close()

def generatePlotTopSaleData():

    for houseHoldKey, weekdict in customerOverTimeDict.items():
        if houseHoldKey in topHouseHoldList:
            Weekly_list = [['week_no', 'sales_value']]
            for weekNo, salesValue in sorted(weekdict.items(), key=lambda k:int(k[0])):
                Weekly_list.append([weekNo,salesValue])
            print houseHoldKey, Weekly_list


def generatePlotBottomSaleData():

    for houseHoldKey, weekdict in customerOverTimeDict.items():
        if houseHoldKey in bottomHouseHoldList:
            Weekly_list = [['week_no', 'sales_value']]
            for weekNo, salesValue in sorted(weekdict.items(), key=lambda k:int(k[0])):
                Weekly_list.append([weekNo,salesValue])
            print houseHoldKey, Weekly_list

def main():

    global customerSaleDict
    global customerOverTimeDict
    global topHouseHoldList
    global bottomHouseHoldList

    if len(sys.argv) < 3 :
        print("Usages: {} --run complete/readcsv/tblist/plottbweek " .format(sys.argv[0]))
        sys.exit(-1)

    else:
        if sys.argv[1] == "--run":
            if sys.argv[2] == "complete" :
                readCSV()
                buildTopSaleHouseHoldList()
                buildBottomSaleHouseHoldList()
                generatePlotTopSaleData()
                generatePlotBottomSaleData()
            elif sys.argv[2] == "readcsv":
                readCSV()
            elif sys.argv[2] == "tblist" or sys.argv[2] == "plottbweek" :
                with open('/Users/Rick/Desktop/segments/customerSaleDict.yaml', 'rb' ) as f:
                    customerSaleDict = yaml.load(f)
                f.close()

                with open('/Users/Rick/Desktop/segments/customerOverTimeDict.yaml', 'rb' ) as f:
                    customerOverTimeDict = yaml.load(f)
                f.close()

                if sys.argv[2] == "tblist":
                    buildTopSaleHouseHoldList()
                    buildBottomSaleHouseHoldList()

                elif  sys.argv[2] == "plottbweek" :
                    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'rb' ) as f:
                        topHouseHoldList =  yaml.load(f)
                    f.close()

                    with open('/Users/Rick/Desktop/segments/bottomHouseHoldList', 'rb' ) as f:
                        bottomHouseHoldList =  yaml.load(f)
                    f.close()

                    generatePlotTopSaleData()
                    generatePlotBottomSaleData()
            else:
                print("Usages: {} --run complete/readcsv/tblist/plottbweek " .format(sys.argv[0]))
                sys.exit(-1)

        else:
            print("Usages: {} --run complete/readcsv/tblist/plottbweek " .format(sys.argv[0]))
            sys.exit(-1)

if __name__=="__main__":
    main()
