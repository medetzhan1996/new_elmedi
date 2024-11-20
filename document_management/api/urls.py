from django.urls import path
from . import views

app_name = 'document_management_api'

urlpatterns = [
    path('attached/document/', views.AttachedDocumentListView.as_view(), name='attached-document-list'),
]
