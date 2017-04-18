import csv
import json
import pprint
from elasticsearch import Elasticsearch as ES
from elasticsearch import helpers
from datetime import datetime
import ast
import csv

es = ES(host="localhost", port=9200)
actions = []

reader = csv.DictReader(open("/Users/Rick/Desktop/Education.csv", "r"))
a = []
c = 0
for row in reader:
    row['_index'] = 'education'
    row["_op_type"] = "index"
    row["_type"] =  'education'
    print c
    c += 1
    actions.append(row)
    if len(actions) == 200:
        print helpers.bulk(es, actions)
        actions = []
