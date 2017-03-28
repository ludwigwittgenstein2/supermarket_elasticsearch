import requests
import json
import numpy as np
import matplotlib.pyplot as plt

products = requests.post(
    'http://localhost:9200/_sql', data='SELECT sum(SALES_VALUE) FROM transactions group by PRODUCT_ID DESC limit 10').json()

print 'name, quantity, value'

names = []
values = []

N = 10
rank = 0

for product in products['aggregations']['PRODUCT_ID']['buckets']:
    product_code = product['key']
    quantity = product['doc_count']
    value = product['SUM(SALES_VALUE)']['value']
    name_json = requests.post('http://localhost:9200/_sql',
                              data='SELECT * FROM products WHERE PRODUCT_ID = ' + str(product_code)).json()
#   print name_json
    if len(name_json['hits']['hits']):
        rank += 1
        name = name_json['hits']['hits'][0]['_source']

        names.append(name)
        values.append(value)

        print "name","Product_key", "quantity", "value", "Commodity_Name"


        print rank, '\t', product_code, '\t', '\t',value, '\t', name['SUB_COMMODITY_DESC'], name['DEPARTMENT']

"""
ind = np.arange(N)
print ind, 'np.arange(N)'
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(ind, values, width)
ax.set_xticklabels(names)
ax.set_title("Top 10 Bought Products with Revenue")

plt.show()
"""
