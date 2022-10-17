from django.urls import path
from apps.website.views import *

app_name = 'website'

urlpatterns = [
    path('', index, name='index'),
]
