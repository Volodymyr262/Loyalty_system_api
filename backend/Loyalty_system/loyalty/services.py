from .models import PointBalance, Transaction, LoyaltyProgram, UserTaskProgress, SpecialTask


def earn_points(user_id, program_id, points):
    """Earn points for a user in a loyalty program."""
    balance, _ = PointBalance.objects.get_or_create(user_id=user_id, program_id=program_id)

    balance.add_points(points)  # This updates balance and total_points_earned
    return balance

def redeem_points(user_id, program_id, points):
    """Redeem points for a user in a loyalty program."""
    balance = PointBalance.objects.get(user_id=user_id, program_id=program_id)

    if balance.balance < points:
        raise ValueError("Insufficient points")

    balance.redeem_points(points)
    return balance



def update_task_progress_for_transaction(transaction):
    """
    Update task progress for a transaction.
    """
    user = transaction.user
    program = transaction.program
    tasks = SpecialTask.objects.filter(program=program)

    for task in tasks:
        # Get or create a progress entry for this task
        progress, _ = UserTaskProgress.objects.get_or_create(user=user, task=task)

        # Update points and transaction counts
        progress.points_earned += transaction.points
        progress.transactions_count += 1

        # Check if the task is completed
        if progress.is_completed():
            progress.reward_user()

        progress.save()
