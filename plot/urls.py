from django.conf.urls import url
from .views import plot, married,TopConsumers, TopProducts, Coupon,purchases, Supermarket_trend

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
