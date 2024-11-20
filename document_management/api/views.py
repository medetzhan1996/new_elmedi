import base64
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AttachedDocumentSerializer
from ..models import AttachedDocument


# Посмотреть детальную информацию направления
class AttachedDocumentListView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = AttachedDocumentSerializer
    queryset = AttachedDocument.objects.all()
    name = 'attached-document-list'
