import requests

BASE_URL = "http://127.0.0.1:8000/api/loyalty-tier/"

def create_tier(tier_name, program_id, points_to_reach, description=""):
    """Create a new loyalty tier."""
    payload = {
        "tier_name": tier_name,
        "program": program_id,
        "points_to_reach": points_to_reach,
        "description": description
    }
    response = requests.post(BASE_URL, json=payload)
    print(f"Create Tier Response ({response.status_code}):", response.json())

def get_tier(tier_id):
    """Retrieve a loyalty tier by ID."""
    response = requests.get(f"{BASE_URL}{tier_id}/")
    print(f"Get Tier Response ({response.status_code}):", response.json())

def list_tiers():
    """List all loyalty tiers."""
    response = requests.get(BASE_URL)
    print(f"List Tiers Response ({response.status_code}):", response.json())

def update_tier(tier_id, new_data):
    """Update an existing loyalty tier."""
    response = requests.put(f"{BASE_URL}{tier_id}/", json=new_data)
    print(f"Update Tier Response ({response.status_code}):", response.json())

def delete_tier(tier_id):
    """Delete a loyalty tier by ID."""
    response = requests.delete(f"{BASE_URL}{tier_id}/")
    print(f"Delete Tier Response ({response.status_code}):", response.text)

# Example Test Scenarios
if __name__ == "__main__":
    # Step 1: Create a new loyalty tier
    create_tier("Gold", program_id=8, points_to_reach=1000, description="Top-tier membership benefits.")
    create_tier("Silver", program_id=8, points_to_reach=500, description="Mid-tier membership benefits.")

    # Step 2: List all tiers
    list_tiers()

    # Step 3: Get a specific tier (replace <id> with the actual ID from the list_tiers output)
    get_tier(tier_id=1)

    # Step 4: Update a specific tier
    update_tier(tier_id=1, new_data={
        "tier_name": "Platinum",
        "program": 1,
        "points_to_reach": 2000,
        "description": "Updated top-tier membership benefits."
    })

    # Step 5: Delete a specific tier
    delete_tier(tier_id=2)  # Replace with the ID of the tier to delete

