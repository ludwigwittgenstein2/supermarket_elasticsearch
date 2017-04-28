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


def CouponDetails(request):

    coupon_redempt = requests.post(
        'http://localhost:9200/_sql', data='SELECT * FROM master_data ORDER BY DAY').json()

    response = []
    RANK = 0

    for redeemed in coupon_redempt['hits']['hits']:
        if len(redeemed):
            RANK += 1
            COUPON_UPC = redeemed['_source']['COUPON_UPC']
            CURR_SIZE_OF_PRODUCT = redeemed['_source']['CURR_SIZE_OF_PRODUCT']
            BRAND = redeemed['_source']['BRAND']
            household_key = redeemed['_source']['household_key']
            PRODUCT_ID = redeemed['_source']['PRODUCT_ID']
            COMMODITY_DESC = redeemed['_source']['COMMODITY_DESC']
            SUB_COMMODITY_DESC = redeemed['_source']['SUB_COMMODITY_DESC']
            DAY = redeemed['_source']['DAY']
            try:
                redeemed['_source']['HH_COMP_DESC']
                MARITAL_STATUS_CODE = redeemed['_source']['MARITAL_STATUS_CODE']
                INCOME_DESC = redeemed['_source']['INCOME_DESC']
                AGE_DESC  = redeemed['_source']['AGE_DESC']
                HOMEOWNER_DESC = redeemed['_source']['HOMEOWNER_DESC']
            except KeyError:
                pass
            else:
                HH_COMP_DESC = redeemed['_source']['HH_COMP_DESC']
                MARITAL_STATUS_CODE = redeemed['_source']['MARITAL_STATUS_CODE']
                INCOME_DESC = redeemed['_source']['INCOME_DESC']
                AGE_DESC  = redeemed['_source']['AGE_DESC']
                HOMEOWNER_DESC = redeemed['_source']['HOMEOWNER_DESC']


            response.append({
            'RANK': RANK,
            'COUPON_UPC': COUPON_UPC,
            'CURR_SIZE_OF_PRODUCT': CURR_SIZE_OF_PRODUCT,
            'BRAND': BRAND,
            'household_key':household_key,
            'PRODUCT_ID':PRODUCT_ID,
            'AGE_DESC':AGE_DESC,
            'HOMEOWNER_DESC':HOMEOWNER_DESC,
            'COMMODITY_DESC':COMMODITY_DESC,
            'SUB_COMMODITY_DESC':SUB_COMMODITY_DESC,
            'MARITAL_STATUS_CODE':MARITAL_STATUS_CODE,
            'HH_COMP_DESC':HH_COMP_DESC,
            'INCOME_DESC':INCOME_DESC,
            'DAY':DAY
            })

    return render(request, 'CouponDetails.html', {'response': response})
