import requests
import time
import sys

BASE_URL = "http://localhost:5000"

print("Checking Mission Service...")

try:
    response = requests.get(
        f"{BASE_URL}/health",
        timeout=5
    )
    response.raise_for_status()
    print("PASS - Mission Service is healthy")
except Exception as e:
    print("FAIL - Mission Service unavailable")
    print(e)
    sys.exit(1)


print("\nCreating test mission...")

response = requests.post(
    f"{BASE_URL}/missions",
    json={
        "start_x": 0,
        "start_y": 0,
        "destination_x": 5,
        "destination_y": 5,
        "priority": 1
    },
    timeout=5
)

response.raise_for_status()

mission = response.json()
mission_id = mission["mission_id"]

print(f"PASS - Mission {mission_id} created")


print("\nWaiting for mission completion...")

for attempt in range(15):

    time.sleep(1)

    response = requests.get(
        f"{BASE_URL}/missions/{mission_id}",
        timeout=5
    )

    data = response.json()

    print(
        f"Attempt {attempt + 1}: "
        f"{data['status']}"
    )

    if data["status"] == "COMPLETED":

        print(
            f"PASS - Robot "
            f"{data['assigned_robot_id']} "
            f"completed mission"
        )

        print("\n========================")
        print("SMOKE TEST PASSED")
        print("========================")

        sys.exit(0)


print("\nFAIL - Mission did not complete")
sys.exit(1)
