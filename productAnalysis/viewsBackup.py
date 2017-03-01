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
        Quarter_list = [['Category','Quarter', 'Revenue']]
        for quarter,quarter_data in eachQuarter.items():
            for prod,quant in quarter_data.iteritems():
                if quant == 0:
                    continue
                Quarter_list.append([prod,(quarter),quant])

        data = Quarter_list

        data_source = SimpleDataSource(data)

        chart = BarChart(data_source, options={'lineWidth':15, 'smooth':False})

        context['chart'+str(count)] = chart
        context['house'+str(count)] = household_key

        count = count + 1
    print Quarter_list
    return render(request, 'productAnalysis.html',context)
