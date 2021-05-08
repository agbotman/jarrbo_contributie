from django.conf.urls import url
from .views import *

app_name = 'jarrbo_contributie'
urlpatterns = [
    url(r'^import/$', ImportLedenView.as_view(), name='import'),
]
