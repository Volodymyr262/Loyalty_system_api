import requests

# Base API URL
BASE_URL = "http://127.0.0.1:8000/api/points/"


# Payload for Redeeming Points
payload = {
    "user_id": 12,
    "program_id": 9,
    "points": 100
}

# Send POST Request to Redeem Points
response = requests.post(f"{BASE_URL}?action=earn", json=payload)

# Print Results
if response.status_code == 200:
    print("Success:")
    print(response.json())
elif response.status_code == 400:
    print("Failed to Redeem Points:")
    print(response.json())
else:
    print(f"Unexpected Status Code: {response.status_code}")
    print(response.json())
