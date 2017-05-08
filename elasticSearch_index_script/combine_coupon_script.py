from elasticsearch import Elasticsearch
import requests
import json
import time


def get_data_from_es(query):
    data = requests.post('http://localhost:9200/_sql', data=query).json()
    if 'hits' not in data:
        print data
    if 'hits' in data['hits']:
        #print data['hits'].keys()
        return data['hits']['hits']
    else:
        print data
        print query
        time.sleep(20)

def main():
    results_all = get_data_from_es('SELECT * FROM coupon_redempt LIMIT 3000')
    for result in results_all:
        result = result['_source']
        result.update(get_coupon_info(result['COUPON_UPC']))
        result.update(get_demographics(result['household_key']))
        requests.post('http://localhost:9200/master_data_new/all',
                      data=json.dumps(result))
        # print missed

def get_coupon_info(COUPON_UPC):

    data = get_data_from_es(
        "SELECT * FROM coupon WHERE COUPON_UPC = '%s'" % (COUPON_UPC))
    product = get_product(data[0]['_source']['PRODUCT_ID'])
    return product


def get_product(PRODUCT_ID):
    data = get_data_from_es(
        'SELECT * FROM products WHERE PRODUCT_ID = "%s"' % (PRODUCT_ID))
    return data[0]['_source']


def get_demographics(household_key):
    data = get_data_from_es(
        'SELECT * FROM demographics WHERE household_key = %s' % (household_key))
    if len(data):
        return data[0]['_source']
    else:
        # print 'household_key : ', household_key
        return {'not_found': True}

if __name__ == '__main__':
    main()
