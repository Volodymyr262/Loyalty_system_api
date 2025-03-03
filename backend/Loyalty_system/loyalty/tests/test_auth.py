import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Define API endpoints
REGISTER_URL = "/api/register/"
LOGIN_URL = "/api/login/"
LOGOUT_URL = "/api/logout/"

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """ Returns an APIClient instance """
    return APIClient()


@pytest.fixture
def create_user(db):
    """ Creates a test user in the database """
    return User.objects.create_user(username="testuser", password="securepassword")



def test_register_user(api_client):
    """ Test user registration """
    api_client = APIClient()
    data = {"username": "newuser", "password": "newpassword"}
    response = api_client.post(REGISTER_URL, data)

    assert response.status_code == 201, response.data  # Expect HTTP 201 Created


def test_register_with_existing_username(api_client, create_user):
    """ Test registering a user with an already used username """
    data = {"username": "testuser", "password": "anotherpassword"}
    response = api_client.post(REGISTER_URL, data)

    assert response.status_code == 400  # Expect 400 Bad Request
    assert "username" in response.data  # Ensure error is related to username


def test_login_user(api_client, create_user):
    """ Test user login """
    data = {"username": "testuser", "password": "securepassword"}
    response = api_client.post(LOGIN_URL, data)

    assert response.status_code == 200
    assert "token" in response.data  # Ensure token is returned


def test_login_with_invalid_credentials(api_client):
    """ Test login with wrong password """
    data = {"username": "testuser", "password": "wrongpassword"}
    response = api_client.post(LOGIN_URL, data)

    assert response.status_code == 400  # Invalid login should return 400


def test_logout_user(api_client, create_user):
    """ Test user logout """
    token = Token.objects.create(user=create_user)  # Create token for user
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")  # Authenticate user

    response = api_client.post(LOGOUT_URL)

    assert response.status_code == 200
    assert response.data["message"] == "Successfully logged out."


def test_logout_without_token(api_client):
    """ Test logout without authentication """
    response = api_client.post(LOGOUT_URL)

    assert response.status_code == 401  # Should return unauthorized
