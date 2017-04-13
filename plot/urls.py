from django.conf.urls import url
from .Coupon import Coupon
from .TopProducts import TopProducts
from .TopConsumers import TopConsumers
from .married import married
from .Supermarket_trend import Supermarket_trend
from .plot import plot
from .purchases import purchases


urlpatterns = [
    #url(r'^([0-9]\d+^$', plot, name='plot')
     url(r'^$', plot, name='plot'),
     url(r'^married$', married, name= 'married'),
     url(r'^TopConsumers$', TopConsumers, name= 'TopConsumers'),
     url(r'^TopProducts$', TopProducts, name= 'TopProducts'),
     url(r'^Coupon$', Coupon, name= 'Coupon'),
     url(r'^consumers/(?P<house_id>\d+)', purchases, name= 'purchases'),
     url(r'^trend$', Supermarket_trend, name= 'Supermarket_trend')
]
