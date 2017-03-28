from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from django.http import HttpResponse
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
from elasticsearch import Elasticsearch
from django.shortcuts import render
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
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
                             data='SELECT SUM(SALES_VALUE) FROM transactions GROUP BY household_key ORDER BY SUM(SALES_VALUE) DESC LIMIT 100 ').json()
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

            response.append({
                'rank': rank,
                'household_key': household_key,
                'values': values,
                'married': name['MARITAL_STATUS_CODE'],
                'age': name['AGE_DESC'],
                'home': name['HOMEOWNER_DESC'],
                'size': name['HOUSEHOLD_SIZE_DESC']})

    print json.dumps(response)
    return render(request, 'TopConsumers.html', {'response':response})
