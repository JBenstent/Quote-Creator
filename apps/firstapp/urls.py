from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', homerender),
    url(r'^register$', register),
    url(r'^login$', login),
]
