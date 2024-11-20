from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('identify/role', views.IdentifyRole.as_view(), name='identify_role'),
]
