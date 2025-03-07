import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from loyalty.models import LoyaltyProgram, LoyaltyTier

# API Endpoints
LOYALTY_TIER_LIST_URL = "/api/loyalty-tiers/"

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Returns an APIClient instance"""
    return APIClient()


@pytest.fixture
def create_users(db):
    """Create two users for testing (owner & another user)"""
    owner = User.objects.create_user(username="owner", password="securepassword")
    another_user = User.objects.create_user(username="anotheruser", password="securepassword")
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
    """Create a loyalty program for the owner"""
    api_client, owner = auth_client
    program = LoyaltyProgram.objects.create(name="VIP Rewards", owner=owner)
    return program


@pytest.fixture
def create_loyalty_tiers(create_loyalty_program):
    """Create multiple tiers for a loyalty program"""
    program = create_loyalty_program
    bronze = LoyaltyTier.objects.create(program=program, tier_name="Bronze", points_to_reach=100)
    silver = LoyaltyTier.objects.create(program=program, tier_name="Silver", points_to_reach=300)
    gold = LoyaltyTier.objects.create(program=program, tier_name="Gold", points_to_reach=500)
    return [bronze, silver, gold]


# ✅ 1. Test Creating a Loyalty Tier
def test_create_loyalty_tier(auth_client, create_loyalty_program):
    """Test that the owner can create a new loyalty tier"""
    api_client, _ = auth_client
    data = {
        "tier_name": "Platinum",
        "points_to_reach": 1000,
        "program": create_loyalty_program.id,
    }
    response = api_client.post(LOYALTY_TIER_LIST_URL, data)

    assert response.status_code == 201
    assert response.data["tier_name"] == "Platinum"
    assert response.data["points_to_reach"] == 1000


# ✅ 2. Test Retrieving a Loyalty Tier
def test_get_loyalty_tier(auth_client, create_loyalty_tiers):
    """Test that the owner can retrieve a loyalty tier"""
    api_client, _ = auth_client
    tier = create_loyalty_tiers[0]  # Get Bronze tier

    response = api_client.get(f"{LOYALTY_TIER_LIST_URL}{tier.id}/")

    assert response.status_code == 200
    assert response.data["tier_name"] == "Bronze"


# ✅ 3. Test Listing All Tiers of a Program
def test_list_loyalty_tiers(auth_client, create_loyalty_program, create_loyalty_tiers):
    """Test that the owner can list all tiers of a loyalty program"""
    api_client, _ = auth_client

    response = api_client.get(LOYALTY_TIER_LIST_URL, {"program": create_loyalty_program.id})

    assert response.status_code == 200
    assert len(response.data) == 3  # Should return all 3 tiers


# ✅ 4. Test Updating a Loyalty Tier
def test_update_loyalty_tier(auth_client, create_loyalty_tiers):
    """Test that the owner can update a loyalty tier"""
    api_client, _ = auth_client
    tier = create_loyalty_tiers[1]  # Update Silver tier

    updated_data = {"tier_name": "Silver Elite", "points_to_reach": 350}
    response = api_client.put(f"{LOYALTY_TIER_LIST_URL}{tier.id}/", updated_data)

    assert response.status_code == 200
    assert response.data["tier_name"] == "Silver Elite"
    assert response.data["points_to_reach"] == 350


# ✅ 5. Test Deleting a Loyalty Tier
def test_delete_loyalty_tier(auth_client, create_loyalty_tiers):
    """Test that the owner can delete a loyalty tier"""
    api_client, _ = auth_client
    tier = create_loyalty_tiers[2]  # Delete Gold tier

    response = api_client.delete(f"{LOYALTY_TIER_LIST_URL}{tier.id}/")

    assert response.status_code == 204  # No content (successful deletion)


# ❌ 6. Test Non-Owner Cannot Modify Tiers
def test_non_owner_cannot_modify_tier(api_client, create_users, create_loyalty_tiers):
    """Test that a non-owner cannot update a loyalty tier"""
    _, another_user = create_users
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    tier = create_loyalty_tiers[0]  # Try modifying Bronze tier

    updated_data = {"tier_name": "Unauthorized Edit", "points_to_reach": 150}
    response = api_client.put(f"{LOYALTY_TIER_LIST_URL}{tier.id}/", updated_data)

    assert response.status_code == 403  # Forbidden


# ❌ 7. Test Non-Owner Cannot Delete Tiers
def test_non_owner_cannot_delete_tier(api_client, create_users, create_loyalty_tiers):
    """Test that a non-owner cannot delete a loyalty tier"""
    _, another_user = create_users
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    tier = create_loyalty_tiers[1]  # Try deleting Silver tier

    response = api_client.delete(f"{LOYALTY_TIER_LIST_URL}{tier.id}/")

    assert response.status_code == 403  # Forbidden
