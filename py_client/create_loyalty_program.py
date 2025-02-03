import requests

BASE_URL = "http://127.0.0.1:8000/api/loyalty-programs/"


data = {
    'name': 'Lp12',
    'description': 'buy shit get more',
    'point_conversion_rate': 1

}

response = requests.post(f"{BASE_URL}", json=data)

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
