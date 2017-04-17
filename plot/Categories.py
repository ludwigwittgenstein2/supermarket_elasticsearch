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

Low = {}
Medium = {}
High = {}
number = 1
transaction_dict = {}
product_dict = {}

def Categories(request):
    global Low
    global Medium
    global High
    global number
    response = []

    #I need Low Income, Medium Income, High Income
    demographics = requests.post('http://localhost:9200/_sql',
                             data='SELECT * FROM demographics limit 10000').json()

    transactions = requests.post('http://localhost:9200/_sql',
                             data='SELECT household_key, PRODUCT_ID FROM transactions limit 10000').json()

    product = requests.post('http://localhost:9200/_sql',
                             data='SELECT * FROM products limit 10000').json()


    for row in transactions['hits']['hits']:
        transactions_PRODUCT_ID = row['_source']['PRODUCT_ID']
        transactions_household_key = row['_source']['household_key']
        transaction_dict[transactions_household_key] = transactions_PRODUCT_ID

    for column in product['hits']['hits']:
        product_PRODUCT_ID = column['_source']['PRODUCT_ID']
        product_COMMODITY_DESC = column['_source']['COMMODITY_DESC']
        product_DEPARTMENT = column['_source']['DEPARTMENT']
        product_dict[product_PRODUCT_ID] = product_COMMODITY_DESC,product_DEPARTMENT




    for row in demographics['hits']['hits']:
        if 'Under 15K' in row['_source']['INCOME_DESC']:
            Low['Under 15K'] = number
        else:
            number += 1
        if '15-24K' in row['_source']['INCOME_DESC']:
            Low['15-24K'] = number
        else:
            number += 1
        if '75-99K' in row['_source']['INCOME_DESC']:
            Medium['75-99K'] = number
        else:
            number += 1
        if '100-124K' in row['_source']['INCOME_DESC']:
            High['100-124K'] = number
        else:
            number += 1
        if '125-149K' in row['_source']['INCOME_DESC']:
            High['125-149K'] = number
        else:
            number += 1
        if '150-174K' in row['_source']['INCOME_DESC']:
            High['150-174K'] = number
        else:
            number += 1

    print Low


    response.append({
        'Low': Low,
        'High': High,
        'Medium': Medium,
        })

    return render(request, 'Categories.html',{'response': response})
