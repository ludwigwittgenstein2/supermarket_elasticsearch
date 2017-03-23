from django.conf.urls import url
from .views import plot

urlpatterns = [
    url(r'^$', plot, name='plot')
]
