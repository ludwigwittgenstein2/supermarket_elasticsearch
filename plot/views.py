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


import pylab
import json
import requests


def plot(request):

    print "Hello"

    query_json = {
        "aggregations": {
            "MARITAL_STATUS_CODE": {
                "terms": {
                    "field": "MARITAL_STATUS_CODE",
                    "size": 0
                },
                "aggregations": {
                    "ln": {
                        "terms": {
                            "field": "INCOME_DESC",
                            "size": 0
                        }
                    }
                }
            }
        }}

    print query_json

    es = Elasticsearch(host='localhost', port=9200)
    res = es.search(index="demographics", body=json.dumps(query_json))
#    res = requests.post('http://localhost:9200/demographics/_search',data=json.dumps(query_json)).text
#    res = json.loads(res)
    print res

    data = []

    for _count in res['aggregations']['MARITAL_STATUS_CODE']['buckets'][0]['ln']['buckets']:
        data.append([_count['key'], _count['doc_count']])

    data_source = SimpleDataSource(data=data)
    print data_source

    chart = BarChart(data_source)
    context = {'chart': chart}

    print context

    return render(request, 'IncomeRange.html', context)


def married(request):

    result = requests.post('http://localhost:9200/_sql',
                           data='SELECT * FROM demographics group by MARITAL_STATUS_CODE, AGE_DESC').text

    result = json.loads(result)

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    c = {
        'u': 'r',  # unknown
        'a': 'b',  # single
        'b': 'g'  # Married
    }

    m = {
        'u': 0,
        'a': 1,
        'b': 2}

    for bucket in result['aggregations']['MARITAL_STATUS_CODE']['buckets']:
        marrige = bucket['key']
        age_list = []
        count_list = []
        for sub_bucket in bucket['AGE_DESC']['buckets']:
            age = sub_bucket['key']
            print bucket['key']
            peoples = requests.post('http://localhost:9200/_sql',
                                    data='SELECT household_key FROM demographics where AGE_DESC="{age}" and MARITAL_STATUS_CODE="{marrige}"'.format(age=age, marrige=marrige)).text

            people_list = []
            peoples = json.loads(peoples)
            for people in peoples['hits']['hits']:
                # print 'people'
                people_list.append(people['_source']['household_key'])

            # print people_list
            count = requests.post('http://localhost:9200/_sql',
                                  data='SELECT count(*) FROM transactions where  household_key in ("{lsit}")'.format(lsit='","'.join(people_list))).text

            count = json.loads(count)['aggregations']['COUNT(*)']['value']

            print marrige, age, count
            age_list.append(int(age))
            count_list.append(int(count))

        ax.bar(np.array(age_list), np.array(
            count_list), m[marrige], color=c[marrige])

    ax.set_xlabel('Age')
    ax.set_ylabel('Count')
    ax.set_zlabel('Married')
    ax.set_title(
        ' Married people with being owner ( X : Income segment , Y : age , Z : Number of visits  )')

    # plt.show()

    response = HttpResponse(content_type="image/png")
    # create your image as usual, e.g. pylab.plot(...)
    pylab.savefig(response, format="png")

    return response


def TopConsumers(request):

    products = requests.post('http://localhost:9200/_sql',
                             data='SELECT SUM(SALES_VALUE) FROM transactions GROUP BY household_key ORDER BY SUM(SALES_VALUE) DESC LIMIT 50 ').json()
    # print 'name, quantity, value'
    response = []
    rank = 0
    for product in products['aggregations']['household_key']['buckets']:
        household_key = product['key']

        values = product['SUM(SALES_VALUE)']['value']
        name_json = requests.post('http://localhost:9200/_sql',
                                  data='SELECT * FROM demographics WHERE household_key = "' + str(household_key) + '"').json()
        if len(name_json['hits']['hits']):
            rank += 1
            name = name_json['hits']['hits'][0]['_source']

            trend = requests.post('http://localhost:9200/_sql', data='SELECT COUNT(*) FROM transactions WHERE household_key =  "'+ str(household_key) +'" GROUP BY WEEK_NO ORDER BY WEEK_NO').json()
            trend_weekly = trend['aggregations']
            data_Trend = []
            for week in trend_weekly['WEEK_NO']['buckets']:
                week_no = week['key']
                times_visited = week['COUNT(*)']['value']
                data_Trend.append([int(week_no), times_visited])
            print data_Trend

            data_source = (SimpleDataSource(data=data_Trend))

            chart = LineChart(data_source, height= 190, width=550, labels=['Week', 'Number'])
            context = {'chart': chart}
            print context['chart']

            response.append({
                'rank': rank,
                'household_key': household_key,
                'values': values,
                'married': name['MARITAL_STATUS_CODE'],
                'age': name['AGE_DESC'],
                'home': name['HOMEOWNER_DESC'],
                'size': name['HOUSEHOLD_SIZE_DESC'],
                'trend': context['chart']})

    #print json.dumps(response)
    return render(request, 'TopConsumers.html', {'response': response})


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
            rank += 1
            a = 0
            name = name_json['hits']['hits'][0]['_source']
            if name['SUB_COMMODITY_DESC'] == name['SUB_COMMODITY_DESC']:
                print name['SUB_COMMODITY_DESC']



            response.append({
                'rank': rank,
                'PRODUCT_ID': product_code,
                'values': value,
                'SUB_COMMODITY_DESC': name['SUB_COMMODITY_DESC'],
                'DEPARTMENT': name['DEPARTMENT'],
                'BRAND': name['BRAND'],
            })

    #print json.dumps(response)
    return render(request, 'TopProducts.html', {'response': response})


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


def purchases(request, house_id):
    Total_SALES_VALUE = 0
    data = requests.post(
        'http://localhost:9200/_sql',
        data='select * from transactions where household_key = %s limit 10000' % (house_id)).json()

    response = []
    for hit in data['hits']['hits']:
        hit = hit['_source']
        product = requests.post(
            'http://localhost:9200/_sql',
            data='select * from products where PRODUCT_ID = %s' % (hit.get('PRODUCT_ID'))
            ).json()['hits']['hits'][0]['_source']
        hit.update(product)

        Total_SALES_VALUE += (hit.get('SALES_VALUE'))

        category_trend = [hit.get('COMMODITY_DESC')]



        response.append({
            'QUANTITY': hit.get('QUANTITY'),
            'RETAIL_DISC': hit.get('RETAIL_DISC'),
            'SUB_COMMODITY_DESC': hit.get('SUB_COMMODITY_DESC'),
            'COMMODITY_DESC': hit.get('COMMODITY_DESC'),
            'SALES_VALUE': hit.get('SALES_VALUE'),
            'DAY': hit.get('DAY'),
            'COUPON_MATCH_DISC': hit.get('COUPON_MATCH_DISC'),
            'COUPON_DISC': hit.get('COUPON_DISC'),
            'BASKET_ID': hit.get('BASKET_ID'),
            'STORE_ID': hit.get('STORE_ID'),
            'TOTAL_SALES': Total_SALES_VALUE
        })
    #print Total_SALES_VALUE
    return render(request, 'purchases.html', {'response': response})

def Supermarket_trend(request):

    return render(request, 'SupermarketTrend.html')
