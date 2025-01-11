from .models import PointBalance, Transaction


def earn_points(user_id, program_id, points):
    try:
        balance, _ = PointBalance.objects.get_or_create(user_id=user_id, program_id=program_id)
        balance.add_points(points)

        # Log the transaction
        Transaction.objects.create(
            user_id=user_id,
            program_id=program_id,
            transaction_type='earn',
            points=points
        )
        return balance
    except Exception as e:
        raise ValueError(f"Error earning points: {e}")


def redeem_points(user_id, program_id, points):
    try:
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
