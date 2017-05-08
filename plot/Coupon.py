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


def Coupon(request):

    coupon_redempt = requests.post(
        'http://localhost:9200/_sql', data='SELECT count(*) FROM master_data group by PRODUCT_ID, SUB_COMMODITY_DESC, COMMODITY_DESC').json()

    response = []
    RANK = 0

    for redeemed in coupon_redempt['aggregations']['PRODUCT_ID']['buckets']:
        if len(redeemed):
            RANK += 1
            for sub_buck in redeemed['SUB_COMMODITY_DESC']['buckets'][0]['COMMODITY_DESC']['buckets']:
                PRODUCT_ID = redeemed['key']
                product_times = requests.post('http://localhost:9200/_sql', data='SELECT PRODUCT_ID, COUNT(*) FROM products WHERE PRODUCT_ID= "'+ str(PRODUCT_ID) +'"  GROUP BY SUB_COMMODITY_DESC').json()
                print product_times
                PRODUCT_NAME = redeemed['SUB_COMMODITY_DESC']['buckets'][0]['key']
                PRODUCT_CATEGORY = sub_buck['key']
                TIMES_RENEWED = sub_buck['doc_count']

        response.append({
            'RANK': RANK,
            'PRODUCT_ID': PRODUCT_ID,
            'PRODUCT_NAME': PRODUCT_NAME,
            'PRODUCT_CATEGORY': PRODUCT_CATEGORY,
            'TIMES_RENEWED': TIMES_RENEWED})

    return render(request, 'Coupon.html', {'response': response})
