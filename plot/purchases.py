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

def purchases(request, house_id):
    Total_SALES_VALUE = 0
    WEEK_SALES_VALUE = 0
    Weekly_trend = []
    number = {}
    data = requests.post('http://localhost:9200/_sql',
        data='SELECT * FROM transactions WHERE household_key = %s ORDER BY WEEK_NO' % (house_id)).json()

    response = []
    for hit in data['hits']['hits']:
        hit = hit['_source']
        product = requests.post('http://localhost:9200/_sql',data='SELECT * FROM products WHERE PRODUCT_ID = %s' % (hit.get('PRODUCT_ID'))).json()['hits']['hits'][0]['_source']
        hit.update(product)
        Total_SALES_VALUE += (hit.get('SALES_VALUE'))

        if hit['SUB_COMMODITY_DESC'] in product['SUB_COMMODITY_DESC']:
            number[product['SUB_COMMODITY_DESC']] = int(hit['QUANTITY'])
        else:
            number[product['SUB_COMMODITY_DESC']] += int(hit['QUANTITY'])
    Label = number.keys()
    Sizes = number.values()

    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': Label[:5], 'y': Sizes[:5]}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'



    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            },
            'chart' : True,
            }


    if hit.get('WEEK_NO') == hit.get('WEEK_NO'):
        WEEK_SALES_VALUE += hit.get('SALES_VALUE')
        Weekly_trend = ([(int(hit.get('WEEK_NO')),(WEEK_SALES_VALUE))])



    response.append({
            'QUANTITY': hit.get('QUANTITY'),
            'RETAIL_DISC': hit.get('RETAIL_DISC'),
            'SUB_COMMODITY_DESC': hit.get('SUB_COMMODITY_DESC'),
            'COMMODITY_DESC': hit.get('COMMODITY_DESC'),
            'SALES_VALUE': hit.get('SALES_VALUE'),
            'DAY': hit.get('DAY'),
            'WEEK_NO': hit.get('WEEK_NO'),
            'COUPON_MATCH_DISC': hit.get('COUPON_MATCH_DISC'),
            'COUPON_DISC': hit.get('COUPON_DISC'),
            'BASKET_ID': hit.get('BASKET_ID'),
            'STORE_ID': hit.get('STORE_ID'),
            'TOTAL_SALES': Total_SALES_VALUE

        })
    #print Total_SALES_VALUE
    return render(request, 'purchases.html', {'response': response,'charttype': charttype,
    'chartdata': chartdata,
    'chartcontainer': chartcontainer,
    'extra': {
        'x_is_date': True,
        'x_axis_format': '',
        'tag_script_js': True,
        'jquery_on_ready': True,
    },
    'chart' : True})
