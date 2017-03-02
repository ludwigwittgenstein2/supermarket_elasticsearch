import csv
import json
import pprint
from elasticsearch import Elasticsearch as ES
from elasticsearch import helpers
import ast

es = ES(host="localhost", port=9200)
actions = []
import csv
reader = csv.DictReader(open("/Users/Rick/Desktop/CSV/transaction_data.csv", "r"))
a = []
from datetime import datetime
c = 0
for row in reader:
    row['_index'] = 'transactions'
    row["_op_type"] = "index"
    row["_type"] =  'transactions'
    row['QUANTITY'] = float(row['QUANTITY'])
    row['SALES_VALUE'] = float(row['SALES_VALUE'])

    c += 1
    actions.append(row)
    if len(actions) == 2000:
    	print c
        print helpers.bulk(es, actions)
        actions = []
