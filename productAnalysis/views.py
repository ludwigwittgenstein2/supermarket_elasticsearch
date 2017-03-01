from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
import yaml
import csv

# Create your views here.


def productAnalysis(request):
    context = {}
    productAnalysis = {}

    with open('/Users/Rick/Desktop/projectFinalFolder/srcCopy/plot/customerProductAnalysis.yaml', 'r') as f:
        customerProductAnalysis = yaml.load(f)
    f.close()

    count = 0
    for household_key, eachQuarter in customerProductAnalysis.items():
        productList= []
        for quarter,quarter_data in eachQuarter.items():
            for product,quant in quarter_data.iteritems():
                if product not in productList:
                    if product == ' ':
                        continue
                    productList.append(product)

    for product in productList:
        Quarter_list = [[product,'Quarter', 'Revenue']]
        for household_key, eachQuarter in customerProductAnalysis.items():
            for quarter,quarter_data in eachQuarter.items():
                for prod,quant in quarter_data.iteritems():
                    if quant == 0:
                        continue
                    if prod == ' ':
                        continue
                    else:
                        if product == prod:
                                Quarter_list.append([prod,(quarter),quant])

        data = Quarter_list

        data_source = SimpleDataSource(data)

        chart = BarChart(data_source, options={'lineWidth':15, 'smooth':False})

        context['chart'+str(count)] = chart
        context['house'+str(count)] = household_key

        count = count + 1
    print Quarter_list
    return render(request, 'productAnalysis.html',context)
