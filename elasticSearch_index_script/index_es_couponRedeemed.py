
x = '''{
          "Application": {
            "type": "string"
          },
          "Archive": {
            "type": "boolean"
          },
          "BU": {
            "type": "string"
          },
          "Codename": {
            "type": "string"
          },
          "Complexity": {
            "type": "string"
          },
          "CurrentBOMCost": {
            "type": "double"
          },
          "CurrentFKRevPerYear": {
            "type": "double"
          }

  }
'''


import csv
import json
import pprint
from elasticsearch import Elasticsearch as ES
from elasticsearch import helpers
import ast

es = ES(host="localhost", port=9200)
actions = []
import csv
x = ast.literal_eval(x)
reader = csv.DictReader(open("/Users/Rick/Desktop/CSV/coupon_redempt.csv", "r"))
a = []
from datetime import datetime
c = 0
for row in reader:
    row['_index'] = 'coupon_redempt'
    row["_op_type"] = "index"
    row["_type"] =  'coupon_redempt'
    print c
    c += 1
    actions.append(row)
    if len(actions) == 2:
        print helpers.bulk(es, actions)
        actions = []
