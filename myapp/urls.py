from django.conf.urls import url
from .views import list, list_all, segment, about

urlpatterns = [
    url(r'^$', about, name = 'about'),
    url(r'^list/$', list, name='list'),
    url(r'^list_all/$', list_all, name='list_all'),
    url(r'^segment/$', segment, name = 'segment'),
    url(r'^about/$', about, name = 'about'),


]
