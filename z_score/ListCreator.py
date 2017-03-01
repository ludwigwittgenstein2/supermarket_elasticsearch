import yaml
import sys
import csv

CustomerSaleDict = {}
CustomerOverTimeDict = {}
CustomerProductDict = {}
CustomerOverTimeDict_list = [] #This is empty list
topHouseHoldList = []
bottomHouseHoldList = []

def readCSV():
    global CustomerSaleDict
    global CustomerOverTimeDict
    CustomerProductDict = {}
    CustomerOverTimeDict_list = [] #This is empty list
    topHouseHoldList = []
    bottomHouseHoldList = []

    with open("/Users/Rick/Desktop/CSV/transaction_data2.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)
	for row in data:

            SALES_VALUE = (round(float(row[5])))

            if row[0] not in CustomerSaleDict:
                CustomerSaleDict[row[0]] = SALES_VALUE
            else:
                CustomerSaleDict[row[0]]+= SALES_VALUE

            if row[0] not in CustomerOverTimeDict:
                CustomerOverTimeDict[row[0]]= {}
                if row[9] not in CustomerOverTimeDict[row[0]]:
                    CustomerOverTimeDict[row[0]][row[9]] = SALES_VALUE
                else:
                    CustomerOverTimeDict[row[0]][row[9]] += SALES_VALUE
            else:
                if row[9] not in CustomerOverTimeDict[row[0]]:
                    CustomerOverTimeDict[row[0]][row[9]]= SALES_VALUE
                else:
                    CustomerOverTimeDict[row[0]][row[9]] += SALES_VALUE

    f.close()
    with open("/Users/Rick/Desktop/segments/CustomerSaleDict.yaml", 'w' ) as f:
        f.write(yaml.dump(CustomerSaleDict,default_flow_style=False))
    f.close()

    with open("/Users/Rick/Desktop/segments/CustomerOverTimeDict.yaml", 'w' ) as f:
        f.write(yaml.dump(CustomerOverTimeDict,default_flow_style=False))
    f.close()

def updateTopSaleHouseHoldList():
    global topHouseHoldList
    count = 0
    for household_key, value in sorted(CustomerSaleDict.items(), key=lambda k:k[1],reverse=True):
        if count>10:
            break
        topHouseHoldList.append(household_key)
        count +=1
    print topHouseHoldList
    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'w' ) as f:
        f.write(yaml.dump(topHouseHoldList,default_flow_style=False))
    f.close()

def updateBottomSaleHouseHoldList():
    global bottomHouseHoldList
    count = 0
    for household_key, value in sorted(CustomerSaleDict.items(), key=lambda k:k[1]):
        if count >10:
          break
        bottomHouseHoldList.append(household_key)
        count +=1
    print bottomHouseHoldList

    with open('/Users/Rick/Desktop/segments/bottomHouseHoldList', 'w' ) as f:
        f.write(yaml.dump(bottomHouseHoldList,default_flow_style=False))
    f.close()

def generatePlotTopSaleData():
    for household_key, value in CustomerOverTimeDict.items():
        if household_key in topHouseHoldList:
            Weekly_list = [['week_no', 'sales_value']]
            for week_no, sales_value in value.items():
                Weekly_list.append([week_no,sales_value])
            print household_key, Weekly_list


def generatePlotBottomSaleData():
    for household_key, value in CustomerOverTimeDict.items():
        if household_key in bottomHouseHoldList:
            Weekly_list = [['week_no', 'sales_value']]
            for week_no, sales_value in value.items():
                Weekly_list.append([week_no,sales_value])
            print household_key, Weekly_list


def main():

    global CustomerSaleDict
    global CustomerOverTimeDict
    global topHouseHoldList
    global bottomHouseHoldList
    if len(sys.argv) < 3 :
        print("Usages: {} --run complete/readcsv/tblist/plottbweek " .format(sys.argv[0]))
        sys.exit(-1)
    else:
        if sys.argv[1] == "--run":
            if sys.argv[2] == "complete" :
                readCSV()
                updateTopSaleHouseHoldList()
                updateBottomSaleHouseHoldList()
                generatePlotTopSaleData()
                generatePlotBottomSaleData()
            elif sys.argv[2] == "readcsv":
                readCSV()
            elif sys.argv[2] == "tblist" or sys.argv[2] == "plottbweek" :
                with open('/Users/Rick/Desktop/segments/CustomerSaleDict.yaml', 'r' ) as f:
                    CustomerSaleDict = yaml.load(f)
                f.close()

                with open('/Users/Rick/Desktop/segments/CustomerOverTimeDict.yaml', 'r' ) as f:
                    CustomerOverTimeDict = yaml.load(f)
                f.close()

                if sys.argv[2] == "tblist":
                    updateTopSaleHouseHoldList()
                    updateBottomSaleHouseHoldList()

                elif  sys.argv[2] == "plottbweek" :
                    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'r' ) as f:
                        topHouseHoldList =  yaml.load(f)
                    f.close()

                    with open('/Users/Rick/Desktop/segments/bottomHouseHoldList', 'r' ) as f:
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
