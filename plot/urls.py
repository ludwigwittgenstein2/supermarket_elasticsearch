from django.conf.urls import url
from .views import plot_income

urlpatterns = [
    url(r'^income$', plot_income, name='plot_income')
]
