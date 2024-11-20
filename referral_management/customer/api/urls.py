from django.urls import path
from . import views

app_name = 'customer_api'

urlpatterns = [
    path('<str:search>/customer/search', views.CustomerSearch.as_view(),
         name='customer_search'),
]
