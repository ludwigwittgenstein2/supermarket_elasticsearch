from django.conf.urls import url
from .views import z_score

urlpatterns = [
    url(r'^$', z_score, name='z_score')
]
