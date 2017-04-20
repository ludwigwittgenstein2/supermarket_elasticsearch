"""Segmentation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

urlpatterns = [
    url(r'^$',include('myapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^plot/', include('plot.urls')),
    url(r'^z_score/', include('z_score.urls')),
    url(r'^myapp/', include('myapp.urls')),
    url(r'^productAnalysis/',include('productAnalysis.urls')),

    #url(r'^$', RedirectView.as_view(url='/myapp/list/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
