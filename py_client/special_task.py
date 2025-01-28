import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

# Endpoints
SPECIAL_TASKS_ENDPOINT = f"{BASE_URL}/special-tasks/"
USER_PROGRESS_ENDPOINT = f"{BASE_URL}/user-task-progress/"


def create_special_task(name, program_id, description, points_required, transactions_required, duration_days, reward_points):
    payload = {
        "name": name,
        "program": program_id,
        "description": description,
        "points_required": points_required,
        "transactions_required": transactions_required,
        "duration_days": duration_days,
        "reward_points": reward_points,
    }
    response = requests.post(SPECIAL_TASKS_ENDPOINT, json=payload)
    print(f"Create Special Task Response ({response.status_code}):", response.json())
    return response.json()


def update_user_progress(user_id, task_id, points_earned, transactions_count):
    payload = {
        "user_id": user_id,
        "task": task_id,
        "points_earned": points_earned,
        "transactions_count": transactions_count,
    }
    response = requests.post(USER_PROGRESS_ENDPOINT, json=payload)
    print(f"Update User Progress Response ({response.status_code}):", response.json())
    return response.json()


def get_user_progress(user_id):
    params = {"user_id": user_id}
    response = requests.get(USER_PROGRESS_ENDPOINT, params=params)
    print(f"User Progress ({response.status_code}):", response.json())
    return response.json()


if __name__ == "__main__":
    # Create two special tasks
    task1 = create_special_task(
        name="Earn 200 Points in 2 Days (Task 1)",
        program_id=1,
        description="Earn 200 points by completing 4 transactions in 2 days.",
        points_required=200,
        transactions_required=4,
        duration_days=2,
        reward_points=50
    )

    task2 = create_special_task(
        name="Earn 200 Points in 2 Days (Task 2)",
        program_id=1,
        description="Earn 200 points by completing 4 transactions in 2 days.",
        points_required=200,
        transactions_required=4,
        duration_days=2,
        reward_points=50
    )

    # Update progress for both tasks
    update_user_progress(user_id="12345", task_id=task1.get("id"), points_earned=200, transactions_count=4)
    update_user_progress(user_id="12345", task_id=task2.get("id"), points_earned=200, transactions_count=4)

    # Get user progress
    get_user_progress(user_id="12345")
