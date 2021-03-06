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


def TopCategories(request):

    transactions = requests.post(
        'http://localhost:9200/_sql', data='SELECT COUNT(*) FROM transactions GROUP BY PRODUCT_ID').json()

    response_categories = []
    DEPARTMENT_COUNT = {}
    rank = 0
    number = 1

    for row in transactions['aggregations']['PRODUCT_ID']['buckets']:
        product_code = row['key']
        quantity = row['COUNT(*)']['value']
        name_json = requests.post('http://localhost:9200/_sql',
                                  data='SELECT * FROM products WHERE PRODUCT_ID = ' + str(product_code)).json()

        rank += 1
        name = name_json['hits']['hits'][0]['_source']
        DEPARTMENT = name['DEPARTMENT']
        data_Chart = []


        if 'GROCERY' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['GROCERY'] = number
        else:
            number += 1
        if 'KIOSK-GAS' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['KIOSK-GAS'] = number
        else:
            number += 1
        if 'DELI' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['DELI'] = number
        else:
            number += 1
        if 'MEAT-PCKGD' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['MEAT-PCKGD'] = number
        else:
            number += 1
        if 'MISC SALES TRAN' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['MISC SALES TRAN'] = number
        else:
            number += 1
        if 'PASTRY' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['PASTRY'] = number
        else:
            number += 1
        if 'DRUG GM' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['DRUG GM'] = number
        else:
            number += 1

        if 'COSMETICS' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['DRUG GM'] = number
        else:
            number += 1
        if 'NUTRITION' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['DRUG GM'] = number
        else:
            number += 1
        if 'SPIRITS' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['DRUG GM'] = number
        else:
            number += 1
        if 'SALAD BAR' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['SALAD BAR'] = number
        else:
            number += 1
        if 'GRO BAKERY' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['SALAD BAR'] = number
        else:
            number += 1
        if 'DELI/SNACK BAR' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['SALAD BAR'] = number
        else:
            number += 1
        if 'GARDEN CENTER' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['SALAD BAR'] = number
        else:
            number += 1
        if 'POSTAL CENTER' in name['DEPARTMENT']:
            DEPARTMENT_COUNT['SALAD BAR'] = number
        else:
            number += 1
        if DEPARTMENT not in name['DEPARTMENT']:
            DEPARTMENT_COUNT[DEPARTMENT] = number
        else:
            number += 1


        print DEPARTMENT_COUNT
        data_Chart = list([DEPARTMENT_COUNT])
        data_source = (SimpleDataSource(data=data_Chart))
        chart = LineChart(data_source)
        context = {'chart': chart}

        response_categories.append({
                'Categories_rank': rank,
                'Categories_PRODUCT_ID': product_code,
                'Categories_values': quantity,
                'Categories_SUB_COMMODITY_DESC': name['SUB_COMMODITY_DESC'],
                'Categories_DEPARTMENT': name['DEPARTMENT'],
                'Categories_BRAND': name['BRAND'],
                'DEPARTMENT_COUNT':context['chart'],
            })

    #print json.dumps(response)
    #print context['chart']
    return render(request, 'TopCategoriesProduct.html', {'response_categories': response_categories})
