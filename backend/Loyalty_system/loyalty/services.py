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
    """ Updates the user's task progress when a transaction is created. """


    user_id = transaction.user_id

    #  Retrieve all special tasks for this program
    special_tasks = SpecialTask.objects.filter(program=transaction.program)

    for task in special_tasks:
        #  Get or create progress entry for this user and task
        progress, created = UserTaskProgress.objects.get_or_create(
            user_id=user_id, task=task
        )

        #  Update points and transaction count
        if transaction.transaction_type == "earn":
            progress.points_earned += transaction.points
            progress.transactions_count += 1  # Assume each transaction counts as one

        progress.save()

        #  Check if the task is now completed
        progress.reward_user()