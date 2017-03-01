from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
from elasticsearch import Elasticsearch
from django.shortcuts import render_to_response
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart


def plot(request):

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
        }
    }

    es = Elasticsearch()
    res = es.search(index="demographics", body=query_json)

    data = []

    print res
    for _count in res['aggregations']['MARITAL_STATUS_CODE']['buckets'][0]['ln']['buckets']:
        data.append([_count['key'], _count['doc_count']])

    data_source = SimpleDataSource(data= data)

    chart = BarChart(data_source)
    context = {'chart': chart}

    return render(request, 'plot.html', context)


