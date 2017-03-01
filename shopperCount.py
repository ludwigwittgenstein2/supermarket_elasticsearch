
#-*- coding: utf-8 -*-
import yaml
import csv

customerWeekDict = {}

with open("/Users/Rick/Desktop/CSV/transaction_data.csv", 'r') as f:
    data = csv.reader(f, delimiter=',')
    next(data)
    for row in data:
        saleValue = (round(float(row[5])))
        if row[0] not in customerWeekDict:
            customerWeekDict[row[0]] = {}
        else:
            if int(row[9]) not in customerWeekDict[row[0]]:
                customerWeekDict[row[0]][int(row[9])] = 1
            else:
                customerWeekDict[row[0]][int(row[9])] += 1
    f.close()

with open('/Users/Rick/Desktop/customerLoyalty.yaml','w') as w:
    w.write(yaml.dump(customerWeekDict, default_flow_style=False))
w.close()


