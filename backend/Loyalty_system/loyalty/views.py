from rest_framework import viewsets
from .models import LoyaltyProgram, PointBalance, Transaction
from .serializers import LoyaltyProgramSerializer, PointBalanceSerializer, TransactionSerializer


class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer


class PointBalanceViewSet(viewsets.ModelViewSet):
    queryset = PointBalance.objects.all()
    serializer_class = PointBalanceSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
