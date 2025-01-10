from rest_framework import serializers
from .models import LoyaltyProgram, PointBalance, Transaction


class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'


class PointBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointBalance
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
