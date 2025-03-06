import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from loyalty.models import LoyaltyProgram, PointBalance, LoyaltyTier

# API Endpoints
POINT_BALANCE_LIST_URL = "/api/point-balances/"

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """ Returns an APIClient instance """
    return APIClient()


@pytest.fixture
def create_users(db):
    """ Create two users for testing (owner & another user) """
    owner = User.objects.create_user(username="owner", password="securepassword")
    another_user = User.objects.create_user(username="anotheruser", password="securepassword")
    return owner, another_user


@pytest.fixture
def auth_client(api_client, create_users):
    """ Authenticated API client for the owner user """
    owner, _ = create_users
    token = Token.objects.create(user=owner)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client, owner


@pytest.fixture
def create_loyalty_program(auth_client):
    """ Create a loyalty program for the owner """
    api_client, owner = auth_client
    program = LoyaltyProgram.objects.create(name="VIP Rewards", owner=owner)
    return program


@pytest.fixture
def create_point_balance(create_loyalty_program):
    """ Create a PointBalance for a user """
    program = create_loyalty_program
    point_balance = PointBalance.objects.create(user_id="12345", program=program, balance=100, total_points_earned=500)
    return point_balance


@pytest.fixture
def create_loyalty_tiers(create_loyalty_program):
    """ Create tiers for the loyalty program """
    program = create_loyalty_program
    LoyaltyTier.objects.create(program=program, tier_name="Bronze", points_to_reach=100)
    LoyaltyTier.objects.create(program=program, tier_name="Silver", points_to_reach=300)
    LoyaltyTier.objects.create(program=program, tier_name="Gold", points_to_reach=500)


# ✅ **1. Test creating a point balance**
def test_create_point_balance(auth_client, create_loyalty_program):
    """ Test creating a point balance for a user """
    api_client, _ = auth_client
    data = {"user_id": "12345", "program": create_loyalty_program.id, "balance": 0, "total_points_earned": 0}

    response = api_client.post(POINT_BALANCE_LIST_URL, data)

    assert response.status_code == 201
    assert response.data["user_id"] == "12345"
    assert response.data["balance"] == 0


# ✅ **2. Test retrieving a user's point balance**
def test_get_point_balance(auth_client, create_point_balance):
    """ Test fetching a user's point balance """
    api_client, _ = auth_client
    response = api_client.get(f"{POINT_BALANCE_LIST_URL}?user_id=12345&program_id={create_point_balance.program.id}")

    assert response.status_code == 200
    assert response.data["user_id"] == "12345"
    assert response.data["balance"] == 100


# ✅ **3. Test that only the owner can access point balances**
def test_only_owner_can_access_point_balance(api_client, create_users, create_loyalty_program, create_point_balance):
    """ Test that another user cannot access the owner's point balance """
    _, another_user = create_users
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    response = api_client.get(f"{POINT_BALANCE_LIST_URL}?user_id=12345&program_id={create_point_balance.program.id}")

    assert response.status_code == 403  # Forbidden


# ✅ **4. Test earning points**
def test_earn_points(auth_client, create_point_balance):
    """ Test adding points to a user's balance """
    api_client, _ = auth_client
    create_point_balance.add_points(50)

    response = api_client.get(f"{POINT_BALANCE_LIST_URL}?user_id=12345&program_id={create_point_balance.program.id}")

    assert response.status_code == 200
    assert response.data["balance"] == 150  # 100 + 50


# ✅ **5. Test redeeming points**
def test_redeem_points(auth_client, create_point_balance):
    """ Test redeeming points from a user's balance """
    api_client, _ = auth_client
    create_point_balance.redeem_points(50)

    response = api_client.get(f"{POINT_BALANCE_LIST_URL}?user_id=12345&program_id={create_point_balance.program.id}")

    assert response.status_code == 200
    assert response.data["balance"] == 50  # 100 - 50


# ✅ **6. Test redeeming points with insufficient balance**
def test_redeem_points_insufficient_balance(auth_client, create_point_balance):
    """ Test that redeeming more points than available results in an error """
    with pytest.raises(ValueError, match="Insufficient points"):
        create_point_balance.redeem_points(200)  # Balance is only 100


# ✅ **7. Test loyalty tier calculation**
def test_loyalty_tier_calculation(auth_client, create_point_balance, create_loyalty_tiers):
    """ Test getting the correct loyalty tier based on total points earned """
    api_client, _ = auth_client
    response = api_client.get(f"{POINT_BALANCE_LIST_URL}?user_id=12345&program_id={create_point_balance.program.id}")

    assert response.status_code == 200
    assert response.data["tier"] == "Gold"  # 500 points earned should give "Gold" tier


# ✅ **8. Test getting point balance for a non-existing user**
def test_get_point_balance_non_existing_user(auth_client, create_loyalty_program):
    """ Test fetching a point balance for a non-existing user """
    api_client, _ = auth_client
    response = api_client.get(f"{POINT_BALANCE_LIST_URL}?user_id=99999&program_id={create_loyalty_program.id}")  # No such user

    assert response.status_code == 403  # Not Found


# ✅ **9. Test missing query parameters when retrieving point balance**
def test_get_point_balance_missing_params(auth_client):
    """ Test fetching a point balance without user_id or program_id """
    api_client, _ = auth_client

    response = api_client.get(POINT_BALANCE_LIST_URL)  # Missing params

    assert response.status_code == 400  # Bad Request
    assert response.data["error"] == "Both user_id and program_id are required."
