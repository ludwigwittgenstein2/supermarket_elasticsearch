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

for product in products['aggregations']['PRODUCT_ID']['buckets']:
    product_code = product['key']
    quantity = product['doc_count']
    value = product['SUM(SALES_VALUE)']['value']
    name_json = requests.post('http://localhost:9200/_sql',
                              data='select SUB_COMMODITY_DESC from products where PRODUCT_ID = ' + str(product_code)).json()
    print name_json
    name = name_json['hits']['hits'][0]['_source']['SUB_COMMODITY_DESC']

    print name, quantity, value

    names.append(name)
    values.append(value)

ind = np.arange(N)
print ind, 'np.arange(N)'
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(ind, values, width)
ax.set_xticklabels(names)
ax.set_title("Top 10 Bought Products with Revenue")

plt.show()
