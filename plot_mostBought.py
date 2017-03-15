#!/usr/bin/Python
"""
 Plot most bought product
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import requests
import json

import matplotlib.patches as patches
import matplotlib.path as path

result = requests.post('http://localhost:9200/_sql',
                       data='SELECT SUM(SALES_VALUE) FROM transactions GROUP BY PRODUCT_ID LIMIT 50').text

N = 51
width = 0.35
fig, ax = plt.subplots()

result = json.loads(result)
ind = np.arange(N)
print result
# Product_ID, SALES_VALUE

"""
for bucket in result['aggregations']['MARITAL_STATUS_CODE']['buckets']:
    marrige = bucket['key']
    age_list = []
    count_list = []
    for sub_bucket in bucket['AGE_DESC']['buckets']:
        age = sub_bucket['key']
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
        print count

        age_list.append(int(age))
        count_list.append(int(count))

    ax.bar(np.array(age_list), np.array(
        count_list), m[marrige], color=c[marrige])


ax.set_xlabel('Age')
ax.set_ylabel('Count')
ax.set_zlabel('Married')
ax.set_title(' Married people  being owner ( X : Income segment , Y : age , Z :  of visits  )')

#plt.show()
"""
