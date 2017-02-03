from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', homerender),
    url(r'^register$', register),
    url(r'^login$', login),
    url(r'^quotes$', quotes),
    url(r'^addquotes$', addquotes),
    url(r'^logout$', logout),
    url(r'^dashboard$', dashboard),
    url(r'^favquotes/(?P<id>\d+)$', favquotes),
    url(r'^users/(?P<id>\d+)$', renderuserpage),

]
