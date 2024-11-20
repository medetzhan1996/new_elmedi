from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ReferralSerializer
from ..models import Referral


class ReferralMixin:
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = ReferralSerializer
    queryset = Referral.objects.all()


# Посмотреть список направлении
class ReferralCreateView(ReferralMixin, generics.CreateAPIView):
    name = 'referral-create'


# Посмотреть детальную информацию направления
class ReferralDetail(ReferralMixin, generics.RetrieveUpdateDestroyAPIView):
    name = 'referral-detail'


class ReferralsByIin(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ReferralSerializer
    name = 'referral-by_iin'

    def get_queryset(self):
        iin = self.kwargs.get("iin")
        return Referral.objects.filter(customer__iin=iin).all()
