from .models import PointBalance, Transaction, LoyaltyProgram, UserTaskProgress, SpecialTask


def earn_points(user_id, program_id, amount):
    try:
        program = LoyaltyProgram.objects.get(id=program_id)
        balance, _ = PointBalance.objects.get_or_create(user_id=user_id, program_id=program_id)
        balance.add_points(amount*program.point_conversion_rate)

        # Log the transaction
        Transaction.objects.create(
            user_id=user_id,
            program_id=program_id,
            transaction_type='earn',
            points=amount
        )
        return balance
    except Exception as e:
        raise ValueError(f"Error earning points: {e}")


def redeem_points(user_id, program_id, points):
    try:
        program = LoyaltyProgram.objects.get(id=program_id)
        balance = PointBalance.objects.get(user_id=user_id, program_id=program_id)
        balance.redeem_points(points)

        # Log the transaction
        Transaction.objects.create(
            user_id=user_id,
            program_id=program_id,
            transaction_type='redeem',
            points=points
        )
        return balance
    except PointBalance.DoesNotExist:
        raise ValueError("Point balance not found")
    except Exception as e:
        raise ValueError(f"Error redeeming points: {e}")


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
