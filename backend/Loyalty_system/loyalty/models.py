from django.db import models


class LoyaltyProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    point_conversion_rate = models.FloatField(default=1.0)  # 1 point = X currency
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PointBalance(models.Model):
    user_id = models.CharField(max_length=255)  # Use CharField for flexible user ID
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="balances")
    balance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user_id', 'program')


    def add_points(self, points):
        """ Add points to the user's  balance"""
        self.balance += points
        self.save()


    def redeem_points(self, points):
        """ Redeem points from the user's  balance"""
        if points > self.balance:
            raise ValueError('Insufficient points')
        self.balance -= points
        self.save()


    def __str__(self):
        return f"User {self.user_id} - {self.program.name}: {self.balance} points"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('earn', 'Earn'),
        ('redeem', 'Redeem'),
    ]

    user_id = models.CharField(max_length=255)  # Use CharField for flexible user ID
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.points} points - User {self.user_id}"


class LoyaltyTier(models.Model):
    tier_name = models.CharField(max_length=40)
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="loyalty_tiers")
    points_to_reach = models.PositiveIntegerField()  # Enforce positive values
    description = models.TextField(blank=True, null=True)  # Optional description for the tier

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tier_name', 'program'], name='unique_tier_per_program'),
        ]
        ordering = ['points_to_reach']  # Default ordering by points required

    def __str__(self):
        return f"{self.tier_name} (Program: {self.program.name}, Points: {self.points_to_reach})"


class Achievement(models.Model):
    TYPE_CHOICES = [
        ('action', 'Action-Based'),
        ('milestone', 'Milestone-Based'),
        ('time', 'Time-Based'),
        ('fun', 'Fun/Unexpected'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    program = models.ForeignKey(
        'LoyaltyProgram',
        on_delete=models.CASCADE,
        related_name="achievements"
    )
    points_required = models.PositiveIntegerField(default=0, blank=True)  # Optional
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='action')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"