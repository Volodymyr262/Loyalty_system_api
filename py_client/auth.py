import requests

BASE_URL = "http://127.0.0.1:8000/api"  # Change if needed

# Test user credentials
TEST_USER = {
    "username": "testuser1232",
    "password": "securepassword"
}

# Endpoints
REGISTER_URL = f"{BASE_URL}/register/"
LOGIN_URL = f"{BASE_URL}/login/"
LOGOUT_URL = f"{BASE_URL}/logout/"

def register_user():
    """ ✅ Register a new user """
    response = requests.post(REGISTER_URL, json=TEST_USER)
    print(f"[REGISTER] {response.status_code}: {response.json()}")
    return response

def login_user():
    """ ✅ Log in and retrieve authentication token """
    response = requests.post(LOGIN_URL, json=TEST_USER)
    print(f"[LOGIN] {response.status_code}: {response.json()}")
    if response.status_code == 200:
        return response.json().get("token")  # Return the auth token
    return None

def logout_user(token):
    """ ✅ Log out the user by sending the token """
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(LOGOUT_URL, headers=headers)
    print(f"[LOGOUT] {response.status_code}: {response.json()}")

def run_tests():
    print("🚀 Running Authentication Tests...")

    # Step 1: Register user
    register_response = register_user()

    # If user already exists, continue testing login & logout
    if register_response.status_code in [201, 400]:  # 400 means user exists
        # Step 2: Log in the user
        token = login_user()
        if token:
            # Step 3: Log out the user
            logout_user(token)
        else:
            print("❌ Login failed, skipping logout.")
    else:
        print("❌ Registration failed, skipping login/logout.")

    print("✅ Authentication Tests Completed!")

if __name__ == "__main__":
    run_tests()
