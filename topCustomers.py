#!/usr/bin/Python

# Top Customers


import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

products = requests.post('http://localhost:9200/_sql', data = 'SELECT SUM(SALES_VALUE) FROM transactions GROUP BY household_key LIMIT 10 ').json()
#print 'name, quantity, value'

N = 10
value = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
household_key_list = []

for product in products['aggregations']['household_key']['buckets']:
    household_key = product['key']
    print household_key
    quantity = product['doc_count']
    values = product['SUM(SALES_VALUE)']['value']
    name_json = requests.post('http://localhost:9200/_sql', data='SELECT AGE_DESC FROM demographics WHERE household_key = '+ str(household_key)).json()
    name = name_json['hits']['hits']
    new_name = []
    household_key_list.append(household_key)

    print household_key_list
    print "household_key:", household_key_list
    print "Length of Household_key:", len(household_key_list)
    print "quantity:", quantity
    print "values:", values
    n = len(household_key_list)
    ind = np.arange(n)
    width = 0.35


    for i in name_json['hits']['hits']:
        new_name.append(i['_source']['AGE_DESC'])



    p1 = plt.bar(ind, values, width, color="blue")
    p2 = plt.bar(ind, values, width, color="blue")
    plt.ylabel("Values")
    plt.title("Top Customers")
    plt.xticks(household_key_list)
    plt.show()

"""
3d GRAPH
        ax.bar(np.array(int(quantity)), np.array(values), [household_key], color="blue")

        #plt.bar(quantity, values, width, color="blue" )

ax.set_xlabel("Household_Key")

ax.set_ylabel("quantity")
ax.set_zlabel("Values")
ax.set_title("Top Customers with revenues, quantity of products bought")

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
