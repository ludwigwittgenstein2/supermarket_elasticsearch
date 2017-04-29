from django.conf.urls import url
from .Coupon import Coupon
from .TopProducts import TopProducts
from .TopConsumers import TopConsumers
from .married import married
from .Supermarket_trend import Supermarket_trend
from .plot import plot
from .purchases import purchases
from .Categories import Categories
from .TopCategories import TopCategories
from .CouponDetails import CouponDetails
from .D3 import D3
from .TopDepartment import TopDepartment


urlpatterns = [
    #url(r'^([0-9]\d+^$', plot, name='plot')
     url(r'^$', plot, name='plot'),
     url(r'^married$', married, name= 'married'),
     url(r'^TopConsumers$', TopConsumers, name= 'TopConsumers'),
     url(r'^TopProducts$', TopProducts, name= 'TopProducts'),
     url(r'^Coupon$', Coupon, name= 'Coupon'),
     url(r'^consumers/(?P<house_id>\d+)', purchases, name= 'purchases'),
     url(r'^trend$', Supermarket_trend, name= 'Supermarket_trend'),
      url(r'^TopCategories$', TopCategories, name= 'TopCategories'),
     url(r'^Categories$', Categories, name= 'Categories'),
      url(r'^TopDepartment$', TopDepartment, name= 'TopDepartment'),
     url(r'^CouponDetails$',CouponDetails, name='CouponDetails'),
      url(r'^D3$', D3, name= 'D3')
]
