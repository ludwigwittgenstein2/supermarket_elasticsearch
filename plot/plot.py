from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from django.http import HttpResponse
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
from graphos.renderers.morris import LineChart
from graphos.renderers.morris import AreaChart
from graphos.renderers.morris import DonutChart
from elasticsearch import Elasticsearch
from django.shortcuts import render
from graphos.sources.simple import SimpleDataSource
import matplotlib.pyplot as plt

import pylab
import json
import requests

def plot(request):

    print "Hello"

    query_json = {
        "aggregations": {
            "MARITAL_STATUS_CODE": {
                "terms": {
                    "field": "MARITAL_STATUS_CODE",
                    "size": 0
                },
                "aggregations": {
                    "ln": {
                        "terms": {
                            "field": "INCOME_DESC",
                            "size": 0
                        }
                    }
                }
            }
        }}

    print query_json

    es = Elasticsearch(host='localhost', port=9200)
    res = es.search(index="demographics", body=json.dumps(query_json))
#    res = requests.post('http://localhost:9200/demographics/_search',data=json.dumps(query_json)).text
#    res = json.loads(res)
    print res

    data = []

    for _count in res['aggregations']['MARITAL_STATUS_CODE']['buckets'][0]['ln']['buckets']:
        data.append([_count['key'], _count['doc_count']])

    data_source = SimpleDataSource(data=data)
    print data_source

    chart = BarChart(data_source)
    context = {'chart': chart}

    print context

    return render(request, 'IncomeRange.html', context)
