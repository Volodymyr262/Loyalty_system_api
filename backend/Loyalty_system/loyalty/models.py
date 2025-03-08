from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta
from django.utils.timezone import now

User = get_user_model()

### LOYALTY PROGRAM MODEL ###
class LoyaltyProgram(models.Model):
    """
    Represents a loyalty program created by a business owner.
    Customers can earn and redeem points within this program.
    """
    name = models.CharField(max_length=255)  # Program name (e.g., "VIP Rewards")
    description = models.TextField(blank=True)  # Optional description of the program
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when program was created
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_programs')
    # The user (owner) who manages this loyalty program

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"

### POINT BALANCE MODEL ###
class PointBalance(models.Model):
    """
    Tracks the points balance of an application user for a specific loyalty program.
    """
    user_id = models.CharField(max_length=255)  # ID of the API user earning points
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="balances")
    balance = models.IntegerField(default=0)  # Current balance of points
    total_points_earned = models.IntegerField(default=0)  # Total points earned over time

    class Meta:
        unique_together = ('user_id', 'program')  # A user can only have one balance per program

    def add_points(self, points):
        """  Add points to the balance and update the total earned points """
        self.balance += points
        self.total_points_earned += points
        self.save(update_fields=['balance', 'total_points_earned'])

    def redeem_points(self, points):
        """  Redeem points from balance, ensuring it doesn't go negative """
        if points > self.balance:
            raise ValueError('Insufficient points')
        self.balance -= points
        self.save(update_fields=['balance'])

    def get_loyalty_tier(self):
        """  Determine the highest loyalty tier based on total earned points """
        eligible_tiers = LoyaltyTier.objects.filter(
            program=self.program,
            points_to_reach__lte=self.total_points_earned
        ).order_by('-points_to_reach')

        return eligible_tiers.first().tier_name if eligible_tiers.exists() else "No Tier"

    def __str__(self):
        return f"User {self.user_id} - {self.program.name}: {self.balance} points (Total Earned: {self.total_points_earned})"

### TRANSACTION MODEL ###
class Transaction(models.Model):
    """
    Represents a transaction where a user earns or redeems points within a loyalty program.
    """
    TRANSACTION_TYPES = [
        ('earn', 'Earn'),
        ('redeem', 'Redeem'),
    ]

    user_id = models.CharField(max_length=255)  # ID of API user making the transaction
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    points = models.IntegerField()  # Points earned or redeemed
    timestamp = models.DateTimeField(auto_now_add=True)  # When transaction was created

    def __str__(self):
        return f"{self.transaction_type} {self.points} points - User {self.user_id}"

### LOYALTY TIER MODEL ###
class LoyaltyTier(models.Model):
    """
    Defines tiers within a loyalty program, based on points earned.
    """
    tier_name = models.CharField(max_length=40)  # Name of the tier (e.g., Bronze, Silver, Gold)
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="loyalty_tiers")
    points_to_reach = models.PositiveIntegerField()  # Points required to achieve this tier
    description = models.TextField(blank=True, null=True)  # Optional description

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tier_name', 'program'], name='unique_tier_per_program'),
        ]
        ordering = ['points_to_reach']  # Ensures tiers are sorted by required points

    def __str__(self):
        return f"{self.tier_name} (Program: {self.program.name}, Points: {self.points_to_reach})"

### SPECIAL TASK MODEL ###
class SpecialTask(models.Model):
    """
    Represents a special task that users can complete for bonus points.
    Example: "Make 5 purchases in a month to earn 500 extra points."
    """
    name = models.CharField(max_length=100)  # Task name
    program = models.ForeignKey('LoyaltyProgram', on_delete=models.CASCADE, related_name="special_tasks")
    description = models.TextField()  # Description of the task
    points_required = models.PositiveIntegerField(default=0)  # Points user must earn to complete the task
    transactions_required = models.PositiveIntegerField(default=0)  # Number of transactions required
    duration_days = models.PositiveIntegerField()  # Time limit to complete the task
    reward_points = models.PositiveIntegerField(default=0)  # Bonus points awarded upon completion
    created_at = models.DateTimeField(auto_now_add=True)  # When task was created

    def __str__(self):
        return f"{self.name} (Program: {self.program.name})"

    def get_deadline(self):
        """  Calculate task deadline based on the creation date """
        return self.created_at + timedelta(days=self.duration_days)

### USER TASK PROGRESS MODEL ###
class UserTaskProgress(models.Model):
    """
    Tracks the progress of a user towards completing a special task.
    """
    user_id = models.CharField(max_length=255)  # ID of the API user completing the task
    task = models.ForeignKey(SpecialTask, on_delete=models.CASCADE, related_name="user_progress")
    points_earned = models.PositiveIntegerField(default=0)  # Points the user has earned for the task
    transactions_count = models.PositiveIntegerField(default=0)  # Transactions completed for the task
    completed_at = models.DateTimeField(blank=True, null=True)  # Timestamp when task was completed

    def is_completed(self):
        """  Check if the user has met the task requirements """
        return (
            self.points_earned >= self.task.points_required and
            self.transactions_count >= self.task.transactions_required
        )

    def reward_user(self):
        """
         If the task is completed, mark it as completed and apply the reward.
        """
        if self.is_completed() and not self.completed_at:
            self.completed_at = now()

            # ✅ Debugging statement (remove in production)
            print(f" User {self.user_id} has completed task '{self.task.name}'. Marking as completed.")

            self.save()

    def __str__(self):
        return f"Progress: User {self.user_id} on '{self.task.name}' - {self.points_earned}/{self.task.points_required} points"
