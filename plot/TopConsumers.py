from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from django.http import HttpResponse
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
from graphos.renderers.morris import LineChart
from graphos.renderers.morris import AreaChart
from elasticsearch import Elasticsearch
from django.shortcuts import render
from graphos.sources.simple import SimpleDataSource
import matplotlib.pyplot as plt

import pylab
import json
import requests

household_total_visit = []


def TopConsumers(request):
    number_times = 0
    quantity_times = {}
    total_visits = {}

    products = requests.post('http://localhost:9200/_sql',
                             data='SELECT SUM(SALES_VALUE) FROM transactions GROUP BY household_key ORDER BY SUM(SALES_VALUE) DESC LIMIT 250 ').json()
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
            data_Trend = [('WEEK_NO','Visits')]

            for week in trend_weekly['WEEK_NO']['buckets']:
                week_no = week['key']
                times_visited = week['COUNT(*)']['value']
                data_Trend.append([int(week_no), times_visited])
                quantity_times = [household_key, week_no, times_visited]
                if quantity_times[0] not in total_visits:
                    total_visits[quantity_times[0]] = quantity_times[2]
                else:
                    total_visits[quantity_times[0]] += quantity_times[2]





            data_source = (SimpleDataSource(data=data_Trend))

            chart = LineChart(data_source, height= 190, width=560, labels=['Week Number', 'Number of Visits'])

            context = {'chart': chart}

            L = (name['INCOME_DESC'])
            n = ''.join(i for i in L if i.isdigit())

            response.append({
                'rank': rank,
                'household_key': household_key,
                'values': values,
                'married': name['MARITAL_STATUS_CODE'],
                'Income': name['INCOME_DESC'],
                'age': name['AGE_DESC'],
                'home': name['HOMEOWNER_DESC'],
                'size': name['HOUSEHOLD_SIZE_DESC'],
                'Visits': total_visits[quantity_times[0]],
                'trend': context['chart']})



    print total_visits
    return render(request, 'TopConsumers.html', {'response': response})
