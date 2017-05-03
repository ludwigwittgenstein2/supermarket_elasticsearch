import requests
import json


def get_data_from_es(query):
    data = requests.post('http://localhost:9200/_sql', data=query).json()
    return data['hits']['hits']


def main():
    results_all = get_data_from_es('select * from coupon_redempt limit 3000')
    for result in results_all:
        result = result['_source']
        result.update(get_coupon_info(result['COUPON_UPC']))
        result.update(get_demographics(result['household_key']))
        requests.post('http://localhost:9200/master_data/all',
                      data=json.dumps(result))
        # print missed


def get_coupon_info(COUPON_UPC):

    data = get_data_from_es(
        "select * from coupon where COUPON_UPC = '%s'" % (COUPON_UPC))
    product = get_product(data[0]['_source']['PRODUCT_ID'])
    return product


def get_product(product_id):
    data = get_data_from_es(
        'select * from product where PRODUCT_ID = "%s"' % (product_id))
    return data[0]['_source']


def get_demographics(household_key):
    data = get_data_from_es(
        'select * from demographics where household_key = %s' % (household_key))
    if len(data):
        return data[0]['_source']
    else:
        # print 'household_key : ', household_key
        return {'not_found': True}

if __name__ == '__main__':
    main()
