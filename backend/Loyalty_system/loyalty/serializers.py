from rest_framework import serializers
from .models import LoyaltyProgram, PointBalance, Transaction, LoyaltyTier, UserTaskProgress, SpecialTask


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ ✅ Hash password before saving """
        user = User.objects.create_user(**validated_data)
        return user


class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'
        read_only_fields = ['owner']  #


class PointBalanceSerializer(serializers.ModelSerializer):
    tier = serializers.SerializerMethodField()

    def get_tier(self, obj):
        return obj.get_loyalty_tier()  #  Include tier dynamically

    class Meta:
        model = PointBalance
        fields = ['id', 'user_id', 'balance', 'program', 'tier']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class LoyaltyTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTier
        fields = "__all__"
        read_only_fields = ["program"]

    def validate(self, data):
        """Prevent updates to the `program` field after creation."""
        if self.instance and "program" in data:
            raise serializers.ValidationError({"program": "You cannot change the program of a loyalty tier."})
        return data

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