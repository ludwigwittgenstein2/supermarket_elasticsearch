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

"""
Demographics:
"_index": "demographics"}, {"_score": 1.0, "_type": "demographic", "_id":
"AVqa6qnXlYC2q1-xgxks", "_source": {"MARITAL_STATUS_CODE": "B", "AGE_DESC": "45-54",
"HOMEOWNER_DESC": "Homeowner", "KID_CATEGORY_DESC": "None/Unknown",
 "HOUSEHOLD_SIZE_DESC": "1",
 "household_key": "2453", "HH_COMP_DESC": "Single Female", "INCOME_DESC": "50-74K"},
"_index": "demographics"}], "total": 800, "max_score": 1.0}

Transactions:
{u'PRODUCT_ID': u'871756', u'household_key': u'647'}, u'_index': u'transactions'},
{u'_score': 1.0, u'_type': u'transactions', u'_id': u'AVqa4TXHlYC2q1-xdBLS', u'_source':
{u'PRODUCT_ID': u'910032', u'household_key': u'647'}, u'_index': u'transactions'},
 {u'_score': 1.0, u'_type': u'transactions', u'_id': u'AVqa4TXHlYC2q1-xdBLV', u'_source':
  {u'PRODUCT_ID': u'930283', u'household_key': u'647'}, u'_index': u'transactions'},
  {u'_score': 1.0, u'_type': u'transactions', u'_id': u'AVqa4TXHlYC2q1-xdBLY',
  u'_source': {u'PRODUCT_ID': u'945998', u'household_key': u'647'},
  u'_index': u'transactions'}],

 Products:

  {u'_score': 1.0, u'_type': u'product', u'_id': u'AVqa-THslYC2q1-xhAE_', u'_source':
  {u'CURR_SIZE_OF_PRODUCT': u'7.4OZ', u'PRODUCT_ID': u'6981856', u'BRAND': u'Private',
  u'SUB_COMMODITY_DESC': u'GRANOLA BARS', u'COMMODITY_DESC':
  u'CONVENIENT BRKFST/WHLSM SNACKS', u'DEPARTMENT': u'GROCERY', u'MANUFACTURER': u'69'},
  u'_index': u'products'}], u'total': 92200, u'max_score': 1.0},
  u'_shards': {u'successful': 5, u'failed': 0, u'total': 5},
   u'took': 125, u'timed_out': False}



Categories
{Meat: Low:2000, Medium:1000, High: 3000}

"""

Low = {}
Medium = {}
High = {}
number = 1
transaction_dict = {}
demographics_dict={}
product_dict = {}




def Categories(request):
    global Low
    global Medium
    global High
    global number
    All_dict = {}
    response = []
    count = 1
    count_product = {}
    All_dict_2 = {}
    All_dict_3 = {}
    All_dict_4 = {}

    #I need Low Income, Medium Income, High Income
    demographics = requests.post('http://localhost:9200/_sql',
                             data='SELECT * FROM demographics limit 10000').json()


    transactions = requests.post('http://localhost:9200/_sql',
                             data='SELECT household_key, PRODUCT_ID FROM transactions limit 10000').json()

    product = requests.post('http://localhost:9200/_sql',
                             data='SELECT * FROM products limit 10000').json()


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


    for column in product['hits']['hits']:
        product_PRODUCT_ID = column['_source']['PRODUCT_ID']
        product_COMMODITY_DESC = column['_source']['COMMODITY_DESC']
        product_DEPARTMENT = column['_source']['DEPARTMENT']
        product_dict[product_PRODUCT_ID] = product_DEPARTMENT

    for row in demographics['hits']['hits']:
        demographics_household_key = row['_source']['household_key']
        demographics_income = row['_source']['INCOME_DESC']
        demographics_dict[demographics_household_key] = demographics_income

    for row in transactions['hits']['hits']:
        transactions_PRODUCT_ID = row['_source']['PRODUCT_ID']
        transactions_household_key = row['_source']['household_key']
        transaction_dict[transactions_household_key] = transactions_PRODUCT_ID

    """for column in product['hits']['hits']:
        if product_COMMODITY_DESC not in All_dict:
            All_dict[product_COMMODITY_DESC] = 1
        else:
            All_dict[product_COMMODITY_DESC] += 1
            """


    for key in transaction_dict.keys():
        #Selecting Household_key, transaction_dict.keys = Household_key
        if key in demographics_dict:
            #If Household_key in demographics[Household_key]
            All_dict[key] = transaction_dict[key]
            #All_dict[Household_key] = product_id

    for row in All_dict.values():
        #unpack dictionary and get product_id
        if row in product_dict.keys():
            #if product_id is in product_id['25325']
            All_dict_2[row] = product_dict[row]
            #Store All_dict_2[product_id] = COMMODITY_DESC



    for new in transaction_dict.values():
        # PRODUCT_ID in ALL_dict[PRODUCT_ID]
        if new in All_dict_2.keys():
            All_dict_3[new] = 1

#--Categories (PRODUCT_ID, SUB_COMMODITY_DESC)
    productValue = {}
    demographicsValue = {}
    result = []
    answer = {}
    resultTwo = []
    answerTwo = {}
    value = 0
    productID = {}
    productKey = {}

    for key, value in transaction_dict.items():
        productValue = [value]
        demographicsValue = [key]
        result = str(productValue) + "," + str(demographicsValue)
        if result in answer.keys():
            value = answer[result] + 1
            answer[result] = value
        else:
            answer[result] = 1

    for row, column in product_dict.items():
        productID = [column]
        productKey = [row]
        resultProduct = str(productID) + "," + str(productKey)
        if resultProduct in answerTwo.keys():
            value = answerTwo[resultProduct] + 1
            answerTwo[resultProduct] = column
        else:
            answerTwo[resultProduct] = 1
    print answerTwo


    for key,value in answer.items():
        #we need to split the key into productValue and demographicsValue
        #using ',' as the delimeter
        productValue = key.split()
        demographicsValue = key.split()
        #print demographicsValue, value



#-- transactions (PRODUCT_ID, Key)
#-- demographics -- (count) (INCOME_DESC)
#-- {Meat: Low:2000, Medium:1000, High: 3000}

    if product_DEPARTMENT not in count_product:
        count_product[product_DEPARTMENT] = 1
    else:
        count_product[product_DEPARTMENT] += 1




    response.append({
        'Low': Low,
        'High': High,
        'Medium': Medium,
        })

    return render(request, 'Categories.html')
