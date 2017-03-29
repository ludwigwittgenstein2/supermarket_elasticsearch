import csv
import json
import pprint
from elasticsearch import Elasticsearch as ES
from elasticsearch import helpers
from datetime import datetime
import ast

es = ES(host="localhost", port=9200)
actions = []

reader = csv.DictReader(open("/Users/Rick/Desktop/CSV/product.csv", "rU"))
a = []
c = 0
for row in reader:
    row['_index'] = 'products'
    row["_op_type"] = "index"
    row["_type"] =  'product'
    print c
    c += 1
    actions.append(row)
    if len(actions) == 200:
        print helpers.bulk(es, actions)
        actions = []
