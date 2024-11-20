from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('customer/create', views.CustomerCreateView.as_view(),
         name='customer_create'),
]
