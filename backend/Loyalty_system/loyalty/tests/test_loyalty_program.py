import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from loyalty.models import LoyaltyProgram  # Import your model

# API endpoints
LOYALTY_PROGRAM_LIST_URL = "/api/loyalty-programs/"
LOYALTY_PROGRAM_DETAIL_URL = lambda pk: f"/api/loyalty-programs/{pk}/"

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """ Returns an APIClient instance """
    return APIClient()


@pytest.fixture
def create_user(db):
    """ Creates a test user in the database """
    user = User.objects.create_user(username="testuser", password="securepassword")
    return user


@pytest.fixture
def auth_client(api_client, create_user):
    """ Returns an authenticated API client """
    token = Token.objects.create(user=create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client, create_user


@pytest.fixture
def another_user(db):
    """ Creates another user to test unauthorized actions """
    return User.objects.create_user(username="anotheruser", password="securepassword")


@pytest.fixture
def create_loyalty_programs(create_user, db):
    """ Creates multiple loyalty programs linked to the test user """
    return [
        LoyaltyProgram.objects.create(name="Program A", description="Description A", owner=create_user),
        LoyaltyProgram.objects.create(name="Program B", description="Description B", owner=create_user),
    ]


def test_create_loyalty_program(auth_client):
    """ Test creating a loyalty program """
    api_client, user = auth_client
    data = {
        "name": "New Loyalty Program",
        "description": "A great loyalty program",
    }
    response = api_client.post(LOYALTY_PROGRAM_LIST_URL, data)

    assert response.status_code == 201
    assert response.data["name"] == data["name"]


def test_get_loyalty_program_list(auth_client, create_loyalty_programs):
    """ Test retrieving a list of loyalty programs owned by the user """
    api_client, user = auth_client
    response = api_client.get(LOYALTY_PROGRAM_LIST_URL)

    assert response.status_code == 200
    assert len(response.data) == len(create_loyalty_programs)  # Ensure all programs are returned
    for program in create_loyalty_programs:
        assert any(item["name"] == program.name for item in response.data)  # Ensure each program is in response


def test_retrieve_loyalty_program(auth_client, create_loyalty_programs):
    """ Test retrieving a single loyalty program """
    api_client, user = auth_client
    program = create_loyalty_programs[0]
    response = api_client.get(LOYALTY_PROGRAM_DETAIL_URL(program.id))

    assert response.status_code == 200
    assert response.data["name"] == program.name


def test_update_loyalty_program(auth_client, create_loyalty_programs):
    """ Test updating a loyalty program by the owner """
    api_client, user = auth_client
    program = create_loyalty_programs[0]
    updated_data = {"name": "Updated Loyalty Program", "description": "Updated description"}

    response = api_client.put(LOYALTY_PROGRAM_DETAIL_URL(program.id), updated_data)

    assert response.status_code == 200
    assert response.data["name"] == updated_data["name"]


def test_delete_loyalty_program(auth_client, create_loyalty_programs):
    """ Test deleting a loyalty program by the owner """
    api_client, user = auth_client
    program = create_loyalty_programs[0]
    response = api_client.delete(LOYALTY_PROGRAM_DETAIL_URL(program.id))

    assert response.status_code == 204
    assert LoyaltyProgram.objects.filter(id=program.id).exists() is False


def test_update_loyalty_program_non_owner(api_client, another_user, create_loyalty_programs):
    """ Test updating a loyalty program as a non-owner """
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    program = create_loyalty_programs[0]
    updated_data = {"name": "Hacked Program", "description": "Unauthorized update"}
    response = api_client.put(LOYALTY_PROGRAM_DETAIL_URL(program.id), updated_data)

    assert response.status_code == 403  # Forbidden action


def test_delete_loyalty_program_non_owner(api_client, another_user, create_loyalty_programs):
    """ Test deleting a loyalty program as a non-owner """
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    program = create_loyalty_programs[0]
    response = api_client.delete(LOYALTY_PROGRAM_DETAIL_URL(program.id))

    assert response.status_code == 403  # Forbidden action
