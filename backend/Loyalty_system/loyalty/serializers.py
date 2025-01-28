from rest_framework import serializers
from .models import LoyaltyProgram, PointBalance, Transaction, LoyaltyTier, UserTaskProgress, SpecialTask


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


class SpecialTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the SpecialTask model.
    """
    class Meta:
        model = SpecialTask
        fields = '__all__'


class UserTaskProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserTaskProgress model.
    Includes related task details for context.
    """
    task_name = serializers.ReadOnlyField(source='task.name')  # Include task name in response
    task_description = serializers.ReadOnlyField(source='task.description')

    class Meta:
        model = UserTaskProgress
        fields = ['id', 'user_id', 'task', 'task_name', 'task_description',
                  'points_earned', 'transactions_count', 'completed_at']