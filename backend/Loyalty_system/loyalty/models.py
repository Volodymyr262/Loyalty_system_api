from django.db import models
from django.contrib.auth.models import User


class LoyaltyProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    point_conversion_rate = models.FloatField(default=1.0)  # 1 point = X currency
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PointBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="point_balances")
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="balances")
    balance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'program')

    def __str__(self):
        return f"{self.user.username} - {self.program.name}: {self.balance} points"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('earn', 'Earn'),
        ('redeem', 'Redeem'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.points} points - {self.user.username}"