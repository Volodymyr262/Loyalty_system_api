from rest_framework import serializers
from .models import LoyaltyProgram, PointBalance, Transaction, LoyaltyTier


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


class LoyaltyTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTier
        fields = '__all__'

    def validate_points_to_reach(self, value):
        if value <= 0:
            raise serializers.ValidationError("Points to reach must be greater than zero.")
        return value