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


def TopProducts(request):

    products = requests.post(
        'http://localhost:9200/_sql', data='SELECT sum(SALES_VALUE) FROM transactions group by PRODUCT_ID ORDER BY SUM(SALES_VALUE) DESC limit 100').json()

    response = []
    rank = 0

    for product in products['aggregations']['PRODUCT_ID']['buckets']:
        product_code = product['key']
        quantity = product['doc_count']
        value = product['SUM(SALES_VALUE)']['value']
        name_json = requests.post('http://localhost:9200/_sql',
                                  data='SELECT * FROM products WHERE PRODUCT_ID = ' + str(product_code)).json()
    #   print name_json
        if len(name_json['hits']['hits']):
            a = 0
            name = name_json['hits']['hits'][0]['_source']
            CURR_SIZE_OF_PRODUCT = name['CURR_SIZE_OF_PRODUCT']
            if name['SUB_COMMODITY_DESC'] == name['SUB_COMMODITY_DESC']:
                print name['SUB_COMMODITY_DESC']

            response.append({
                'PRODUCT_ID': product_code,
                'PRODUCT_SIZE': CURR_SIZE_OF_PRODUCT,
                'values': value,
                'SUB_COMMODITY_DESC': name['SUB_COMMODITY_DESC'],
                'DEPARTMENT': name['DEPARTMENT'],
                'BRAND': name['BRAND'],
            })

    final = []
    done = []
    for r in response:
        if not r['SUB_COMMODITY_DESC'] in done:
            rank += 1
            r['rank'] = rank
            final.append(r)
            done.append(r['SUB_COMMODITY_DESC'])
        else:
            for _r in final:
                if _r['SUB_COMMODITY_DESC'] == r['SUB_COMMODITY_DESC']:
                    _r['values'] += r['values']
    return render(request, 'TopProducts.html', {'response': final })
