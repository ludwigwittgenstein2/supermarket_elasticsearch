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
    ax.set_title(' Married people with being owner ( X : Income segment , Y : age , Z : Number of visits  )')

    # plt.show()

    response = HttpResponse(content_type="image/png")
    # create your image as usual, e.g. pylab.plot(...)
    pylab.savefig(response, format="png")

    return response
