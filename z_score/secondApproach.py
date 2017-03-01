#!/usr/bin/python

import yaml
import sys
import csv

# Global Variable for Dictionary and Product

customerSaleDict = {}
customerWeekSalesDict = {}
customerWeekZscoreDict = {}
topCompleteHouseHoldList = []

def readCSV():
    global customerSaleDict
    global customerWeekSalesDict
    global customerWeekZscoreDict
    with open("/Users/Rick/Desktop/CSV/transaction_data2.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)
	for row in data:

            salesValue = (round(float(row[5])))
            # in this code, row[0] is HOUSEHOLD_KEY  and int(row[9]) is SALES_VALUE

            if row[0] not in customerSaleDict:
                customerSaleDict[row[0]] = salesValue
            else:
                customerSaleDict[row[0]]+= salesValue

            if row[0] not in customerWeekSalesDict:
                customerWeekSalesDict[row[0]]= {}

            if row[0] not in customerWeekSalesDict:
                customerWeekSalesDict[row[0]]= {}

            if row[0] not in customerWeekZscoreDict:
                customerWeekZscoreDict[row[0]] = {}

                if int(row[9]) not in customerWeekSalesDict[row[0]]:
                    customerWeekSalesDict[row[0]][int(row[9])] = salesValue
                else:
                    customerWeekSalesDict[row[0]][int(row[9])] += salesValue
            else:

                if int(row[9]) not in customerWeekSalesDict[row[0]]:
                    customerWeekSalesDict[row[0]][int(row[9])]= salesValue

                else:
                    customerWeekSalesDict[row[0]][int(row[9])] += salesValue
    f.close()

    with open("/Users/Rick/Desktop/segments/customerSaleDict.yaml", 'w' ) as f:
        f.write(yaml.dump(customerSaleDict,default_flow_style=False))
    f.close()

    with open("/Users/Rick/Desktop/segments/customerWeekSalesDict.yaml", 'w' ) as f:
        f.write(yaml.dump(customerWeekSalesDict,default_flow_style=False))
    f.close()

def computerZscoreSalesValue():
    for houseHoldKey, weekDict in customerWeekSalesDict.items():
        customerMean = 0.0
        customerStandardDeviation = 0.0
        numberofWeeks = 0
        sumofDifference = 0.0

    # Computing Mean for each customer Sales_Value
        for weekNo,salesValue in weekDict.items():
            customerMean +=  salesValue
            numberofWeeks += 1
        customerMean /=  numberofWeeks

    # Computing standard Derivation for each customer Sales_Value
        for weekNo,salesValue in weekDict.items():
            sumofDifference += (salesValue - customerMean)**2
        sumofDifference /= numberofWeeks
        customerStandardDeviation = (sumofDifference)**0.5

    # Computing Zscore for each sale Value
        for weekNo,salesValue in weekDict.items():
            print weekNo, salesValue,customerMean,customerStandardDeviation
            if customerStandardDeviation == 0.0:
                customerWeekZscoreDict[houseHoldKey][weekNo] = 0.0
            else:
                customerWeekZscoreDict[houseHoldKey][weekNo] = float("%.2f" % (( salesValue - customerMean )/ customerStandardDeviation))

    with open("/Users/Rick/Desktop/segments/customerWeekZscoreDict.yaml", 'w' ) as f:
        f.write(yaml.dump(customerWeekZscoreDict,default_flow_style=False))
    f.close()

    count = 0

def buildTopList():
    global topCompleteHouseHoldList

    for houseHoldKey, salesValue in sorted(customerSaleDict.items(), key=lambda k:k[1],reverse=True):
        topCompleteHouseHoldList.append(houseHoldKey)
    print topCompleteHouseHoldList

    with open('/Users/Rick/Desktop/segments/topCompleteHouseHoldList', 'wb' ) as f:
        f.write(yaml.dump(topCompleteHouseHoldList,default_flow_style=False))
    f.close()

def plotCustomerTrend():
    count =0
    for houseHoldKey, weekdict in customerWeekZscoreDict.items():
        if houseHoldKey in topCompleteHouseHoldList:
            if count == 20:
                break
            Weekly_list = [['week_no', 'zscore_value']]
            for weekNo, zscoreValue in sorted(weekdict.items(), key=lambda k:int(k[0])):
                Weekly_list.append([weekNo,zscoreValue])
            print houseHoldKey, Weekly_list
            count += 1

def main():
    readCSV()
    computerZscoreSalesValue()
    buildTopList()
    plotCustomerTrend()
if __name__=="__main__":
    main()
