
#-*- coding: utf-8 -*-
import yaml
import csv

customerWeekDict = {}

with open("/Users/Rick/Desktop/CSV/transaction_data.csv", 'r') as f:
    data = csv.reader(f, delimiter=',')
    next(data)
    for row in data:
        if row[0] not in customerWeekDict:
            customerWeekDict[row[0]] = []
        else:
            if int(row[9]) not in customerWeekDict[row[0]]:
                customerWeekDict[row[0]].append(row[9])
    f.close()

    WeekDict = {}
    for customer, newlist in customerWeekDict.items():
        WeekDict[customer] = len(newlist)

with open('/Users/Rick/Desktop/shopperCounts.yaml','w') as w:
    w.write(yaml.dump(WeekDict, default_flow_style=False))
w.close()


