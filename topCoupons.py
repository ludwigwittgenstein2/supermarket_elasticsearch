#!/usr/bin/Python

# Top Customers
#Arranging based on household_key not SALES_VALUE


import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


coupon_json_id = []
coupon_json_product = []
product_json_id = []
rank = 0


coupon_redempt = requests.post('http://localhost:9200/_sql', data = 'SELECT COUPON_UPC, household_key FROM coupon_redempt').json()
#print 'name, quantity, value'

for coupon in coupon_redempt['hits']['hits']:
    coupon_id = coupon['_source']['COUPON_UPC']
    household_key = coupon['_source']['household_key']

    coupon_json = requests.post('http://localhost:9200/_sql', data = 'SELECT COUPON_UPC, PRODUCT_ID FROM coupon WHERE COUPON_UPC=' + str(coupon_id)).json()

    if len(coupon_json['hits']['hits']):
        print coupon_json['hits']['hits']
        rank += 1
        coupon_json_id.append(coupon_json_id['hits']['hits']['_source']['COUPON_UPC'])
        coupon_json_product.append(coupon_json_product['hits']['hits']['_source']['PRODUCT_ID'])
        print coupon_json_id

"""



    print coupon_json

    for row in coupon_json['hits']['hits']:
        coupon_json_id.append(row['_source']['COUPON_UPC'])
        coupon_json_product.append(row['_source']['PRODUCT_ID'])

        product_json = requests.post('http://localhost:9200/_sql', data = 'SELECT PRODUCT_ID, SUB_COMMODITY_DESC, DEPARTMENT FROM products').json()

        for row in product_json['hits']['hits']:
            product_json_id.append(row['_source']['PRODUCT_ID'])







#for row in product_json['hits']['hits']:
    #print row

"""
