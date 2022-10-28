"""SingdlService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from apps.admin.views.index import Index
from apps.admin.views.scheduler import Scheduler
from apps.users.views import *

app_name = 'admin'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('scheduler', Scheduler.as_view(), name='scheduler'),
    path('scheduler_single', Scheduler.scheduler_single, name='scheduler_single'),
    path('schedulers_list', Scheduler.schedulers_list, name='schedulers_list'),
    path('schedulers_delete', Scheduler.schedulers_delete,
         name='schedulers_delete'),
]
