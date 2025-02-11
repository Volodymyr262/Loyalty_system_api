import requests

BASE_URL = "http://127.0.0.1:8000/api"  # Change if necessary

# User and Program Data
USER_ID = "12345"
PROGRAM_NAME = "VIP Rewards"

LOYALTY_TIERS = [
    {"tier_name": "Bronze", "points_to_reach": 100},
    {"tier_name": "Silver", "points_to_reach": 300},
    {"tier_name": "Gold", "points_to_reach": 500},
]

# Endpoints
PROGRAMS_ENDPOINT = f"{BASE_URL}/loyalty-programs/"
TIERS_ENDPOINT = f"{BASE_URL}/loyalty-tiers/"
POINT_BALANCE_ENDPOINT = f"{BASE_URL}/point-balances/"
TRANSACTION_ENDPOINT = f"{BASE_URL}/transactions/"


# ---- 1. Create Loyalty Program ----
def create_loyalty_program():
    payload = {"name": PROGRAM_NAME, "description": "Exclusive VIP Rewards"}
    response = requests.post(PROGRAMS_ENDPOINT, json=payload)
    print(f"[CREATE LOYALTY PROGRAM] {response.status_code}: {response.json()}")
    return response.json()["id"]


# ---- 2. Create Tiers ----
def create_loyalty_tiers(program_id):
    tier_ids = []
    for tier in LOYALTY_TIERS:
        tier["program"] = program_id
        response = requests.post(TIERS_ENDPOINT, json=tier)
        print(f"[CREATE TIER {tier['tier_name']}] {response.status_code}: {response.json()}")
        tier_ids.append(response.json()["id"])
    return tier_ids


# ---- 3. Create User's Point Balance ----
def create_point_balance(user_id, program_id):
    payload = {"user_id": user_id, "program": program_id, "balance": 0, "total_points_earned": 0}
    response = requests.post(POINT_BALANCE_ENDPOINT, json=payload)
    print(f"[CREATE POINT BALANCE] {response.status_code}: {response.json()}")
    return response.json()["id"]


# ---- 4. Add Points ----
def add_points(user_id, program_id, points):
    payload = {
        "user_id": user_id,
        "program": program_id,
        "transaction_type": "earn",
        "points": points
    }
    response = requests.post(TRANSACTION_ENDPOINT, json=payload)
    print(f"[EARN {points} POINTS] {response.status_code}: {response.json()}")


# ---- 5. Redeem Points ----
def redeem_points(user_id, program_id, points):
    payload = {
        "user_id": user_id,
        "program": program_id,
        "transaction_type": "redeem",
        "points": points
    }
    response = requests.post(TRANSACTION_ENDPOINT, json=payload)
    print(f"[REDEEM {points} POINTS] {response.status_code}: {response.json()}")


# ---- 6. Check User's Balance & Tier ----
def check_user_balance(user_id, program_id):
    params = {"user_id": user_id, "program_id": program_id}
    response = requests.get(POINT_BALANCE_ENDPOINT, params=params)

    if response.status_code == 200:
        data = response.json()
        balance = data.get("balance", 0)
        total_points_earned = data.get("total_points_earned", 0)
        tier = data.get("tier", "No Tier")  # API should return the current tier

        print(
            f"[CHECK BALANCE] {response.status_code}: User {user_id} - Balance: {balance} | Total Earned: {total_points_earned} | Tier: {tier}")
        return data
    else:
        print(f"[CHECK BALANCE] {response.status_code}: {response.json()}")
        return None


# ---- RUN ALL TESTS ----
def run_tests():
    print("🚀 Starting PointBalance Tests...")

    # Step 1: Create Loyalty Program
    program_id = create_loyalty_program()

    # Step 2: Create Loyalty Tiers
    create_loyalty_tiers(program_id)

    # Step 3: Create User's Point Balance
    create_point_balance(USER_ID, program_id)

    # Step 4: User Earns 150 Points (Should qualify for Bronze)
    add_points(USER_ID, program_id, 150)
    check_user_balance(USER_ID, program_id)

    # Step 5: User Earns 200 More Points (Should qualify for Silver)
    add_points(USER_ID, program_id, 200)
    check_user_balance(USER_ID, program_id)

    # Step 6: User Redeems 200 Points (Should NOT lose tier)
    redeem_points(USER_ID, program_id, 200)
    check_user_balance(USER_ID, program_id)

    # Step 7: User Earns 300 More Points (Should qualify for Gold)
    add_points(USER_ID, program_id, 300)
    check_user_balance(USER_ID, program_id)

    print("✅ All PointBalance tests completed successfully!")


if __name__ == "__main__":
    run_tests()
