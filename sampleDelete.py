import pylab
import json
import requests
import matplotlib.pyplot as plt





Total_SALES_VALUE = 0
WEEK_SALES_VALUE = 0
Weekly_trend = []
data = requests.post('http://localhost:9200/_sql',
      data='SELECT * FROM transactions WHERE household_key = %s ORDER BY WEEK_NO limit 10' % (2322)).json()

#print json.dumps(data)

response = []

count = 0
number = {}
for hit in data['hits']['hits']:
    hit = hit['_source']
    product = requests.post('http://localhost:9200/_sql', data='SELECT * FROM products WHERE PRODUCT_ID = %s'%(hit.get('PRODUCT_ID'))).json()['hits']['hits'][0]['_source']
    hit.update(product)

    if hit['SUB_COMMODITY_DESC'] in product['SUB_COMMODITY_DESC']:
        number[product['SUB_COMMODITY_DESC']] = int(hit['QUANTITY'])
    else:
        number[product['SUB_COMMODITY_DESC']] += int(hit['QUANTITY'])

Label = number.keys()
Sizes = number.values()


labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(Sizes, labels=Label, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()



"""

  response = []
  for hit in data['hits']['hits']:
      hit = hit['_source']
      product = requests.post(
          'http://localhost:9200/_sql',
          data='SELECT * FROM products WHERE PRODUCT_ID = %s' % (hit.get('PRODUCT_ID'))
          ).json()['hits']['hits'][0]['_source']
      hit.update(product)

      Total_SALES_VALUE += (hit.get('SALES_VALUE'))


      if hit.get('WEEK_NO') == hit.get('WEEK_NO'):
          WEEK_SALES_VALUE += hit.get('SALES_VALUE')
          Weekly_trend = ([(int(hit.get('WEEK_NO')),(WEEK_SALES_VALUE))])
      print Weekly_trend

      data_source = SimpleDataSource(data=Weekly_trend)

      chart = LineChart(data_source, height= 190, width=550, labels=['Week', 'Number'])
      context = {'chart': chart}
      print context['chart']

"""
