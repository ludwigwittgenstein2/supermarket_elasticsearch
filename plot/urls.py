from django.conf.urls import url
from .views import plot, married,TopConsumers, TopProducts

urlpatterns = [
    #url(r'^([0-9]\d+^$', plot, name='plot')
     url(r'^$', plot, name='plot'),
     url(r'^married$', married, name= 'married'),
     url(r'^TopConsumers$', TopConsumers, name= 'TopConsumers'),
     url(r'^TopProducts$', TopProducts, name= 'TopProducts')

]
