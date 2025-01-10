from django.db import models


class LoyaltyProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    point_conversion_rate = models.FloatField(default=1.0)  # 1 point = X currency
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PointBalance(models.Model):
    user_id = models.IntegerField()  # Reference external user by ID
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="balances")
    balance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user_id', 'program')

    def __str__(self):
        return f"User {self.user_id} - {self.program.name}: {self.balance} points"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('earn', 'Earn'),
        ('redeem', 'Redeem'),
    ]

    user_id = models.IntegerField()  # Reference external user by ID
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.points} points - User {self.user_id}"
