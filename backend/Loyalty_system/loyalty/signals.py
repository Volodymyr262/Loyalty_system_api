from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, PointBalance

@receiver(post_save, sender=Transaction)
def update_balance(sender, instance, created, **kwargs):
    """Automatically updates PointBalance when a new Transaction is created."""
    if created:  # Only update on new transactions
        try:
            point_balance, created = PointBalance.objects.get_or_create(
                user_id=instance.user_id,
                program=instance.program
            )

            if instance.transaction_type == 'earn':
                point_balance.balance += instance.points
                point_balance.total_points_earned += instance.points
            elif instance.transaction_type == 'redeem':
                point_balance.balance -= instance.points
                if point_balance.balance < 0:
                    point_balance.balance = 0  # Ensure balance doesn't go negative

            point_balance.save()
        except Exception as e:
            print(f"Error updating balance: {e}")
