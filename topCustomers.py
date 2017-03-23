#!/usr/bin/Python

# Top Customers


import requests
import json
import numpy as np
import matplotlib.pyplot as plt

products = requests.post('http://localhost:9200/_sql', data = 'SELECT SUM(SALES_VALUE) FROM transactions GROUP BY household_key LIMIT 10 ').json()
#print 'name, quantity, value'

N = 10
value = []

for product in products['aggregations']['household_key']['buckets']:
    household_key = product['key']
    quantity = product['doc_count']
    values = product['SUM(SALES_VALUE)']['value']
    name_json = requests.post('http://localhost:9200/_sql', data='SELECT AGE_DESC FROM demographics WHERE household_key = '+ str(household_key)).json()
    name = name_json['hits']['hits']
    new_name = []

    for i in name_json['hits']['hits']:
        print i['_source']['AGE_DESC']
        new_name.append(i['_source']['AGE_DESC'])


"""
    names_AgeDesc = []
    names_Age =[]

    for i in name:
        names_Age.append(i['_source']['AGE_DESC'])

print names_Age

width = 0.35
ind = np.arange(N)

fig, ax = plt.subplots()
rects1 = ax.bar(ind, values, width)
ax.set_xticklabels(names_AgeDesc)
ax.set_title("Top 10 Consumers with Age Description")
plt.show()
"""



"""

print ind, 'np.arange(N)'

width = 0.35

fig, ax = plt.subplots()

rects1 = ax.bar(ind, value, width)
ax.set_xticklabels(names_AgeDesc)

ax.set_title("Top 10 Consumers with Age Description")

plt.show()

"""


"""
names = []
values = []

N = 10

for product in products['aggregations']['PRODUCT_ID']['buckets']:
    product_code = product['key']
    quantity = product['doc_count']
    value = product['SUM(SALES_VALUE)']['value']
    name_json = requests.post('http://localhost:9200/_sql',
                              data='select SUB_COMMODITY_DESC from products where PRODUCT_ID = ' + str(product_code)).json()
#   print name_json
    name = name_json['hits']['hits'][0]['_source']['SUB_COMMODITY_DESC']

#   print name, quantity, value

    names.append(name)
    values.append(value)

ind = np.arange(N)
print ind, 'np.arange(N)'
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(ind, values, width)
ax.set_xticklabels(names)
print names, values
ax.set_title("Top 10 Bought Products with Revenue")

plt.show()
"""
