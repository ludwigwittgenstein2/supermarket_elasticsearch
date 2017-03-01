from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart

from .models import Monthly, Daily
from chartit import DataPool, Chart
from chartit import PivotDataPool, PivotChart

import simplejson
import yaml
import csv


from django.shortcuts import render_to_response
import random
import datetime
import time

#with open('/Users/Rick/Desktop/sample_demographics.csv', 'r') as w:
#    income_group = {}
#    income_group_list = []
#    next(w)
#    data = csv.reader(w, delimiter=',')
#    for row in data:
#        if row[2] not in income_group:
#            income_group[row[2]] = 1
#        else:
#            income_group[row[2]] += 1
#    for key, value in sorted(income_group.iteritems(), key=lambda(k,v):(v,k)):
#        print "%s: %s" % (key,value)
#
#    for i, k in income_group.items():
#        income_group_list.append([i,k])
#        print income_group_list

#    with open("/Users/Rick/Desktop/Project/src/media/documents/2016/08/24/transaction_data.csv", 'r') as f:
#         csv_f = list(csv.reader(f,delimiter = ','))
#         new_list = []
#         J = csv_f[0].index('SALES_VALUE')
#         K = csv_f[0].index('WEEK_NO')
#         for i in range(len(csv_f)):
#             new_list.append(csv_f[i][J])
#             new_list.append(csv_f[i][K])
#    new_list = new_list[:5]
#
# Test CSV file
#    csv_file = open('/Users/Rick/Desktop/Project/test.csv')

def z_score(request):

    customerMaritalStatusMoreOverTime_list_status = []
    customerMaritalStatusMoreOverTime_list_household = []
    customerMaritalStatusMoreOverTime_list_income = []

    with open("/Users/Rick/Desktop/projectFinalFolder/segments/customerMaritalStatusMoreOverTime.yaml") as w:
        customerMaritalStatusMoreOverTime = yaml.load(w)
    w.close()

    for row, value in customerMaritalStatusMoreOverTime.items():
        for column, data in value.items():
            customerMaritalStatusMoreOverTime_list_income.append(row)

    for row, value in customerMaritalStatusMoreOverTime.items():
        for household_key in value:
            customerMaritalStatusMoreOverTime_list_household.append(household_key)

    ydata = customerMaritalStatusMoreOverTime_list_income
    xdata = customerMaritalStatusMoreOverTime_list_household

    zdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    mdata = [5, 48, 160, 94, 75, 71, 49, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "lineChart"
    chartcontainer = 'linechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            }
            }
    return render_to_response('plot.html', data)



def sample(request):
    weatherdata = \
    customerMarital_List = []

    with open("/Users/Rick/Desktop/projectFinalFolder/segments/customerMaritalStatusMoreOverTime.yaml") as w:
        customerMaritalStatusMoreOverTime = yaml.load(w)
    w.close()

    for row in customerMaritalStatusMoreOverTime.items():
        for value in row:
            customerMarital_List.append(value)

    DataPool(series=[{'options':{
                    'source':customerMarital_List},
                    'terms': [
                    'Marital status',
                    'Household',
                    'Income']}
                    ])
    cht = Chart(
            datasource = weatherdata,
            chart_options = {'title':{'text': 'Customer Marital Status'}}
                )
    return render_to_response('none.html', {'weatherchart':cht})

def none(request):

    N = 1000
    random_x = np.random.randn(N)
    random_y = np.random.randn(N)

# Create a trace
    trace = go.Scatter(x = random_x, y = random_y, mode = 'markers')
    data = [trace]

# Plot and embed in ipython notebook!
    take_back = py.iplot(data, filename='basic-scatter')

# or plot with: plot_url = py.plot(data, filename='basic-line')

    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Monthly.objects.all()},
              'terms': [
                'month',
                'houston_temp',
                'boston_temp']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'month': [
                    'boston_temp',
                    'houston_temp']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response('plot.html', {'take_back': basic-scatter})

"""



def door(request):
    context = {}
    customerQuarterProductDict = {}
    moreOverTime = []

    with open("/Users/Rick/Desktop/projectFinalFolder/segments/customerMoreQuarterProductDictOverTime.yaml", 'r') as f:
        customerQuarterProductDict =  yaml.load(f)
    f.close()

    with open("/Users/Rick/Desktop/projectFinalFolder/segments/moreSpentOverTime.yaml", 'r') as f:
        moreOverTime =  yaml.load(f)
    f.close()

    Quarterly_list = []
    count = 0

    for houseKey in moreOverTime:
        for houseHoldKey, quarterDict in customerQuarterProductDict.items():
                if houseKey == houseHoldKey:
                    Quarterly_list = [['Category', 'Sale_value']]
                    for quarterNo, categoryDict in quarterDict.items():
                        for item, saleValue in categoryDict.items():
                            if item == "GROCERY" :
                                Quarterly_list.append([str(quarterNo), saleValue])
                    data = Quarterly_list
                    data_source = SimpleDataSource(data)
                    chart = BarChart(data_source, height=500, width=500, options={'title': 'Quarterly_list'})
                    context['chart'+str(count)] = chart
                    context['house'+str(count)]= houseHoldKey
                    count = count+ 1
    print data
    print "This is Printing"
    return render(request, 'plot.html', context)



def z_score(request):
    '''   data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]'''
    context = {}
    customerQuarterSalesDict = {}
    customerQuarterSalesList = []

    with open('/Users/Rick/Desktop/segments/customerQuarterSalesDict.yaml', 'r' ) as f:
        customerQuarterSalesDict =  yaml.load(f)
    f.close()

    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'r' ) as f:
        topHouseHoldList =  yaml.load(f)
    f.close()


    count = 0
    for houseHoldKey, weekDict in customerQuarterSalesDict.items():
        if houseHoldKey in topHouseHoldList:
            customerQuarterSalesList = [['week_no','sales-value']]
            for weekNo,zscoreValue in sorted(weekDict.items(), key=lambda k:k[0]):
                customerQuarterSalesList.append([weekNo,zscoreValue])
                print customerQuarterSalesList

            data = customerQuarterSalesList
                    # DataSource object
            #dataSource = SimpleDataSource(data)
                    # Chart object
            data_source = SimpleDataSource(data)

            chart = LineChart(data_source, height=500, width=500, options={'title': 'Z scores'})
            #chart = LineChart(dataSource)
            context['chart'+str(count)] = chart
            context['house'+str(count)]= houseHoldKey
            count = count+ 1

    return render(request, 'plot.html', context)
"""

# Create your views here.
