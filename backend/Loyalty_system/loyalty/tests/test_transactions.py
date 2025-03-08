import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from loyalty.models import LoyaltyProgram, Transaction, PointBalance
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils.timezone import now

# API Endpoints
TRANSACTION_LIST_URL = "/api/transactions/"

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Returns an APIClient instance"""
    return APIClient()


@pytest.fixture
def create_users(db):
    """Creates an owner and a regular user"""
    owner = User.objects.create_user(username="owner", password="securepassword")
    another_user = User.objects.create_user(username="user", password="securepassword")
    return owner, another_user


@pytest.fixture
def auth_client(api_client, create_users):
    """Authenticated API client for the owner user"""
    owner, _ = create_users
    token = Token.objects.create(user=owner)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client, owner


@pytest.fixture
def create_loyalty_program(auth_client):
    """Creates a loyalty program owned by the authenticated user"""
    _, owner = auth_client
    return LoyaltyProgram.objects.create(name="VIP Rewards", owner=owner)


@pytest.fixture
def create_transaction(create_loyalty_program):
    """Creates a sample transaction"""
    program = create_loyalty_program
    return Transaction.objects.create(
        user_id="12345",
        program=program,
        transaction_type="earn",
        points=50,
    )


def test_create_transaction(auth_client, create_loyalty_program):
    """ Test creating a transaction"""
    api_client, _ = auth_client
    data = {
        "user_id": "12345",
        "program": create_loyalty_program.id,
        "transaction_type": "earn",
        "points": 100,
    }

    response = api_client.post(TRANSACTION_LIST_URL, data)

    assert response.status_code == 201
    assert response.data["user_id"] == "12345"
    assert response.data["points"] == 100


def test_retrieve_transaction_list(auth_client, create_transaction):
    """ Test retrieving a list of transactions for a program"""
    api_client, _ = auth_client
    program_id = create_transaction.program.id

    response = api_client.get(f"{TRANSACTION_LIST_URL}?program_id={program_id}")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["user_id"] == "12345"


def test_filter_transactions_by_user(auth_client, create_transaction):
    """ Test filtering transactions by user_id"""
    api_client, _ = auth_client
    program_id = create_transaction.program.id
    user_id = create_transaction.user_id

    response = api_client.get(f"{TRANSACTION_LIST_URL}?program_id={program_id}&user_id={user_id}")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["user_id"] == user_id


def test_filter_transactions_by_date(auth_client, create_transaction):
    """ Test filtering transactions by date range"""
    api_client, _ = auth_client
    program_id = create_transaction.program.id

    # Correct format
    start_date = (now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_date = (now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    response = api_client.get(f"{TRANSACTION_LIST_URL}?program_id={program_id}&start_date={start_date}&end_date={end_date}")

    assert response.status_code == 200
    assert len(response.data) == 1


def test_create_transaction_missing_fields(auth_client):
    """ Test transaction creation fails with missing fields"""
    api_client, _ = auth_client
    data = {"user_id": "12345"}  # Missing program, transaction_type, points

    response = api_client.post(TRANSACTION_LIST_URL, data)

    assert response.status_code == 400


def test_non_owner_cannot_access_transactions(api_client, create_users, create_loyalty_program):
    """ Test that a non-owner cannot view transactions"""
    _, another_user = create_users  # Ensure we're using a non-owner
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")  # Authenticate as non-owner

    response = api_client.get(f"{TRANSACTION_LIST_URL}?program_id={create_loyalty_program.id}")

    print("🔍 Debug Response:", response.status_code, response.data)  #  Print response for debugging

    assert response.status_code == 403  #  Should be Forbidden


def test_transaction_updates_task_progress(auth_client, create_loyalty_program):
    """ Test that creating a transaction updates user task progress"""
    api_client, _ = auth_client
    data = {
        "user_id": "12345",  # Correct field
        "program": create_loyalty_program.id,
        "transaction_type": "earn",
        "points": 200,
    }

    response = api_client.post(f"{TRANSACTION_LIST_URL}create_and_update_task_progress/", data)

    assert response.status_code == 201  # ✅ Should be created