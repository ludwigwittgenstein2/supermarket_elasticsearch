#!/usr/bin/Python

# Top Customers
#Arranging based on household_key not SALES_VALUE


import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

products = requests.post('http://localhost:9200/_sql', data = 'SELECT SUM(SALES_VALUE) FROM transactions GROUP BY household_key ORDER BY SUM(SALES_VALUE) DESC LIMIT 160 ').json()
#print 'name, quantity, value'

N = 10
value = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
household_key_list = []

#Find top 10 household keys by spending, this you have aklready done.

{
    "SUM(SALES_VALUE)": {
      "value": 11558.11999999999
    },
    "key": "2459",
    "doc_count": 3642
  }
rank = 0
for product in products['aggregations']['household_key']['buckets']:
    household_key = product['key']
    print 'rank, household_key, value spent, Married,   Age, Home Status, Household_Size'

    values = product['SUM(SALES_VALUE)']['value']
    name_json = requests.post('http://localhost:9200/_sql', data='SELECT * FROM demographics WHERE household_key = "'+ str(household_key)+'"').json()
    if len(name_json['hits']['hits']):
        rank += 1
        name = name_json['hits']['hits'][0]['_source']

        household_key_list.append(household_key)

        print rank,'\t', household_key, '\t', '\t', values,'\t',name['MARITAL_STATUS_CODE'],'\t',name['AGE_DESC'],'\t', name['HOMEOWNER_DESC'],'\t',name['HOUSEHOLD_SIZE_DESC']
