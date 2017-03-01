from django.conf.urls import url
from .views import productAnalysis

urlpatterns = [url(r'^$',productAnalysis, name='productAnalysis')]
