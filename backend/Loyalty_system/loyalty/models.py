from django.db import models
from datetime import timedelta, timezone

from django.utils.timezone import now


class LoyaltyProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    point_conversion_rate = models.FloatField(default=1.0)  # 1 point = X currency
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PointBalance(models.Model):
    user_id = models.CharField(max_length=255)
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="balances")
    balance = models.IntegerField(default=0)
    total_points_earned = models.IntegerField(default=0)  # ✅ Track total earned points

    class Meta:
        unique_together = ('user_id', 'program')

    def add_points(self, points):
        """ ✅ Add points and update total earned points """
        self.balance += points
        self.total_points_earned += points  # ✅ Ensure total earned points updates
        self.save(update_fields=['balance', 'total_points_earned'])  # ✅ Force DB save

    def redeem_points(self, points):
        """ ✅ Redeem points from balance """
        if points > self.balance:
            raise ValueError('Insufficient points')
        self.balance -= points
        self.save(update_fields=['balance'])

    def get_loyalty_tier(self):
        """ ✅ Dynamically determine the highest tier the user qualifies for based on `total_points_earned` """
        eligible_tiers = LoyaltyTier.objects.filter(
            program=self.program,
            points_to_reach__lte=self.total_points_earned  # ✅ Use `total_points_earned`
        ).order_by('-points_to_reach')  # Get the highest eligible tier

        return eligible_tiers.first().tier_name if eligible_tiers.exists() else "No Tier"

    def __str__(self):
        return f"User {self.user_id} - {self.program.name}: {self.balance} points (Total Earned: {self.total_points_earned})"


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
    points_to_reach = models.PositiveIntegerField()  # Required points to reach the tier
    description = models.TextField(blank=True, null=True)  # Optional description

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tier_name', 'program'], name='unique_tier_per_program'),
        ]
        ordering = ['points_to_reach']  # Ensures we get the lowest tier first

    def __str__(self):
        return f"{self.tier_name} (Program: {self.program.name}, Points: {self.points_to_reach})"



class SpecialTask(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey('LoyaltyProgram', on_delete=models.CASCADE, related_name="special_tasks")
    description = models.TextField()
    points_required = models.PositiveIntegerField(default=0)  # E.g., Earn 200 points
    transactions_required = models.PositiveIntegerField(default=0)  # E.g., Complete 4 transactions
    duration_days = models.PositiveIntegerField()  # E.g., Task must be completed in 2 days
    reward_points = models.PositiveIntegerField(default=0)  # Bonus points
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Program: {self.program.name})"

    def get_deadline(self):
        return self.created_at + timedelta(days=self.duration_days)



class UserTaskProgress(models.Model):
    user_id = models.CharField(max_length=255)
    task = models.ForeignKey(SpecialTask, on_delete=models.CASCADE, related_name="user_progress")
    points_earned = models.PositiveIntegerField(default=0)
    transactions_count = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(blank=True, null=True)

    def is_completed(self):
        """
        Check if the user has met the task requirements.
        """
        return (
            self.points_earned >= self.task.points_required and
            self.transactions_count >= self.task.transactions_required
        )

    def reward_user(self):
        """
        Reward the user and mark the task as completed.
        """
        if self.is_completed() and not self.completed_at:
            # ✅ **Mark task as completed**
            self.completed_at = now()

            # ✅ **Debugging Print Statement**
            print(f"✅ User {self.user_id} has completed task '{self.task.name}'. Marking as completed.")

            # ✅ **Save the updated progress**
            self.save()