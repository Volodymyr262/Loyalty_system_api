import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from loyalty.models import LoyaltyProgram, SpecialTask, UserTaskProgress
from django.utils.timezone import now, timedelta

# API Endpoints
SPECIAL_TASK_LIST_URL = "/api/special-tasks/"
USER_TASK_PROGRESS_URL = "/api/user-task-progress/"

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Returns an APIClient instance."""
    return APIClient()


@pytest.fixture
def create_users(db):
    """Create two users (owner and another user)."""
    owner = User.objects.create_user(username="owner", password="securepassword")
    another_user = User.objects.create_user(username="anotheruser", password="securepassword")
    return owner, another_user


@pytest.fixture
def auth_client(api_client, create_users):
    """Authenticated API client for the owner."""
    owner, _ = create_users
    token = Token.objects.create(user=owner)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client, owner


@pytest.fixture
def create_loyalty_program(auth_client):
    """Creates a loyalty program for the owner."""
    api_client, owner = auth_client
    program = LoyaltyProgram.objects.create(name="VIP Rewards", owner=owner)
    return program


@pytest.fixture
def create_special_task(create_loyalty_program):
    """Creates a Special Task inside the loyalty program."""
    program = create_loyalty_program
    task = SpecialTask.objects.create(
        name="Earn 200 Points",
        program=program,
        description="Earn 200 points to complete this task.",
        points_required=200,
        transactions_required=3,
        duration_days=7,
        reward_points=50
    )
    return task


@pytest.fixture
def create_user_task_progress(create_special_task):
    """Creates a UserTaskProgress instance linked to a special task."""
    task = create_special_task
    progress = UserTaskProgress.objects.create(
        user_id="12345",
        task=task,
        points_earned=100,
        transactions_count=2
    )
    return progress


def test_create_special_task(auth_client, create_loyalty_program):
    """Test creating a special task."""
    api_client, _ = auth_client
    data = {
        "name": "Complete 3 Transactions",
        "description": "Make 3 transactions to earn bonus points.",
        "points_required": 200,
        "transactions_required": 3,
        "duration_days": 5,
        "reward_points": 100,
        "program": create_loyalty_program.id,
    }
    response = api_client.post(SPECIAL_TASK_LIST_URL, data)

    assert response.status_code == 201
    assert response.data["name"] == data["name"]
    assert response.data["program"] == create_loyalty_program.id


def test_get_special_task_list(auth_client, create_special_task):
    """Test listing special tasks."""
    api_client, _ = auth_client
    response = api_client.get(SPECIAL_TASK_LIST_URL)

    assert response.status_code == 200
    assert len(response.data) > 0


def test_retrieve_special_task(auth_client, create_special_task):
    """Test retrieving a single special task."""
    api_client, _ = auth_client
    response = api_client.get(f"{SPECIAL_TASK_LIST_URL}{create_special_task.id}/")

    assert response.status_code == 200
    assert response.data["name"] == create_special_task.name


def test_update_special_task(auth_client, create_special_task):
    """Test updating a special task."""
    api_client, _ = auth_client
    updated_data = {"name": "Updated Task Name"}
    response = api_client.patch(f"{SPECIAL_TASK_LIST_URL}{create_special_task.id}/", updated_data)

    assert response.status_code == 200
    assert response.data["name"] == updated_data["name"]


def test_delete_special_task(auth_client, create_special_task):
    """Test deleting a special task."""
    api_client, _ = auth_client
    response = api_client.delete(f"{SPECIAL_TASK_LIST_URL}{create_special_task.id}/")

    assert response.status_code == 204


def test_non_owner_cannot_modify_task(api_client, create_users, create_special_task):
    """Ensure a non-owner cannot update/delete tasks."""
    _, another_user = create_users
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    updated_data = {"name": "Hacked Task"}
    response = api_client.patch(f"{SPECIAL_TASK_LIST_URL}{create_special_task.id}/", updated_data)
    assert response.status_code == 403  # Forbidden

    response = api_client.delete(f"{SPECIAL_TASK_LIST_URL}{create_special_task.id}/")
    assert response.status_code == 403


def test_create_user_task_progress(auth_client, create_special_task):
    """Test creating user task progress."""
    api_client, _ = auth_client
    data = {
        "user_id": "12345",
        "task": create_special_task.id,
        "points_earned": 100,
        "transactions_count": 2,
    }
    response = api_client.post(USER_TASK_PROGRESS_URL, data)

    assert response.status_code == 201
    assert response.data["user_id"] == "12345"


def test_update_user_task_progress(auth_client, create_user_task_progress):
    """Test updating user task progress."""
    api_client, _ = auth_client
    updated_data = {"points_earned": 200, "transactions_count": 3}
    response = api_client.patch(f"{USER_TASK_PROGRESS_URL}{create_user_task_progress.id}/", updated_data)

    assert response.status_code == 200
    assert response.data["points_earned"] == 200
    assert response.data["transactions_count"] == 3


def test_reward_user_on_completion(auth_client, create_user_task_progress):
    """Test if a user is rewarded when completing a task."""
    api_client, _ = auth_client
    updated_data = {"points_earned": 200, "transactions_count": 3}  # Meets task requirements

    response = api_client.patch(f"{USER_TASK_PROGRESS_URL}{create_user_task_progress.id}/", updated_data)
    assert response.status_code == 200
    assert response.data["completed_at"] is not None  # Task should be marked as completed


def test_non_owner_cannot_modify_user_progress(api_client, create_users, create_user_task_progress):
    """Ensure a non-owner cannot update user task progress."""
    _, another_user = create_users
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    updated_data = {"points_earned": 500}
    response = api_client.patch(f"{USER_TASK_PROGRESS_URL}{create_user_task_progress.id}/", updated_data)
    assert response.status_code == 403
