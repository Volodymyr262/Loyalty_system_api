import requests

# Base API URL
BASE_URL = "http://127.0.0.1:8000/api/point-balances/"

# User ID for whom to fetch transactions
USER_ID = 12
PROGRAM_ID = 8
# Query parameters
params = {"user_id": USER_ID, "program_id": PROGRAM_ID}

# Send GET request
response = requests.get(BASE_URL, params=params)

# Print the results
if response.status_code == 200:
    print("Transactions fetched successfully:")
    print(response.json())
elif response.status_code == 400:
    print("Failed to fetch transactions:")
    print(response.json())
else:
    print(f"Unexpected Status Code: {response.status_code}")
    print(response.json())
