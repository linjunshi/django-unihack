"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

import api.views as apiview

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='register'),
    
    # RESTFUL
    
    # # store token
    # url(r'api/storeToken'),
    
    # get car park info by id
    url(r'api/getCarPark/([0-9]*)', apiview.get_carpark),
    
    # get all records
    url(r'^api/allRecord', apiview.get_all_records),
    
    # get record by id
    url(r'^api/getRecord/([0-9]*)', apiview.get_car),
    
    # create a new record using plate number
    url(r'^api/parking/start', apiview.car_start_parking),
    
    # inform the server the car has leaved the parking lot
    url(r'^api/parking/leave', apiview.car_leave),
    
    # pay the order
    url(r'^api/parking/payOrder/', apiview.pay_order)

]

urlpatterns = format_suffix_patterns(urlpatterns)
